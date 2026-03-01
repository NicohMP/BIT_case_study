"""Audit / grounding checks for Step 5 security signal reports.

This is *not* a quality judge; it is a "lint" layer to catch common failure modes:
- report references markets not present in the context pack
- evidence_refs do not resolve
- duplicate event_id flooding
- rate-like over-concentration
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


@dataclass(frozen=True)
class AuditIssue:
    level: str  # "error" | "warning"
    message: str
    path: str | None = None


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)

_LEAK_PATTERNS = [
    re.compile(r"\bbase score\b", re.IGNORECASE),
    re.compile(r"\bmarket strength\b", re.IGNORECASE),
    re.compile(r"\bfinal score\b", re.IGNORECASE),
    re.compile(r"\bquality multiplier\b", re.IGNORECASE),
    re.compile(r"\b\d+\.\d{3,}\b"),  # long decimals like 0.771428...
]


def _mentions_internal_numbers(text: Any) -> bool:
    if not isinstance(text, str):
        return False
    t = text.strip()
    if not t:
        return False
    return any(p.search(t) for p in _LEAK_PATTERNS)


def audit_security_signal_report(
    *,
    report: dict[str, Any],
    pack: dict[str, Any],
    max_markets: int = 10,
    max_rate_like: int = 3,
) -> list[AuditIssue]:
    issues: list[AuditIssue] = []

    def err(msg: str, path: str | None = None) -> None:
        issues.append(AuditIssue(level="error", message=msg, path=path))

    def warn(msg: str, path: str | None = None) -> None:
        issues.append(AuditIssue(level="warning", message=msg, path=path))

    pack_markets = pack.get("markets") or []
    pack_market_by_id: dict[int, dict[str, Any]] = {}
    for m in pack_markets:
        if isinstance(m, dict) and m.get("market_id") is not None:
            try:
                pack_market_by_id[int(m["market_id"])] = m
            except Exception:
                continue

    pack_family_ids: set[int] = set()
    for f in pack.get("signal_families") or []:
        if isinstance(f, dict) and f.get("id") is not None:
            try:
                pack_family_ids.add(int(f["id"]))
            except Exception:
                continue

    pack_domain_ids: set[int] = set()
    for d in pack.get("exposure_vector") or []:
        if isinstance(d, dict) and d.get("macro_domain_id") is not None:
            try:
                pack_domain_ids.add(int(d["macro_domain_id"]))
            except Exception:
                continue

    influence_edges: set[tuple[int, int]] = set()
    for e in pack.get("influence_matrix_slice") or []:
        if not isinstance(e, dict):
            continue
        fid = e.get("signal_family_id")
        did = e.get("macro_domain_id")
        if fid is None or did is None:
            continue
        try:
            influence_edges.add((int(fid), int(did)))
        except Exception:
            continue

    top = report.get("top_markets")
    if not isinstance(top, list):
        err("report.top_markets must be a list", path="top_markets")
        return issues

    if len(top) > int(max_markets):
        warn(f"top_markets has {len(top)} items (> max_markets={max_markets})", path="top_markets")

    # Narrative hygiene: the report is meant to be PM-readable; keep internal numeric score talk out of prose.
    if _mentions_internal_numbers(report.get("top_take")):
        warn("top_take mentions internal numeric scores; prefer buckets/labels", path="top_take")

    # Duplicate event check + rate-like cap check
    seen_event_ids: set[int] = set()
    rate_like_count = 0

    for i, it in enumerate(top[:100]):
        if not isinstance(it, dict):
            err("top_markets items must be objects", path=f"top_markets[{i}]")
            continue
        mid = it.get("market_id")
        if mid is None:
            err("missing market_id", path=f"top_markets[{i}].market_id")
            continue
        try:
            mid_i = int(mid)
        except Exception:
            err("market_id must be int", path=f"top_markets[{i}].market_id")
            continue
        if mid_i not in pack_market_by_id:
            err("market_id not in context pack", path=f"top_markets[{i}].market_id")
            continue

        pm = pack_market_by_id[mid_i]
        ev = it.get("event_id", pm.get("event_id"))
        if ev is not None:
            try:
                ev_i = int(ev)
                if ev_i in seen_event_ids:
                    warn("duplicate event_id in top_markets (should be at most one per event)", path=f"top_markets[{i}].event_id")
                seen_event_ids.add(ev_i)
            except Exception:
                warn("event_id not int", path=f"top_markets[{i}].event_id")

        is_rate = bool(pm.get("is_rate_like"))
        if is_rate:
            rate_like_count += 1

        # Evidence refs resolution.
        evrefs = it.get("evidence_refs")
        if evrefs is None:
            warn("missing evidence_refs", path=f"top_markets[{i}].evidence_refs")
            continue
        if not isinstance(evrefs, list):
            err("evidence_refs must be a list", path=f"top_markets[{i}].evidence_refs")
            continue

        for j, ref in enumerate(evrefs[:50]):
            if not isinstance(ref, dict):
                err("evidence_refs items must be objects", path=f"top_markets[{i}].evidence_refs[{j}]")
                continue
            kind = ref.get("kind")
            if kind not in {"market", "family_match", "influence_edge", "security_exposure"}:
                warn("unknown evidence_refs kind", path=f"top_markets[{i}].evidence_refs[{j}].kind")
                continue
            if kind in {"market", "family_match"}:
                rid = ref.get("market_id")
                if rid is None:
                    err("evidence ref missing market_id", path=f"top_markets[{i}].evidence_refs[{j}].market_id")
                else:
                    try:
                        if int(rid) not in pack_market_by_id:
                            err("evidence ref market_id not in pack", path=f"top_markets[{i}].evidence_refs[{j}].market_id")
                    except Exception:
                        err("evidence ref market_id not int", path=f"top_markets[{i}].evidence_refs[{j}].market_id")
            if kind in {"family_match", "influence_edge"}:
                fid = ref.get("signal_family_id")
                if fid is None:
                    err("evidence ref missing signal_family_id", path=f"top_markets[{i}].evidence_refs[{j}].signal_family_id")
                else:
                    try:
                        if int(fid) not in pack_family_ids:
                            err("evidence ref signal_family_id not in pack", path=f"top_markets[{i}].evidence_refs[{j}].signal_family_id")
                    except Exception:
                        err("evidence ref signal_family_id not int", path=f"top_markets[{i}].evidence_refs[{j}].signal_family_id")
            if kind in {"influence_edge", "security_exposure"}:
                did = ref.get("macro_domain_id")
                if did is None:
                    err("evidence ref missing macro_domain_id", path=f"top_markets[{i}].evidence_refs[{j}].macro_domain_id")
                else:
                    try:
                        did_i = int(did)
                        if did_i not in pack_domain_ids:
                            err("evidence ref macro_domain_id not in pack exposure_vector", path=f"top_markets[{i}].evidence_refs[{j}].macro_domain_id")
                        if kind == "influence_edge":
                            fid = ref.get("signal_family_id")
                            if fid is not None:
                                try:
                                    edge = (int(fid), did_i)
                                    if edge not in influence_edges:
                                        warn(
                                            "influence_edge does not exist in influence_matrix_slice",
                                            path=f"top_markets[{i}].evidence_refs[{j}]",
                                        )
                                except Exception:
                                    pass
                    except Exception:
                        err("evidence ref macro_domain_id not int", path=f"top_markets[{i}].evidence_refs[{j}].macro_domain_id")

        if _mentions_internal_numbers(it.get("structural_relevance")):
            warn("structural_relevance mentions internal numeric scores; prefer buckets/labels", path=f"top_markets[{i}].structural_relevance")
        if _mentions_internal_numbers(it.get("actionability")):
            warn("actionability mentions internal numeric scores; prefer buckets/labels", path=f"top_markets[{i}].actionability")

    themes = report.get("themes") or []
    if isinstance(themes, list):
        for i, t in enumerate(themes[:20]):
            if not isinstance(t, dict):
                continue
            if _mentions_internal_numbers(t.get("why")):
                warn("themes.why mentions internal numeric scores; prefer buckets/labels", path=f"themes[{i}].why")

    if rate_like_count > int(max_rate_like):
        warn(f"selected {rate_like_count} rate-like markets (> max_rate_like={max_rate_like})", path="top_markets")

    return issues


def render_security_signal_report_audit_markdown(
    *,
    issues: list[AuditIssue],
    title: str = "Security Signal Report Audit",
) -> str:
    lines: list[str] = [f"# {title}", ""]
    if not issues:
        lines.append("✅ No issues found.")
        lines.append("")
        return "\n".join(lines)

    errs = [x for x in issues if x.level == "error"]
    warns = [x for x in issues if x.level == "warning"]

    if errs:
        lines.append("## Errors")
        for e in errs:
            loc = f" ({e.path})" if e.path else ""
            lines.append(f"- {e.message}{loc}")
        lines.append("")

    if warns:
        lines.append("## Warnings")
        for w in warns:
            loc = f" ({w.path})" if w.path else ""
            lines.append(f"- {w.message}{loc}")
        lines.append("")

    return "\n".join(lines)
