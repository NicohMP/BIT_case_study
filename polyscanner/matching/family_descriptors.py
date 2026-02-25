"""Family descriptors for Step-3 discovery.

We build a canonical "family query text" that is used by discovery:
- lexical: keywords list
- semantic: embedding of the family descriptor text
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_KEYWORDS_PATH = Path(__file__).resolve().parent / "family_keywords.yaml"


@dataclass(frozen=True)
class FamilyDescriptor:
    signal_family_id: int
    slug: str
    title: str
    description: str
    keywords: list[str]
    query_text: str
    query_text_hash: str


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_family_keywords(path: Path | None = None) -> dict[str, list[str]]:
    p = path or DEFAULT_KEYWORDS_PATH
    cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg, dict):
        raise TypeError("family_keywords.yaml must be a mapping")

    # Newer format:
    # families:
    #   <slug>:
    #     keywords: [...]
    #     synonyms: [...]
    families = cfg.get("families")
    if isinstance(families, dict):
        out: dict[str, list[str]] = {}
        for slug, node in families.items():
            if not isinstance(node, dict):
                continue
            kws_raw = node.get("keywords") or []
            syn_raw = node.get("synonyms") or []
            merged: list[str] = []
            for seq in (kws_raw, syn_raw):
                if not isinstance(seq, list):
                    continue
                for k in seq:
                    if not isinstance(k, str):
                        continue
                    kk = k.strip()
                    if kk:
                        merged.append(kk)
            if merged:
                out[str(slug)] = merged
        return out

    # Back-compat format: <slug>: [keywords...]
    out: dict[str, list[str]] = {}
    for slug, kws in cfg.items():
        if not isinstance(kws, list):
            continue
        cleaned = []
        for k in kws:
            if not isinstance(k, str):
                continue
            kk = k.strip()
            if kk:
                cleaned.append(kk)
        out[str(slug)] = cleaned
    return out


def build_family_query_text(*, title: str, description: str, keywords: list[str]) -> str:
    desc = (description or "").strip()
    kw = ", ".join([k.strip() for k in keywords if isinstance(k, str) and k.strip()])
    parts = [title.strip()]
    if desc:
        parts.append(desc)
    if kw:
        parts.append(f"Keywords: {kw}.")
    return " ".join([p for p in parts if p]).strip()


def build_family_descriptors(
    *,
    signal_families: list[dict[str, Any]],
    keywords_by_slug: dict[str, list[str]] | None = None,
) -> list[FamilyDescriptor]:
    kws = keywords_by_slug or load_family_keywords()
    out: list[FamilyDescriptor] = []
    for sf in signal_families:
        sf_id = int(sf["id"])
        slug = str(sf["slug"])
        title = str(sf.get("title") or "")
        description = str(sf.get("description") or "")
        keywords = kws.get(slug, [])
        qt = build_family_query_text(title=title, description=description, keywords=keywords)
        out.append(
            FamilyDescriptor(
                signal_family_id=sf_id,
                slug=slug,
                title=title,
                description=description,
                keywords=keywords,
                query_text=qt,
                query_text_hash=_sha256_hex(qt),
            )
        )
    return out
