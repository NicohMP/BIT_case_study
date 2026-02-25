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
    embedding_gates: list[str]
    lexical_gates: list[str]
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


def load_family_embedding_gates(path: Path | None = None) -> dict[str, list[str]]:
    """Load optional embedding gating terms per family.

    If provided, embedding discovery candidates for that family will only be kept
    when the market text contains at least one of these terms.

    This is a precision control to reduce semantic drift for "broad" families
    (e.g., antitrust / export controls), without globally raising similarity
    thresholds.
    """
    p = path or DEFAULT_KEYWORDS_PATH
    cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg, dict):
        raise TypeError("family_keywords.yaml must be a mapping")

    families = cfg.get("families")
    if not isinstance(families, dict):
        return {}

    out: dict[str, list[str]] = {}
    for slug, node in families.items():
        if not isinstance(node, dict):
            continue
        gates_raw = node.get("embedding_gates") or []
        if not isinstance(gates_raw, list):
            continue
        gates: list[str] = []
        for g in gates_raw:
            if not isinstance(g, str):
                continue
            gg = g.strip()
            if gg:
                gates.append(gg)
        if gates:
            out[str(slug)] = gates
    return out


def load_family_lexical_gates(path: Path | None = None) -> dict[str, list[str]]:
    """Load optional lexical gating terms per family.

    If provided, lexical discovery candidates for that family will only be kept
    when the market text contains at least one of these terms.

    This is a precision control to prevent a single broad keyword (e.g., "nvidia")
    from nominating a family like "export controls" on unrelated markets (e.g.,
    compute pricing templates).
    """
    p = path or DEFAULT_KEYWORDS_PATH
    cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg, dict):
        raise TypeError("family_keywords.yaml must be a mapping")

    families = cfg.get("families")
    if not isinstance(families, dict):
        return {}

    out: dict[str, list[str]] = {}
    for slug, node in families.items():
        if not isinstance(node, dict):
            continue
        gates_raw = node.get("lexical_gates") or []
        if not isinstance(gates_raw, list):
            continue
        gates: list[str] = []
        for g in gates_raw:
            if not isinstance(g, str):
                continue
            gg = g.strip()
            if gg:
                gates.append(gg)
        if gates:
            out[str(slug)] = gates
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
    embedding_gates_by_slug: dict[str, list[str]] | None = None,
    lexical_gates_by_slug: dict[str, list[str]] | None = None,
) -> list[FamilyDescriptor]:
    kws = keywords_by_slug or load_family_keywords()
    gates_by_slug = embedding_gates_by_slug or {}
    lex_gates_by_slug = lexical_gates_by_slug or {}
    out: list[FamilyDescriptor] = []
    for sf in signal_families:
        sf_id = int(sf["id"])
        slug = str(sf["slug"])
        title = str(sf.get("title") or "")
        description = str(sf.get("description") or "")
        keywords = kws.get(slug, [])
        embedding_gates = gates_by_slug.get(slug, [])
        lexical_gates = lex_gates_by_slug.get(slug, [])
        qt = build_family_query_text(title=title, description=description, keywords=keywords)
        out.append(
            FamilyDescriptor(
                signal_family_id=sf_id,
                slug=slug,
                title=title,
                description=description,
                keywords=keywords,
                embedding_gates=embedding_gates,
                lexical_gates=lexical_gates,
                query_text=qt,
                query_text_hash=_sha256_hex(qt),
            )
        )
    return out
