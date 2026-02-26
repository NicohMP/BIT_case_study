"""Validation helpers for LLM context packs and report JSON.

These are lightweight checks intended to fail fast before/after LLM calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValidationIssue:
    level: str  # "error" | "warning"
    message: str
    path: str | None = None


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_context_pack(pack: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def err(msg: str, path: str | None = None) -> None:
        issues.append(ValidationIssue(level="error", message=msg, path=path))

    def warn(msg: str, path: str | None = None) -> None:
        issues.append(ValidationIssue(level="warning", message=msg, path=path))

    if not isinstance(pack, dict):
        err("pack must be a JSON object")
        return issues

    for k in ("report_meta", "security", "exposure_vector", "signal_families", "influence_matrix_slice", "markets"):
        if k not in pack:
            err(f"missing required key: {k}", path=k)

    sec = pack.get("security")
    if isinstance(sec, dict):
        for k in ("security_id", "ticker", "company_name"):
            if k not in sec:
                err(f"security missing {k}", path=f"security.{k}")

    exp = pack.get("exposure_vector")
    if isinstance(exp, list) and exp:
        wsum = 0.0
        for i, it in enumerate(exp):
            if not isinstance(it, dict):
                err("exposure_vector items must be objects", path=f"exposure_vector[{i}]")
                continue
            w = it.get("weight")
            if not _is_number(w):
                err("exposure weight must be numeric", path=f"exposure_vector[{i}].weight")
                continue
            wsum += float(w)
        if abs(wsum - 1.0) > 0.02:
            warn(f"exposure weights sum to {wsum:.3f} (expected ~1.0)", path="exposure_vector")
    else:
        err("exposure_vector is empty", path="exposure_vector")

    mkts = pack.get("markets")
    if not isinstance(mkts, list) or not mkts:
        err("markets must be a non-empty list", path="markets")
    else:
        for i, m in enumerate(mkts[:200]):
            if not isinstance(m, dict):
                err("market must be an object", path=f"markets[{i}]")
                continue
            if m.get("market_id") is None:
                err("market missing market_id", path=f"markets[{i}].market_id")
            if "market_card" not in m or not isinstance(m.get("market_card"), dict):
                err("market missing market_card (rebuild context pack)", path=f"markets[{i}].market_card")
            if "buckets" not in m or not isinstance(m.get("buckets"), dict):
                err("market missing buckets (rebuild context pack)", path=f"markets[{i}].buckets")
            scores = m.get("scores")
            if not isinstance(scores, dict):
                err("market missing scores object", path=f"markets[{i}].scores")
                continue
            for k in ("final_score", "base_score", "quality_multiplier", "market_strength"):
                if k not in scores:
                    err(f"market scores missing {k}", path=f"markets[{i}].scores.{k}")
                elif not _is_number(scores.get(k)):
                    err(f"market score {k} must be numeric", path=f"markets[{i}].scores.{k}")

    return issues


def validate_security_report_json(report: dict[str, Any], *, pack: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def err(msg: str, path: str | None = None) -> None:
        issues.append(ValidationIssue(level="error", message=msg, path=path))

    def warn(msg: str, path: str | None = None) -> None:
        issues.append(ValidationIssue(level="warning", message=msg, path=path))

    if not isinstance(report, dict):
        err("report must be a JSON object")
        return issues

    for k in ("as_of_utc", "security", "top_markets", "themes", "monitor_next"):
        if k not in report:
            err(f"missing required key: {k}", path=k)

    tt = report.get("top_take")
    if tt is None:
        warn("missing top_take (PM-readable synthesis)", path="top_take")
    elif not isinstance(tt, str) or not tt.strip():
        warn("top_take is empty", path="top_take")

    versions = report.get("versions")
    if not isinstance(versions, dict):
        warn("missing versions object", path="versions")
    else:
        pv = versions.get("prompt_version")
        model = versions.get("model")
        if not pv or str(pv).strip().lower() in {"string", "unknown", "none"}:
            warn("versions.prompt_version looks unset", path="versions.prompt_version")
        if not model or str(model).strip().lower() in {"string", "unknown", "none"}:
            warn("versions.model looks unset", path="versions.model")

    # Ensure selected market ids are from pack candidates.
    pack_market_ids = set()
    for m in pack.get("markets") or []:
        if isinstance(m, dict) and m.get("market_id") is not None:
            pack_market_ids.add(int(m["market_id"]))

    top = report.get("top_markets")
    if isinstance(top, list):
        for i, it in enumerate(top[:50]):
            if not isinstance(it, dict):
                err("top_markets items must be objects", path=f"top_markets[{i}]")
                continue
            mid = it.get("market_id")
            if mid is None:
                err("top_markets item missing market_id", path=f"top_markets[{i}].market_id")
                continue
            if int(mid) not in pack_market_ids:
                err("top_markets market_id not in context pack", path=f"top_markets[{i}].market_id")
            ev = it.get("evidence_refs")
            if ev is None:
                warn("missing evidence_refs (grounding)", path=f"top_markets[{i}].evidence_refs")

    return issues
