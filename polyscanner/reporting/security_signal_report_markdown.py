"""Markdown rendering for Step 5 security signal reports (LLM JSON).

Design goal:
- PM skim first (narrative paragraphs + buckets, minimal numbers)
- Analyst drill-down later (appendix with raw metrics + ids + evidence)
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from typing import Any


def _fmt_usd(x: Any) -> str | None:
    try:
        v = float(x)
    except Exception:
        return None
    if v >= 1_000_000_000:
        return f"${v/1_000_000_000:.2f}B"
    if v >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"${v/1_000:.1f}k"
    return f"${v:.0f}"


def _fmt_pct(x: Any) -> str | None:
    try:
        v = float(x)
    except Exception:
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    if 0.0 <= v <= 1.0:
        return f"{v*100:.0f}%"
    return f"{v:.0f}%"


def _parse_dt(iso: Any) -> datetime | None:
    if not iso:
        return None
    try:
        s = str(iso).replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _days_to(end_iso: Any, *, now: datetime) -> int | None:
    dt = _parse_dt(end_iso)
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = (dt - now).total_seconds()
    return int(delta // 86400)


def _bucket(v: Any, *, hi: float, mid: float) -> str:
    try:
        x = float(v)
    except Exception:
        return "Unknown"
    if x >= hi:
        return "High"
    if x >= mid:
        return "Medium"
    return "Low"

def _clean_items(items: Any, *, max_n: int) -> list[str]:
    if not isinstance(items, list):
        return []
    out: list[str] = []
    for it in items:
        if it is None:
            continue
        s = str(it).strip()
        s = s.rstrip().rstrip(".;").strip()
        if not s:
            continue
        out.append(s)
        if len(out) >= max(1, int(max_n)):
            break
    return out


def _join_semicolons(items: Any, *, max_n: int) -> str | None:
    parts = _clean_items(items, max_n=max_n)
    if not parts:
        return None
    s = "; ".join(parts)
    if not s.endswith((".", "!", "?")):
        s += "."
    return s


def _top_domains_for_market(market: dict[str, Any], *, k: int = 2) -> list[dict[str, Any]]:
    chain = market.get("transmission_chain") or []
    if not isinstance(chain, list) or not chain:
        return []
    first = chain[0] if isinstance(chain[0], dict) else None
    if not isinstance(first, dict):
        return []
    doms = first.get("domains") or []
    if not isinstance(doms, list):
        return []

    scored: list[tuple[float, dict[str, Any]]] = []
    for d in doms:
        if not isinstance(d, dict):
            continue
        infl = d.get("family_influence_score")
        expw = d.get("security_exposure_weight")
        try:
            score = float(infl) * float(expw)
        except Exception:
            score = 0.0
        scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[: max(1, int(k))] if isinstance(d, dict)]


def render_security_signal_report_markdown(*, report: dict[str, Any]) -> str:
    title = str(report.get("title") or "Security Signal Report")
    now = datetime.now(tz=timezone.utc)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    as_of = report.get("as_of_utc")
    if as_of:
        lines.append(f"_As of_: `{as_of}`")

    versions = report.get("versions") or {}
    if isinstance(versions, dict) and versions:
        fv = versions.get("filter_version")
        mv = versions.get("matcher_version")
        sv = versions.get("scoring_version")
        selv = versions.get("selection_version")
        pv = versions.get("prompt_version")
        model = versions.get("model")
        parts: list[str] = []
        if fv:
            parts.append(f"filter `{fv}`")
        if mv:
            parts.append(f"matcher `{mv}`")
        if sv:
            parts.append(f"scoring `{sv}`")
        if selv:
            parts.append(f"selection `{selv}`")
        if pv:
            parts.append(f"prompt `{pv}`")
        if model:
            parts.append(f"model `{model}`")
        if parts:
            lines.append(f"_Pipeline_: " + ", ".join(parts))

        run_id = versions.get("run_id")
        if run_id:
            lines.append("")
            lines.append("<details>")
            lines.append("<summary>Run metadata</summary>")
            lines.append("")
            lines.append(f"- run_id: `{run_id}`")
            lines.append("</details>")
            lines.append("")

    sec = report.get("security") or {}
    if isinstance(sec, dict) and sec:
        ticker = sec.get("ticker") or "SEC"
        company = sec.get("company_name") or ""
        mic = sec.get("exchange_mic") or ""
        head = f"**Security:** `{ticker}`"
        if company:
            head += f" — {company}"
        if mic:
            head += f" ({mic})"
        lines.append(head)
    lines.append("")

    top = report.get("top_markets") or []

    # Compute dynamic bucket thresholds for structural relevance (base_score) from the report's selected markets.
    base_scores: list[float] = []
    for m in top if isinstance(top, list) else []:
        if not isinstance(m, dict):
            continue
        scores = m.get("scores") or {}
        if not isinstance(scores, dict):
            continue
        try:
            base_scores.append(float(scores.get("base_score")))
        except Exception:
            continue
    base_scores.sort()
    if base_scores:
        p33 = base_scores[max(0, int(len(base_scores) * 0.33) - 1)]
        p66 = base_scores[max(0, int(len(base_scores) * 0.66) - 1)]
    else:
        p33, p66 = 0.45, 0.65

    lines.append("## Executive Summary")
    if not isinstance(top, list) or not top:
        lines.append("_No markets selected._")
        lines.append("")
    else:
        top_take = str(report.get("top_take") or "").strip()
        if top_take:
            lines.append(top_take)
            lines.append("")

        bits: list[str] = []
        for m in top[:5]:
            if not isinstance(m, dict):
                continue
            q = str(m.get("question") or "(no question)")
            scores = m.get("scores") or {}
            act = _bucket((scores.get("market_strength") if isinstance(scores, dict) else None), hi=0.75, mid=0.5)
            mag = m.get("magnitude_bucket") or "Unknown"
            tl = m.get("timeline_bucket") or "Unknown"
            bits.append(f"**{q}** (magnitude: {mag}; timeline: {tl}; actionability: {act})")
        if bits:
            lines.append("Top signals: " + "; ".join(bits) + ".")
            lines.append("")

    lines.append("## Top Signals")
    if not isinstance(top, list) or not top:
        lines.append("")
        lines.append("_No markets selected._")
        lines.append("")
    else:
        for i, m in enumerate(top[:8], start=1):
            if not isinstance(m, dict):
                continue
            q = m.get("question") or "(no question)"
            lines.append(f"### {i}) {q}")
            lines.append("")

            event_title = m.get("event_title")
            if event_title and str(event_title).strip() and str(event_title).strip() != str(q).strip():
                lines.append(f"**Event:** {event_title}")

            prob = _fmt_pct(m.get("probability"))
            if prob:
                lines.append(f"**Current probability:** {prob}")
            else:
                pricing = m.get("pricing") or {}
                if isinstance(pricing, dict):
                    if pricing.get("kind") == "multi_outcome":
                        tops = pricing.get("top_outcomes") or []
                        if isinstance(tops, list) and tops:
                            t0 = tops[0] if isinstance(tops[0], dict) else None
                            if isinstance(t0, dict) and t0.get("outcome") and t0.get("probability") is not None:
                                p0 = _fmt_pct(t0.get("probability"))
                                if p0:
                                    lines.append(f"**Pricing:** leading outcome “{t0.get('outcome')}” at {p0}")
                    elif pricing.get("kind") == "binary" and pricing.get("yes_probability") is not None:
                        p = _fmt_pct(pricing.get("yes_probability"))
                        if p:
                            lines.append(f"**Pricing:** Yes {p}")

            end_iso = m.get("end_date")
            dleft = _days_to(end_iso, now=now) if end_iso else None

            vol = _fmt_usd(m.get("volume_usd"))
            liq = _fmt_usd(m.get("liquidity_usd"))

            scores = m.get("scores") or {}
            base = scores.get("base_score") if isinstance(scores, dict) else None
            strength = scores.get("market_strength") if isinstance(scores, dict) else None
            structural_bucket = _bucket(base, hi=float(p66), mid=float(p33))
            action_bucket = _bucket(strength, hi=0.75, mid=0.5)
            conf_bucket = _bucket(m.get("confidence"), hi=0.67, mid=0.45)
            mb = m.get("magnitude_bucket") or "Unknown"
            tb = m.get("timeline_bucket") or "Unknown"

            snap_parts: list[str] = []
            if end_iso:
                if dleft is None:
                    snap_parts.append(f"resolves `{end_iso}`")
                else:
                    snap_parts.append(f"resolves `{end_iso}` ({dleft}d)")
            if vol:
                snap_parts.append(f"volume {vol}")
            if liq:
                snap_parts.append(f"liquidity {liq}")
            snap_parts.append(f"structural relevance {structural_bucket}")
            snap_parts.append(f"actionability {action_bucket}")
            snap_parts.append(f"confidence {conf_bucket}")
            snap_parts.append(f"magnitude {mb}")
            snap_parts.append(f"timeline {tb}")
            lines.append("_Snapshot:_ " + "; ".join(snap_parts) + ".")
            lines.append("")

            if m.get("structural_relevance"):
                lines.append(f"**Why it matters.** {m.get('structural_relevance')}")
            if m.get("actionability"):
                lines.append(f"**Why now.** {m.get('actionability')}")
            lines.append("")

            chain = m.get("transmission_chain") or []
            if isinstance(chain, list) and chain:
                c0 = chain[0] if isinstance(chain[0], dict) else None
                if isinstance(c0, dict):
                    fam_title = c0.get("title") or c0.get("slug") or c0.get("signal_family_id") or "signal family"
                    lines.append(f"**Transmission chain.** Market → **{fam_title}** → macro domains → `{sec.get('ticker')}`.")
                    lines.append("")

                    top_doms = _top_domains_for_market(m, k=2)
                    for d in top_doms:
                        dn = d.get("macro_domain_name") or d.get("macro_domain_id") or "domain"
                        infl = d.get("family_influence_score")
                        infl_bucket = _bucket(infl, hi=4.0, mid=2.0)
                        exp = _fmt_pct(d.get("security_exposure_weight"))
                        hdr = f"**{dn}** — influence: {infl_bucket}"
                        if exp:
                            hdr += f"; exposure: {exp}"
                        lines.append(f"> {hdr}")
                        er = (d.get("edge_rationale") or "").strip()
                        if er:
                            lines.append(f"> _Influence rationale:_ {er}")
                        xr = (d.get("exposure_rationale") or "").strip()
                        if xr:
                            lines.append(f"> _Exposure rationale:_ {xr}")
                        lines.append(">")
                    lines.append("")

            wtw_s = _join_semicolons(m.get("what_to_watch"), max_n=6)
            if wtw_s:
                lines.append(f"**What to watch.** {wtw_s}")

            unk_s = _join_semicolons(m.get("key_unknowns"), max_n=4)
            if unk_s:
                lines.append(f"**Key unknowns.** {unk_s}")

            mid = m.get("market_id")
            eid = m.get("event_id")
            if mid is not None or eid is not None:
                parts = []
                if mid is not None:
                    parts.append(f"market_id={mid}")
                if eid is not None:
                    parts.append(f"event_id={eid}")
                lines.append(f"_IDs:_ `{', '.join(parts)}`")

            lines.append("")
            lines.append("---")
            lines.append("")

    themes = report.get("themes") or []
    if isinstance(themes, list) and themes:
        lines.append("## Themes")
        lines.append("")
        for t in themes[:10]:
            if not isinstance(t, dict):
                continue
            tt = str(t.get("title") or "").strip()
            why = str(t.get("why") or "").strip()
            mids = t.get("market_ids") or []
            suffix = ""
            if isinstance(mids, list) and mids:
                suffix = f" (markets: {', '.join(str(x) for x in mids[:10])})"
            if tt and why:
                lines.append(f"**{tt}.** {why}{suffix}")
                lines.append("")

    monitor = report.get("monitor_next") or []
    if isinstance(monitor, list) and monitor:
        lines.append("## What To Monitor Next")
        s = _join_semicolons(monitor, max_n=25)
        if s:
            lines.append(s)
        lines.append("")

    notes = report.get("notes") or []
    if isinstance(notes, list) and notes:
        lines.append("## Notes")
        s = _join_semicolons(notes, max_n=25)
        if s:
            lines.append(s)
        lines.append("")

    exclusions = report.get("exclusions") or {}
    if isinstance(exclusions, dict) and exclusions:
        lines.append("## Appendix: Evidence & Metrics")
        lines.append("")

        # Raw metrics table
        lines.append("### Metrics (raw)")
        lines.append("| market_id | event_id | final_score | base_score | quality_mult | market_strength | confidence |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|")
        for m in top[:50] if isinstance(top, list) else []:
            if not isinstance(m, dict):
                continue
            scores = m.get("scores") or {}
            if not isinstance(scores, dict):
                scores = {}
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(m.get("market_id")),
                        str(m.get("event_id")),
                        str(scores.get("final_score")),
                        str(scores.get("base_score")),
                        str(scores.get("quality_multiplier")),
                        str(scores.get("market_strength")),
                        str(m.get("confidence")),
                    ]
                )
                + " |"
            )
        lines.append("")

        # Exclusions summary
        lines.append("### Exclusions")
        for k in ("dropped_due_to_duplicate_event", "dropped_due_to_rate_cap", "dropped_due_to_low_actionability"):
            items = exclusions.get(k) or []
            if not isinstance(items, list) or not items:
                continue
            lines.append(f"- {k}:")
            for it in items[:30]:
                if not isinstance(it, dict):
                    continue
                mid = it.get("market_id")
                reason = it.get("reason") or ""
                lines.append(f"  - {mid}: {reason}".rstrip())
        lines.append("")

    lines.append("<details>")
    lines.append("<summary>Raw LLM JSON</summary>")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(report, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("</details>")
    lines.append("")
    return "\n".join(lines)
