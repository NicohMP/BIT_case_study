"""Markdown report rendering helpers."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from polyscanner.models import Domain, DomainDefinition, RankedMarket


def render_signal_report_markdown(
    *,
    as_of: datetime,
    domains: list[Domain],
    ranked_markets: list[RankedMarket],
    llm_result: dict[str, Any],
) -> str:
    title = str(llm_result.get("title") or f"Signal Report — {as_of.date().isoformat()}")
    items = llm_result.get("items") or []
    by_id = {int(i.get("pm_market_id")): i for i in items if isinstance(i, dict) and i.get("pm_market_id") is not None}

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Generated at: `{as_of.isoformat()}`")
    lines.append("")
    lines.append("## Domains")
    for d in domains:
        lines.append(f"- {d.name}")
    lines.append("")
    lines.append("## Top Markets (domain assignment)")
    lines.append("")
    for rm in ranked_markets:
        m = rm.market
        llm_item = by_id.get(m.pm_market_id, {})
        llm_domain = llm_item.get("domain")
        confidence = llm_item.get("confidence")
        rationale = llm_item.get("rationale")
        lines.append(f"### {m.question}")
        lines.append(f"- `pm_market_id`: {m.pm_market_id}")
        if m.probability is not None:
            lines.append(f"- probability: {m.probability}")
        if m.volume is not None:
            lines.append(f"- volume: {m.volume}")
        lines.append(f"- heuristic_domain: {rm.heuristic_domain or 'None'} (score={rm.score:.2f})")
        lines.append(f"- llm_domain: {llm_domain or 'Unknown'} (confidence={confidence if confidence is not None else 'n/a'})")
        if rationale:
            lines.append(f"- rationale: {rationale}")
        lines.append("")

    lines.append("---")
    lines.append("## Raw LLM JSON")
    lines.append("```json")
    lines.append(json.dumps(llm_result, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def render_scored_signal_report_markdown(
    *,
    as_of: datetime,
    domains: list[DomainDefinition],
    scored_items: list[dict[str, Any]],
    llm_result: dict[str, Any] | None = None,
) -> str:
    """Render a scored report.

    `scored_items` should be JSONable dicts (see `polyscanner.relevance.final_score.to_jsonable`).
    """
    llm_result = llm_result or {}
    title = str(llm_result.get("title") or f"Signal Report — {as_of.date().isoformat()}")
    items = llm_result.get("items") or []
    by_id = {int(i.get("pm_market_id")): i for i in items if isinstance(i, dict) and i.get("pm_market_id") is not None}

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- Generated at: `{as_of.isoformat()}`")
    lines.append("")
    lines.append("## Domains (definitions)")
    for d in domains:
        lines.append(f"### {d.name}")
        lines.append(d.description.strip() or "(no description)")
        if d.keywords:
            lines.append(f"- keywords: {', '.join(d.keywords)}")
        if d.exclusions:
            lines.append(f"- exclusions: {', '.join(d.exclusions)}")
        lines.append("")

    lines.append("## Top Markets (scored)")
    lines.append("")
    for it in scored_items:
        pm_market_id = it.get("pm_market_id")
        llm_item = by_id.get(int(pm_market_id), {}) if pm_market_id is not None else {}

        lines.append(f"### {it.get('question')}")
        lines.append(f"- `pm_market_id`: {pm_market_id}")
        if it.get("probability") is not None:
            lines.append(f"- probability: {it.get('probability')}")
        if it.get("volume") is not None:
            lines.append(f"- volume: {it.get('volume')}")

        lines.append(f"- best_domain: {it.get('best_domain')}")
        lines.append(f"- domain_relevance: {it.get('domain_relevance')}")
        if it.get("raw_domain_similarity") is not None:
            lines.append(f"- raw_domain_similarity: {it.get('raw_domain_similarity')}")

        lines.append(f"- channel_relevance: {json.dumps(it.get('channel_relevance', {}), ensure_ascii=False)}")
        lines.append(f"- domain_exposure: {json.dumps(it.get('domain_exposure', {}), ensure_ascii=False)}")
        lines.append(f"- exposure_dot: {it.get('exposure_dot')}")
        lines.append(f"- final_score: {it.get('final_score')}")

        # LLM (optional)
        if llm_item:
            llm_domain = llm_item.get("domain")
            confidence = llm_item.get("confidence")
            rationale = llm_item.get("rationale")
            lines.append(f"- llm_domain: {llm_domain or 'Unknown'} (confidence={confidence if confidence is not None else 'n/a'})")
            if rationale:
                lines.append(f"- llm_rationale: {rationale}")
        lines.append("")

    lines.append("---")
    if llm_result:
        lines.append("## Raw LLM JSON")
        lines.append("```json")
        lines.append(json.dumps(llm_result, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def write_report_markdown(*, report_md: str, out_dir: str, as_of: datetime) -> str:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    fname = f"signal_report_{as_of.strftime('%Y%m%d_%H%M%S')}.md"
    report_path = out_path / fname
    report_path.write_text(report_md, encoding="utf-8")
    return str(report_path)
