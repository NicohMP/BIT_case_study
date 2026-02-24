"""Markdown rendering for the signal-family LLM report."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def render_signal_family_llm_report_markdown(*, as_of: datetime, llm_report: dict[str, Any]) -> str:
    title = str(llm_report.get("title") or "Signal Family Report")

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Generated at: `{as_of.isoformat()}`")
    lines.append("")

    families = llm_report.get("families") or []
    for fam in families:
        if not isinstance(fam, dict):
            continue
        lines.append(f"## {fam.get('title') or fam.get('slug')}")
        if fam.get("slug"):
            lines.append(f"- `slug`: `{fam.get('slug')}`")

        what = fam.get("what_to_watch") or []
        if what:
            lines.append("- what_to_watch:")
            for w in what:
                lines.append(f"  - {w}")

        top = fam.get("top_markets") or []
        if not top:
            lines.append("")
            lines.append("_No representative markets selected._")
            lines.append("")
        else:
            lines.append("")
            for m in top:
                if not isinstance(m, dict):
                    continue
                headline = m.get("headline") or m.get("question") or "(no headline)"
                lines.append(f"### {headline}")
                if m.get("question") and m.get("headline") and m.get("headline") != m.get("question"):
                    lines.append(f"- question: {m.get('question')}")
                if m.get("pm_market_id") is not None:
                    lines.append(f"- `pm_market_id`: {m.get('pm_market_id')}")
                if m.get("probability") is not None:
                    lines.append(f"- probability: {m.get('probability')}")
                if m.get("volume_usd") is not None:
                    lines.append(f"- volume_usd: {m.get('volume_usd')}")
                if m.get("final_score") is not None:
                    lines.append(f"- final_score: {m.get('final_score')}")
                if m.get("confidence") is not None:
                    lines.append(f"- confidence: {m.get('confidence')}")
                if m.get("dedupe_group"):
                    lines.append(f"- dedupe_group: `{m.get('dedupe_group')}`")
                if m.get("why_it_matters"):
                    lines.append(f"- why_it_matters: {m.get('why_it_matters')}")

                impacted = m.get("impacted_domains") or []
                if impacted:
                    lines.append("- impacted_domains:")
                    for d in impacted:
                        if not isinstance(d, dict):
                            continue
                        dom = d.get("macro_domain") or "Unknown"
                        score = d.get("influence_score")
                        expl = d.get("explanation") or ""
                        if score is None:
                            lines.append(f"  - {dom}: {expl}".rstrip())
                        else:
                            lines.append(f"  - {dom} (score={score}): {expl}".rstrip())
                lines.append("")

        excluded = fam.get("excluded_as_redundant") or []
        if excluded:
            lines.append("**Redundant markets excluded**")
            for e in excluded:
                if not isinstance(e, dict):
                    continue
                mid = e.get("pm_market_id")
                reason = e.get("reason") or ""
                lines.append(f"- {mid}: {reason}".rstrip())
            lines.append("")

        off = fam.get("excluded_as_offtopic") or []
        if off:
            lines.append("**Off-topic markets excluded**")
            for e in off:
                if not isinstance(e, dict):
                    continue
                mid = e.get("pm_market_id")
                reason = e.get("reason") or ""
                lines.append(f"- {mid}: {reason}".rstrip())
            lines.append("")

    notes = llm_report.get("notes") or []
    if notes:
        lines.append("## Notes")
        for n in notes:
            lines.append(f"- {n}")
        lines.append("")

    lines.append("---")
    lines.append("## Raw LLM JSON")
    lines.append("```json")
    lines.append(json.dumps(llm_report, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)
