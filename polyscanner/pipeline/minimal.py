"""Minimal end-to-end pipeline (notebook-friendly).

Flow:
1) Read BIT domains from Postgres (Supabase)
2) Fetch active Polymarket markets (Gamma API)
3) Heuristically rank markets against domains (pick top N)
4) Ask Gemini to assign each market to a domain (structured JSON)
5) Render to markdown and write a `.md` file

This is designed as a "wiring test" for the case study, not as a final system.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv  # type: ignore
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

from polyscanner.filtering import Domain, rank_markets
from polyscanner.polymarket_client import fetch_and_normalize_active_markets
from polyscanner.signal_llm import assign_domains_with_gemini


def _env(name: str) -> str | None:
    v = os.getenv(name)
    if v is None:
        return None
    v = v.strip()
    return v or None


def _connect_pg(db_url: str):
    try:
        import psycopg  # type: ignore

        return psycopg.connect(db_url)
    except Exception as e:
        raise RuntimeError("psycopg is required to connect to Postgres") from e


def fetch_domains(db_url: str) -> list[Domain]:
    conn = _connect_pg(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute("select id, name from bit_domain order by id;")
            rows = cur.fetchall()
        return [Domain(id=int(r[0]), name=str(r[1])) for r in rows]
    finally:
        conn.close()


def _render_markdown(
    *,
    as_of: datetime,
    domains: list[Domain],
    ranked_markets,
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

    # Include raw JSON at bottom for easy inspection in a notebook/editor.
    lines.append("---")
    lines.append("## Raw LLM JSON")
    lines.append("```json")
    lines.append(json.dumps(llm_result, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def run_minimal_pipeline(
    *,
    db_url: str | None = None,
    polymarket_base_url: str | None = None,
    top_n: int = 10,
    markets_limit: int = 200,
    out_dir: str = "reports",
    use_llm: bool = True,
) -> dict[str, Any]:
    """Run the minimal pipeline and write a markdown report.

    Returns a dict containing:
    - report_path
    - report_md
    - domains
    - ranked_markets
    - llm_result
    """
    if load_dotenv is not None:
        load_dotenv(override=False)

    db_url = (db_url or _env("DATABASE_URL"))
    if not db_url:
        raise RuntimeError("DATABASE_URL is required (pass db_url=... or set it in .env)")
    db_url = db_url.strip()
    # Accept SQLAlchemy-style URLs (common in local .env files).
    db_url = db_url.replace("postgresql+psycopg://", "postgresql://")

    domains = fetch_domains(db_url)
    if not domains:
        raise RuntimeError("No domains found in bit_domain; seed domains first.")

    markets = fetch_and_normalize_active_markets(
        base_url=polymarket_base_url or _env("POLYMARKET_API_BASE_URL") or "https://gamma-api.polymarket.com",
        limit=markets_limit,
    )
    ranked = rank_markets(markets, domains, top_n=top_n)

    as_of = datetime.now(timezone.utc)
    if use_llm:
        llm_result = assign_domains_with_gemini(ranked, domains)
    else:
        llm_result = {
            "title": f"Signal Report — {as_of.date().isoformat()}",
            "items": [
                {
                    "pm_market_id": rm.market.pm_market_id,
                    "domain": rm.heuristic_domain or "Unknown",
                    "confidence": 0.0,
                    "rationale": "Heuristic-only (LLM disabled).",
                }
                for rm in ranked
            ],
        }
    report_md = _render_markdown(as_of=as_of, domains=domains, ranked_markets=ranked, llm_result=llm_result)

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    fname = f"signal_report_{as_of.strftime('%Y%m%d_%H%M%S')}.md"
    report_path = out_path / fname
    report_path.write_text(report_md, encoding="utf-8")

    return {
        "report_path": str(report_path),
        "report_md": report_md,
        "domains": [asdict(d) for d in domains],
        "ranked_markets": [
            {
                "pm_market_id": rm.market.pm_market_id,
                "question": rm.market.question,
                "category": rm.market.category,
                "probability": rm.market.probability,
                "volume": rm.market.volume,
                "heuristic_domain": rm.heuristic_domain,
                "score": rm.score,
            }
            for rm in ranked
        ],
        "llm_result": llm_result,
    }
