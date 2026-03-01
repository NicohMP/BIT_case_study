"""Step-3 discovery stage: high-recall candidate generation.

Channels:
- Lexical discovery: loose keyword hits (fast, transparent)
- Embedding discovery: semantic similarity against family descriptors (optional)

Discovery produces candidates, NOT trusted matches. Final acceptance comes from
strict classification.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np

from polyscanner.matching.embeddings import DBEmbeddingCache, LocalSentenceTransformerEmbedder
from polyscanner.matching.family_descriptors import FamilyDescriptor


def _norm_text(text: str) -> str:
    return " ".join((text or "").lower().split()).strip()


def _keyword_hits(text: str, keywords: Iterable[str]) -> list[str]:
    t = _norm_text(text)
    if not t:
        return []
    toks = set(t.split())
    hits: list[str] = []
    for kw in keywords:
        k = _norm_text(str(kw or ""))
        if not k:
            continue
        if " " in k or any(ch in k for ch in ("&", "-", "/", ".")):
            if k in t:
                hits.append(str(kw))
        else:
            if k in toks:
                hits.append(str(kw))
    return sorted(set(hits))


@dataclass(frozen=True)
class DiscoveryCandidate:
    signal_family_id: int
    slug: str
    method: str  # discovery_lexical | discovery_embedding
    score: float
    evidence: dict[str, Any]


def lexical_discover(
    *,
    market_text: str,
    family: FamilyDescriptor,
    target_hits: int = 2,
) -> DiscoveryCandidate | None:
    t = _norm_text(market_text)
    if not t or not family.keywords:
        return None

    gate_hits: list[str] = []
    if getattr(family, "lexical_gates", None):
        gate_hits = _keyword_hits(t, family.lexical_gates)
        if not gate_hits:
            return None

    hits: list[str] = []
    # Speed trick: single-word keywords are checked via token set; phrases via substring.
    toks = set(t.split())
    for kw in family.keywords:
        k = _norm_text(kw)
        if not k:
            continue
        if " " in k or any(ch in k for ch in ("&", "-", "/", ".")):
            if k in t:
                hits.append(kw)
        else:
            if k in toks:
                hits.append(kw)

    if not hits:
        return None

    denom = max(1, int(target_hits))
    lexical_score = min(1.0, float(len(set(hits))) / float(denom))
    return DiscoveryCandidate(
        signal_family_id=family.signal_family_id,
        slug=family.slug,
        method="discovery_lexical",
        score=float(lexical_score),
        evidence={
            "matched_keywords": sorted(set(hits)),
            "hit_count": int(len(set(hits))),
            "target_hits": int(target_hits),
            "lexical_score": float(lexical_score),
            "lexical_gate_required": bool(getattr(family, "lexical_gates", None)),
            "lexical_gate_hits": gate_hits,
        },
    )


class EmbeddingProvider:
    name: str
    model_name: str

    def embed_texts(self, texts: list[str]) -> list[list[float]]:  # pragma: no cover
        raise NotImplementedError


class SentenceTransformersProvider(EmbeddingProvider):
    def __init__(self, *, model_name: str, device: str | None = None):
        self.name = "sentence_transformers"
        self.model_name = str(model_name)
        self._embedder = LocalSentenceTransformerEmbedder(model_name=self.model_name, device=device)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self._embedder.embed_texts(texts)


def _topk_cosine(
    market_vec: np.ndarray,
    family_matrix: np.ndarray,
    *,
    top_k: int,
) -> tuple[np.ndarray, np.ndarray]:
    # embeddings are normalized => cosine = dot
    sims = family_matrix @ market_vec
    k = max(1, int(top_k))
    if sims.shape[0] <= k:
        idx = np.argsort(-sims)
        return idx, sims[idx]
    idx = np.argpartition(-sims, k - 1)[:k]
    idx = idx[np.argsort(-sims[idx])]
    return idx, sims[idx]


def embedding_discover_topk(
    *,
    market_texts_by_id: dict[int, str],
    families: list[FamilyDescriptor],
    provider: EmbeddingProvider,
    db_url: str,
    top_k: int = 5,
    min_similarity: float = 0.40,
    batch_size: int = 256,
) -> dict[int, list[DiscoveryCandidate]]:
    """Return embedding discovery candidates per market_id."""
    if not market_texts_by_id:
        return {}
    if not families:
        return {}

    cache = DBEmbeddingCache(db_url=db_url)
    family_texts = [f.query_text for f in families]
    fam_cached = cache.get_many(model_name=provider.model_name, texts=family_texts)
    fam_vecs: list[list[float]] = []
    fam_missing_texts: list[str] = []
    fam_missing_idx: list[int] = []
    for i, t in enumerate(family_texts):
        k = cache.key(model_name=provider.model_name, text=t)
        if k in fam_cached:
            fam_vecs.append(fam_cached[k])
        else:
            fam_vecs.append([])
            fam_missing_texts.append(t)
            fam_missing_idx.append(i)

    if fam_missing_texts:
        new_vecs = provider.embed_texts(fam_missing_texts)
        cache.put_many(model_name=provider.model_name, texts=fam_missing_texts, embeddings=new_vecs)
        for idx, vec in zip(fam_missing_idx, new_vecs):
            fam_vecs[idx] = vec

    fam_matrix = np.array(fam_vecs, dtype=np.float32)
    # Ensure normalized; if provider didn't normalize, we normalize defensively.
    norms = np.linalg.norm(fam_matrix, axis=1, keepdims=True)
    fam_matrix = np.divide(fam_matrix, np.maximum(1e-9, norms))

    out: dict[int, list[DiscoveryCandidate]] = {mid: [] for mid in market_texts_by_id.keys()}
    market_ids = list(market_texts_by_id.keys())
    market_texts = [market_texts_by_id[mid] for mid in market_ids]

    for start in range(0, len(market_texts), int(batch_size)):
        chunk_texts = market_texts[start : start + int(batch_size)]
        chunk_ids = market_ids[start : start + int(batch_size)]

        cached = cache.get_many(model_name=provider.model_name, texts=chunk_texts)
        missing_texts: list[str] = []
        missing_pos: list[int] = []
        chunk_vecs: list[list[float] | None] = [None] * len(chunk_texts)
        for j, t in enumerate(chunk_texts):
            key = cache.key(model_name=provider.model_name, text=t)
            if key in cached:
                chunk_vecs[j] = cached[key]
            else:
                missing_texts.append(t)
                missing_pos.append(j)

        if missing_texts:
            new_vecs = provider.embed_texts(missing_texts)
            cache.put_many(model_name=provider.model_name, texts=missing_texts, embeddings=new_vecs)
            for pos, vec in zip(missing_pos, new_vecs):
                chunk_vecs[pos] = vec

        mat = np.array([v for v in chunk_vecs if v is not None], dtype=np.float32)
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        mat = np.divide(mat, np.maximum(1e-9, norms))

        for i, mid in enumerate(chunk_ids):
            mv = mat[i]
            idxs, sims = _topk_cosine(mv, fam_matrix, top_k=int(top_k))
            cands: list[DiscoveryCandidate] = []
            for rank, (fi, sim) in enumerate(zip(idxs.tolist(), sims.tolist()), start=1):
                if float(sim) < float(min_similarity):
                    continue
                f = families[int(fi)]
                gate_hits: list[str] = []
                if getattr(f, "embedding_gates", None):
                    gate_hits = _keyword_hits(market_texts_by_id.get(int(mid), ""), f.embedding_gates)
                    if not gate_hits:
                        continue
                cands.append(
                    DiscoveryCandidate(
                        signal_family_id=f.signal_family_id,
                        slug=f.slug,
                        method="discovery_embedding",
                        score=float(sim),
                        evidence={
                            "similarity": float(sim),
                            "min_similarity": float(min_similarity),
                            "rank": int(rank),
                            "top_k": int(top_k),
                            "provider": provider.name,
                            "model_name": provider.model_name,
                            "family_query_text_hash": f.query_text_hash,
                            "embedding_gate_required": bool(getattr(f, "embedding_gates", None)),
                            "embedding_gate_hits": gate_hits,
                        },
                    )
                )
            out[mid] = cands

    return out


def embedding_discover_topk_with_stats(
    *,
    market_texts_by_id: dict[int, str],
    families: list[FamilyDescriptor],
    provider: EmbeddingProvider,
    db_url: str,
    top_k: int = 5,
    min_similarity: float = 0.40,
    batch_size: int = 256,
) -> tuple[dict[int, list[DiscoveryCandidate]], dict[int, dict[str, Any]]]:
    """Embedding discovery + per-market threshold diagnostics.

    Returns:
      - candidates_by_market: filtered candidates (same semantics as embedding_discover_topk)
      - best_by_market: unfiltered top-1 stats per market:
          {
            "best_signal_family_id": int,
            "best_slug": str,
            "best_similarity": float,
            "top_k": int,
            "model_name": str,
          }

    Why this exists:
    - `pm_market_signal_family_match` only stores candidates above thresholds.
    - Without per-market "best similarity", it's hard to tell whether embeddings are broken
      vs thresholds are simply too strict.
    """
    if not market_texts_by_id:
        return {}, {}
    if not families:
        return {}, {}

    cache = DBEmbeddingCache(db_url=db_url)
    family_texts = [f.query_text for f in families]
    fam_cached = cache.get_many(model_name=provider.model_name, texts=family_texts)
    fam_vecs: list[list[float]] = []
    fam_missing_texts: list[str] = []
    fam_missing_idx: list[int] = []
    for i, t in enumerate(family_texts):
        k = cache.key(model_name=provider.model_name, text=t)
        if k in fam_cached:
            fam_vecs.append(fam_cached[k])
        else:
            fam_vecs.append([])
            fam_missing_texts.append(t)
            fam_missing_idx.append(i)

    if fam_missing_texts:
        new_vecs = provider.embed_texts(fam_missing_texts)
        cache.put_many(model_name=provider.model_name, texts=fam_missing_texts, embeddings=new_vecs)
        for idx, vec in zip(fam_missing_idx, new_vecs):
            fam_vecs[idx] = vec

    fam_matrix = np.array(fam_vecs, dtype=np.float32)
    norms = np.linalg.norm(fam_matrix, axis=1, keepdims=True)
    fam_matrix = np.divide(fam_matrix, np.maximum(1e-9, norms))

    out: dict[int, list[DiscoveryCandidate]] = {mid: [] for mid in market_texts_by_id.keys()}
    best: dict[int, dict[str, Any]] = {}

    market_ids = list(market_texts_by_id.keys())
    market_texts = [market_texts_by_id[mid] for mid in market_ids]

    for start in range(0, len(market_texts), int(batch_size)):
        chunk_texts = market_texts[start : start + int(batch_size)]
        chunk_ids = market_ids[start : start + int(batch_size)]

        cached = cache.get_many(model_name=provider.model_name, texts=chunk_texts)
        missing_texts: list[str] = []
        missing_pos: list[int] = []
        chunk_vecs: list[list[float] | None] = [None] * len(chunk_texts)
        for j, t in enumerate(chunk_texts):
            key = cache.key(model_name=provider.model_name, text=t)
            if key in cached:
                chunk_vecs[j] = cached[key]
            else:
                missing_texts.append(t)
                missing_pos.append(j)

        if missing_texts:
            new_vecs = provider.embed_texts(missing_texts)
            cache.put_many(model_name=provider.model_name, texts=missing_texts, embeddings=new_vecs)
            for pos, vec in zip(missing_pos, new_vecs):
                chunk_vecs[pos] = vec

        mat = np.array([v for v in chunk_vecs if v is not None], dtype=np.float32)
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        mat = np.divide(mat, np.maximum(1e-9, norms))

        for i, mid in enumerate(chunk_ids):
            mv = mat[i]
            idxs, sims = _topk_cosine(mv, fam_matrix, top_k=int(top_k))
            best_fi = int(idxs[0])
            best_sim = float(sims[0])
            best[mid] = {
                "best_signal_family_id": int(families[best_fi].signal_family_id),
                "best_slug": str(families[best_fi].slug),
                "best_similarity": float(best_sim),
                "top_k": int(top_k),
                "model_name": str(provider.model_name),
                "provider": str(provider.name),
            }

            cands: list[DiscoveryCandidate] = []
            for rank, (fi, sim) in enumerate(zip(idxs.tolist(), sims.tolist()), start=1):
                if float(sim) < float(min_similarity):
                    continue
                f = families[int(fi)]
                gate_hits: list[str] = []
                if getattr(f, "embedding_gates", None):
                    gate_hits = _keyword_hits(market_texts_by_id.get(int(mid), ""), f.embedding_gates)
                    if not gate_hits:
                        continue
                cands.append(
                    DiscoveryCandidate(
                        signal_family_id=f.signal_family_id,
                        slug=f.slug,
                        method="discovery_embedding",
                        score=float(sim),
                        evidence={
                            "similarity": float(sim),
                            "min_similarity": float(min_similarity),
                            "rank": int(rank),
                            "top_k": int(top_k),
                            "provider": provider.name,
                            "model_name": provider.model_name,
                            "family_query_text_hash": f.query_text_hash,
                            "embedding_gate_required": bool(getattr(f, "embedding_gates", None)),
                            "embedding_gate_hits": gate_hits,
                        },
                    )
                )
            out[mid] = cands

    return out, best
