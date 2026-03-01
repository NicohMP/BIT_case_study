"""Embeddings utilities for Step 3 (local sentence-transformers + DB cache).

This module is intentionally lightweight at import-time:
- sentence-transformers (and torch) are imported only when the embedder is constructed.
- Embeddings are cached in Postgres (`pm_text_embedding_cache`) as jsonb arrays.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from polyscanner.db.pg import connect

try:
    from psycopg.types.json import Jsonb  # type: ignore
except Exception:  # pragma: no cover
    Jsonb = None  # type: ignore[assignment]


def _jsonb(v: Any) -> Any:
    return Jsonb(v) if Jsonb is not None else v


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class LocalSentenceTransformerEmbedder:
    """Local sentence-transformers embedder with normalized outputs.

    Normalized vectors make cosine similarity equal to a dot product.
    """

    name = "sentence_transformers"

    def __init__(self, *, model_name: str, device: str | None = None, batch_size: int = 256):
        from sentence_transformers import SentenceTransformer  # type: ignore

        self.model_name = str(model_name)
        self.device = device
        self.batch_size = int(batch_size)
        self._model = SentenceTransformer(self.model_name, device=device)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vecs = self._model.encode(
            texts,
            batch_size=int(self.batch_size),
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        if hasattr(vecs, "tolist"):
            return vecs.tolist()
        return [list(map(float, v)) for v in vecs]


class DBEmbeddingCache:
    """DB-backed embedding cache (jsonb arrays).

    Storage key: sha256(model_name + '\\0' + text)
    """

    def __init__(self, *, db_url: str):
        self.db_url = db_url

    def key(self, *, model_name: str, text: str) -> str:
        return sha256_hex(str(model_name) + "\0" + str(text))

    def get_many(self, *, model_name: str, texts: list[str]) -> dict[str, list[float]]:
        if not texts:
            return {}
        keys = [self.key(model_name=model_name, text=t) for t in texts]
        conn = connect(self.db_url)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    select text_hash, embedding
                    from pm_text_embedding_cache
                    where text_hash = any(%s);
                    """,
                    (keys,),
                )
                rows = cur.fetchall()
            out: dict[str, list[float]] = {}
            for h, emb in rows:
                if isinstance(emb, list):
                    out[str(h)] = [float(x) for x in emb]
                elif isinstance(emb, str):
                    try:
                        parsed = json.loads(emb)
                        if isinstance(parsed, list):
                            out[str(h)] = [float(x) for x in parsed]
                    except Exception:
                        continue
            return out
        finally:
            conn.close()

    def put_many(self, *, model_name: str, texts: list[str], embeddings: list[list[float]]) -> None:
        if not texts:
            return
        conn = connect(self.db_url)
        try:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    insert into pm_text_embedding_cache (text_hash, text, model_name, embedding, created_at)
                    values (%(text_hash)s, %(text)s, %(model_name)s, %(embedding)s, now())
                    on conflict (text_hash) do nothing;
                    """,
                    [
                        {
                            "text_hash": self.key(model_name=model_name, text=t),
                            "text": t,
                            "model_name": str(model_name),
                            "embedding": _jsonb(e),
                        }
                        for t, e in zip(texts, embeddings)
                    ],
                )
            conn.commit()
        finally:
            conn.close()

