"""Domain relevance scoring (MVP).

Primary path:
- sentence-transformers cosine similarity between market text and DB-backed domain definition text.

Fallback path:
- if sentence-transformers isn't installed, use the existing keyword ranker score
  (less semantic, but keeps the pipeline runnable).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from polyscanner.models import Domain, DomainDefinition, PMMarket
from polyscanner.relevance.keyword_ranker import score_market_against_domain


@dataclass(frozen=True)
class DomainScore:
    domain_id: int
    domain_name: str
    domain_relevance: float  # 0..1
    raw_similarity: float | None  # cosine similarity if embeddings are used


def _market_text(m: PMMarket) -> str:
    return f"{m.question} {m.category or ''}".strip()


def _load_model(*, model_name: str, device: str | None):
    from sentence_transformers import SentenceTransformer  # type: ignore

    return SentenceTransformer(model_name, device=device or "cpu")


def _embed(model, texts: list[str]) -> np.ndarray:
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return np.asarray(emb, dtype=np.float32)


@dataclass(frozen=True)
class EmbeddingDomainScorer:
    """Caches model + domain embeddings for fast per-market scoring."""

    domains: list[DomainDefinition]
    model_name: str = "all-MiniLM-L6-v2"
    device: str | None = None

    def __post_init__(self) -> None:  # type: ignore[override]
        object.__setattr__(self, "_model", _load_model(model_name=self.model_name, device=self.device))
        theme_texts = [d.to_theme_text() for d in self.domains]
        object.__setattr__(self, "_domain_emb", _embed(self._model, theme_texts))

    def score(self, market: PMMarket) -> list[DomainScore]:
        market_emb = _embed(self._model, [_market_text(market)])[0]
        sims = self._domain_emb @ market_emb
        out: list[DomainScore] = []
        for d, sim in zip(self.domains, sims, strict=True):
            rel = float(max(0.0, float(sim)))
            out.append(DomainScore(domain_id=d.id, domain_name=d.name, domain_relevance=rel, raw_similarity=float(sim)))
        out.sort(key=lambda x: x.domain_relevance, reverse=True)
        return out


def score_domains_with_embeddings(
    market: PMMarket,
    domains: list[DomainDefinition],
    *,
    model_name: str = "all-MiniLM-L6-v2",
    device: str | None = None,
) -> list[DomainScore]:
    """Return per-domain relevance scores based on cosine similarity."""
    scorer = EmbeddingDomainScorer(domains=domains, model_name=model_name, device=device)
    return scorer.score(market)


def score_domains_fallback_keyword(
    market: PMMarket,
    domains: list[Domain] | list[DomainDefinition],
) -> list[DomainScore]:
    """Fallback scorer using keyword ranker scores, normalized to [0,1] per market."""
    dom_objs: list[Domain] = []
    for d in domains:
        if isinstance(d, DomainDefinition):
            dom_objs.append(Domain(id=d.id, name=d.name))
        else:
            dom_objs.append(d)

    raw_scores = [(d, float(score_market_against_domain(market, d))) for d in dom_objs]
    max_s = max((s for _d, s in raw_scores), default=0.0)
    out: list[DomainScore] = []
    for d, s in raw_scores:
        rel = 0.0 if max_s <= 0 else float(s / max_s)
        out.append(DomainScore(domain_id=d.id, domain_name=d.name, domain_relevance=rel, raw_similarity=None))
    out.sort(key=lambda x: x.domain_relevance, reverse=True)
    return out


def score_domains(
    market: PMMarket,
    domains: list[DomainDefinition],
    *,
    prefer_embeddings: bool = True,
    model_name: str = "all-MiniLM-L6-v2",
    device: str | None = None,
    scorer: EmbeddingDomainScorer | None = None,
) -> list[DomainScore]:
    """Score domains for a market; tries embeddings then falls back to keywords."""
    if prefer_embeddings:
        try:
            if scorer is not None:
                return scorer.score(market)
            return score_domains_with_embeddings(market, domains, model_name=model_name, device=device)
        except Exception:
            pass
    return score_domains_fallback_keyword(market, domains)
