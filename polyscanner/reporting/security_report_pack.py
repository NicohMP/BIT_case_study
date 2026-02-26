"""Deterministic context pack builder for the LLM (report time only).

Design:
- The LLM is NOT used for ingestion/filtering/matching/scoring.
- This module reads Postgres tables produced by Steps 1–4b and assembles a compact,
  structured context pack for a single security.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from polyscanner.db.pg import connect
from polyscanner.relevance.rate_like import is_rate_like


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def hash_pack(pack: dict[str, Any]) -> str:
    payload = json.dumps(pack, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _sha256_text(payload)


def _table_exists(conn, *, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", (f"public.{table_name}",))
        return cur.fetchone()[0] is not None


def _parse_md_table_row(line: str) -> list[str]:
    # Expect: | col1 | col2 | ... |
    # Note: this is a best-effort parser; it assumes no literal '|' characters inside cells.
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    return parts


def _load_security_exposure_rationales_md(md_path: str) -> dict[str, dict[str, str]]:
    """Return mapping company_name -> {table_header_domain -> rationale_text}."""
    p = Path(md_path)
    if not p.exists():
        return {}
    lines = p.read_text(encoding="utf-8").splitlines()
    # Find header row and separator row.
    header_idx = None
    for i, ln in enumerate(lines[:20]):
        if ln.strip().startswith("|") and "Company" in ln:
            header_idx = i
            break
    if header_idx is None or header_idx + 2 >= len(lines):
        return {}
    headers = _parse_md_table_row(lines[header_idx])
    # Next line is separator; data starts after it.
    out: dict[str, dict[str, str]] = {}
    for ln in lines[header_idx + 2 :]:
        if not ln.strip().startswith("|"):
            continue
        cols = _parse_md_table_row(ln)
        if len(cols) != len(headers):
            continue
        row = dict(zip(headers, cols, strict=False))
        company = (row.get("Company") or "").strip()
        if not company:
            continue
        out[company] = {k: (v or "").strip() for k, v in row.items() if k != "Company"}
    return out


def _strip_md_links(text: str) -> str:
    # Keep link text, drop URLs.
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text or "")
    return t.strip()


@dataclass(frozen=True)
class Versions:
    run_id: str | None
    filter_version: str
    matcher_version: str
    scoring_version: str
    selection_version: str


def _fmt_usd_short(x: Any) -> str | None:
    try:
        v = float(x)
    except Exception:
        return None
    if v < 0 or v != v:  # NaN
        return None
    if v >= 1_000_000_000:
        return f"${v/1_000_000_000:.2f}B"
    if v >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"${v/1_000:.1f}k"
    return f"${v:.0f}"


def _bucket3(x: float | None, *, hi: float, mid: float) -> str:
    try:
        v = float(x) if x is not None else 0.0
    except Exception:
        return "Unknown"
    if v >= hi:
        return "High"
    if v >= mid:
        return "Medium"
    return "Low"


def _days_to(end_iso: str | None, *, now: datetime) -> int | None:
    if not end_iso:
        return None
    try:
        end_dt = datetime.fromisoformat(str(end_iso).replace("Z", "+00:00"))
        return int((end_dt - now).total_seconds() // 86400)
    except Exception:
        return None


def _derive_pricing(*, probability: Any, outcomes: Any, probabilities: Any) -> dict[str, Any]:
    """Best-effort pricing summary for the report-time pack.

    Goal: give the LLM something it can quote without inventing numbers.
    """
    out: dict[str, Any] = {"kind": "unknown", "yes_probability": None, "top_outcomes": [], "note": None}

    # Binary yes/no: prefer explicit scalar probability.
    try:
        p = float(probability) if probability is not None else None
    except Exception:
        p = None
    if p is not None and 0.0 <= p <= 1.0:
        out["kind"] = "binary"
        out["yes_probability"] = p
        out["note"] = None
        return out

    # Multi-outcome: pair outcomes + probabilities if possible.
    oc = outcomes if isinstance(outcomes, list) else None
    pr = probabilities if isinstance(probabilities, list) else None
    prd = probabilities if isinstance(probabilities, dict) else None
    pairs: list[tuple[float, str]] = []

    if oc and pr and len(oc) == len(pr) and oc:
        for o, pv in zip(oc, pr, strict=False):
            try:
                prob = float(pv)
            except Exception:
                continue
            if prob < 0 or prob > 1:
                continue
            label = None
            if isinstance(o, str):
                label = o.strip()
            elif isinstance(o, dict):
                label = str(o.get("outcome") or o.get("name") or o.get("title") or "").strip()
            if not label:
                continue
            pairs.append((prob, label))

    # Dict-shaped probabilities: {outcome_label: prob}
    if not pairs and prd:
        for k, v in prd.items():
            label = str(k or "").strip()
            try:
                prob = float(v) if v is not None else None
            except Exception:
                prob = None
            if not label or prob is None:
                continue
            if 0.0 <= prob <= 1.0:
                pairs.append((prob, label))

    # Sometimes outcomes are dicts with embedded probability/price.
    if not pairs and oc:
        for o in oc:
            if not isinstance(o, dict):
                continue
            label = str(o.get("outcome") or o.get("name") or o.get("title") or "").strip()
            pv = o.get("probability") or o.get("prob") or o.get("p") or o.get("price")
            try:
                prob = float(pv) if pv is not None else None
            except Exception:
                prob = None
            if not label or prob is None:
                continue
            if 0.0 <= prob <= 1.0:
                pairs.append((prob, label))

    if pairs:
        pairs.sort(key=lambda x: x[0], reverse=True)
        out["kind"] = "multi_outcome"
        out["top_outcomes"] = [{"outcome": lab, "probability": prob} for prob, lab in pairs[:5]]
        out["note"] = None
        return out

    out["note"] = "Pricing unavailable in ingestion schema for this market type."
    return out


def fetch_latest_versions(conn) -> Versions:
    if not _table_exists(conn, table_name="pm_pipeline_run"):
        raise RuntimeError("pm_pipeline_run not found. Apply migration 20260225201500_add_pm_pipeline_run_and_views.sql.")
    with conn.cursor() as cur:
        cur.execute(
            """
            select run_id, filter_version, matcher_version, scoring_version, selection_version
            from v_pm_latest_pipeline_run;
            """
        )
        row = cur.fetchone()
    if not row:
        raise RuntimeError("No successful pipeline runs found in pm_pipeline_run.")
    run_id, fv, mv, sv, selv = row
    if not (fv and mv and sv and selv):
        raise RuntimeError(f"Latest run is missing version fields: {row}")
    return Versions(
        run_id=str(run_id) if run_id is not None else None,
        filter_version=str(fv),
        matcher_version=str(mv),
        scoring_version=str(sv),
        selection_version=str(selv),
    )


def _fetch_security(conn, *, security_id: int | None, ticker: str | None, exchange_mic: str | None) -> dict[str, Any]:
    if security_id is not None:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, company_name, ticker, exchange_mic
                from bit_security
                where id = %s;
                """,
                (int(security_id),),
            )
            row = cur.fetchone()
        if not row:
            raise RuntimeError(f"Unknown security_id={security_id}")
        return {"id": int(row[0]), "company_name": str(row[1]), "ticker": str(row[2]), "exchange_mic": str(row[3])}

    if not ticker:
        raise ValueError("Provide security_id or ticker")
    if exchange_mic:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, company_name, ticker, exchange_mic
                from bit_security
                where ticker = %s and exchange_mic = %s;
                """,
                (str(ticker), str(exchange_mic)),
            )
            row = cur.fetchone()
        if not row:
            raise RuntimeError(f"Unknown security ticker={ticker!r} exchange_mic={exchange_mic!r}")
        return {"id": int(row[0]), "company_name": str(row[1]), "ticker": str(row[2]), "exchange_mic": str(row[3])}

    with conn.cursor() as cur:
        cur.execute(
            """
            select id, company_name, ticker, exchange_mic
            from bit_security
            where ticker = %s
            order by exchange_mic;
            """,
            (str(ticker),),
        )
        rows = cur.fetchall()
    if not rows:
        raise RuntimeError(f"Unknown security ticker={ticker!r}")
    if len(rows) > 1:
        opts = ", ".join([f"{r[2]}@{r[3]}" for r in rows[:10]])
        raise RuntimeError(f"Ambiguous ticker={ticker!r}; specify --exchange-mic. Options: {opts}")
    r = rows[0]
    return {"id": int(r[0]), "company_name": str(r[1]), "ticker": str(r[2]), "exchange_mic": str(r[3])}


def _fetch_exposures(conn, *, security_id: int) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select d.id, d.name, x.weight
            from bit_security_macro_domain_exposure x
            join macro_domain d on d.id = x.macro_domain_id
            where x.security_id = %s
            order by x.weight desc, d.name;
            """,
            (int(security_id),),
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for did, name, w in rows:
        out.append({"macro_domain_id": int(did), "macro_domain_name": str(name), "weight": float(w)})
    return out


def _fetch_selected_markets_enriched(
    conn,
    *,
    security_id: int,
    scoring_version: str,
    selection_version: str,
    top_k: int,
) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            select
              sel.rank,
              sel.final_score,
              sel.market_id,
              sel.event_id,
              sel.is_rate_like,
              m.question,
              m.category,
              m.probability,
              m.probabilities,
              m.volume_usd,
              m.liquidity_usd,
              m.end_date,
              m.outcomes,
              m.tags,
              e.title as event_title,
              r.base_score,
              r.quality_multiplier,
              r.score_breakdown
            from pm_market_security_relevance_selection sel
            join pm_market m on m.pm_market_id = sel.market_id
            left join pm_event e on e.event_id = m.event_id
            join pm_market_security_relevance r
              on r.security_id = sel.security_id
             and r.market_id = sel.market_id
             and r.scoring_version = sel.scoring_version
            where sel.security_id = %s
              and sel.scoring_version = %s
              and sel.selection_version = %s
            order by sel.rank asc
            limit %s;
            """,
            (int(security_id), str(scoring_version), str(selection_version), int(top_k)),
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        # Columns:
        #  0 rank
        #  1 final_score
        #  2 market_id
        #  3 event_id
        #  4 is_rate_like
        #  5 question
        #  6 category
        #  7 probability
        #  8 probabilities (jsonb)
        #  9 volume_usd
        # 10 liquidity_usd
        # 11 end_date
        # 12 outcomes
        # 13 tags
        # 14 event_title
        # 15 base_score
        # 16 quality_multiplier
        # 17 score_breakdown
        breakdown = r[17] if isinstance(r[17], dict) else {}
        out.append(
            {
                "rank": int(r[0]),
                "final_score": float(r[1]),
                "market_id": int(r[2]),
                "event_id": int(r[3]) if r[3] is not None else None,
                "is_rate_like": bool(r[4]) if r[4] is not None else is_rate_like(str(r[5] or "")),
                "question": str(r[5] or ""),
                "category": str(r[6]) if r[6] is not None else None,
                "probability": float(r[7]) if r[7] is not None else None,
                "probabilities": r[8] if isinstance(r[8], (list, dict)) else None,
                "volume_usd": float(r[9]) if r[9] is not None else None,
                "liquidity_usd": float(r[10]) if r[10] is not None else None,
                "end_date": r[11].isoformat() if r[11] is not None else None,
                "outcomes": r[12] if isinstance(r[12], list) else None,
                "tags": r[13] if isinstance(r[13], list) else [],
                "event_title": str(r[14]) if r[14] is not None else None,
                "base_score": float(r[15]) if r[15] is not None else None,
                "quality_multiplier": float(r[16]) if r[16] is not None else 1.0,
                "score_breakdown": breakdown,
            }
        )
    return out


def _fetch_filter_decisions(conn, *, market_ids: list[int], filter_version: str) -> dict[int, dict[str, Any]]:
    if not market_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            select market_id, quality_score, template_score, equity_relevance_score, rejection_reasons
            from pm_market_filter_decision
            where filter_version = %s
              and market_id = any(%s);
            """,
            (str(filter_version), market_ids),
        )
        rows = cur.fetchall()
    out: dict[int, dict[str, Any]] = {}
    for mid, q, tmpl, eq, reasons in rows:
        out[int(mid)] = {
            "quality_score": float(q) if q is not None else None,
            "template_score": float(tmpl) if tmpl is not None else None,
            "equity_relevance_score": float(eq) if eq is not None else None,
            "rejection_reasons": list(reasons) if isinstance(reasons, (list, tuple)) else [],
        }
    return out


def _fetch_market_family_matches(
    conn,
    *,
    market_ids: list[int],
    matcher_version: str,
    top_k: int = 5,
) -> dict[int, list[dict[str, Any]]]:
    if not market_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            select market_id, signal_family_id, method, match_strength, evidence
            from pm_market_signal_family_match
            where matcher_version = %s
              and market_id = any(%s)
              and match_strength > 0.0
            order by market_id,
              case when method = 'rule_classification' then 0 else 1 end,
              match_strength desc;
            """,
            (str(matcher_version), market_ids),
        )
        rows = cur.fetchall()
    out: dict[int, list[dict[str, Any]]] = {}
    for mid, fid, method, strength, evidence in rows:
        out.setdefault(int(mid), [])
        if len(out[int(mid)]) >= int(top_k):
            continue
        out[int(mid)].append(
            {
                "signal_family_id": int(fid),
                "method": str(method),
                "match_strength": float(strength),
                "evidence": evidence if isinstance(evidence, dict) else {},
            }
        )
    return out


def _fetch_signal_families(conn, *, family_ids: list[int]) -> list[dict[str, Any]]:
    if not family_ids:
        return []
    with conn.cursor() as cur:
        cur.execute(
            """
            select id, slug, title, description
            from signal_family
            where id = any(%s)
            order by id;
            """,
            (family_ids,),
        )
        rows = cur.fetchall()
    return [{"id": int(r[0]), "slug": str(r[1]), "title": str(r[2]), "description": str(r[3] or "")} for r in rows]


def _fetch_influence_slice(
    conn,
    *,
    family_ids: list[int],
    macro_domain_ids: list[int],
) -> list[dict[str, Any]]:
    if not family_ids or not macro_domain_ids:
        return []
    with conn.cursor() as cur:
        cur.execute(
            """
            select signal_family_id, macro_domain_id, score, rationale_md, sources
            from signal_family_domain_influence
            where signal_family_id = any(%s)
              and macro_domain_id = any(%s)
            order by signal_family_id, macro_domain_id;
            """,
            (family_ids, macro_domain_ids),
        )
        rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for fid, did, score, rationale_md, sources in rows:
        out.append(
            {
                "signal_family_id": int(fid),
                "macro_domain_id": int(did),
                "score": int(score),
                "score_norm": float(score) / 5.0,
                "rationale_md": str(rationale_md or ""),
                "sources": sources if isinstance(sources, list) else [],
            }
        )
    return out


def _market_strength(
    *,
    volume_usd: float | None,
    liquidity_usd: float | None,
    quality_multiplier: float | None,
    end_date_iso: str | None,
    now: datetime,
) -> float:
    vol = max(0.0, float(volume_usd or 0.0))
    liq = max(0.0, float(liquidity_usd or 0.0))
    q = float(quality_multiplier) if quality_multiplier is not None else 1.0
    # Log-scale volume/liquidity to 0..1-ish; cap at 1.
    import math

    vol_f = min(1.0, math.log1p(vol) / math.log1p(1_000_000.0))
    liq_f = min(1.0, math.log1p(liq) / math.log1p(1_000_000.0))

    # Time urgency: within 14 days => high urgency.
    urg = 0.5
    if end_date_iso:
        try:
            end_dt = datetime.fromisoformat(end_date_iso.replace("Z", "+00:00"))
            days = max(0.0, (end_dt - now).total_seconds() / 86400.0)
            urg = 1.0 if days <= 14.0 else 0.7 if days <= 60.0 else 0.4
        except Exception:
            urg = 0.5

    # Blend: quality is a multiplier, but we cap to keep within 0..1.
    strength = (0.55 * vol_f + 0.35 * liq_f + 0.10 * urg) * min(1.0, max(0.5, q))
    return float(max(0.0, min(1.0, strength)))


def build_security_context_pack(
    *,
    db_url: str,
    security_id: int | None = None,
    ticker: str | None = None,
    exchange_mic: str | None = None,
    versions: Versions | None = None,
    top_k_markets: int = 20,
    top_k_matches_per_market: int = 5,
    exposure_rationales_md_path: str = "security_domain_exposure_rationale.md",
) -> dict[str, Any]:
    """Build a deterministic context pack for one security."""
    now = _utcnow()

    conn = connect(db_url)
    try:
        if versions is None:
            versions = fetch_latest_versions(conn)

        sec = _fetch_security(conn, security_id=security_id, ticker=ticker, exchange_mic=exchange_mic)
        exposures = _fetch_exposures(conn, security_id=int(sec["id"]))
        if not exposures:
            raise RuntimeError(
                "No rows in bit_security_macro_domain_exposure for this security. "
                "Run `./venv/bin/python scripts/seed_security_domain_exposure.py`."
            )

        rationales_md = _load_security_exposure_rationales_md(exposure_rationales_md_path)

        # Map macro_domain.name -> rationale table header
        rationale_header_by_macro_domain = {
            "AI & Big Tech": "AI & Data Platforms",
            "Semis & Compute": "Semiconductors & Compute",
            "Cloud / Dev": "Cloud & Software Infrastructure",
            "Crypto Infra": "Crypto Mining & Infrastructure",
            "Fintech / CFP": "Fintech",
            "Digital Health": "Digital Health",
        }

        exp_with_rationale: list[dict[str, Any]] = []
        for ex in exposures:
            md_header = rationale_header_by_macro_domain.get(str(ex["macro_domain_name"]))
            rat = None
            if md_header and sec["company_name"] in rationales_md:
                rat = rationales_md[sec["company_name"]].get(md_header)
            exp_with_rationale.append(
                {
                    **ex,
                    "rationale": _strip_md_links(rat or "") or None,
                }
            )

        markets = _fetch_selected_markets_enriched(
            conn,
            security_id=int(sec["id"]),
            scoring_version=str(versions.scoring_version),
            selection_version=str(versions.selection_version),
            top_k=int(top_k_markets),
        )
        if not markets:
            raise RuntimeError(
                "No selected markets found for this security. Ensure Step 4b has been run and versions match."
            )

        market_ids = [int(m["market_id"]) for m in markets]
        decisions = _fetch_filter_decisions(conn, market_ids=market_ids, filter_version=str(versions.filter_version))
        matches = _fetch_market_family_matches(
            conn, market_ids=market_ids, matcher_version=str(versions.matcher_version), top_k=int(top_k_matches_per_market)
        )

        # Collect family ids from matches + breakdown.
        family_ids: set[int] = set()
        for mid, ms in matches.items():
            for it in ms:
                family_ids.add(int(it["signal_family_id"]))
        for m in markets:
            bd = m.get("score_breakdown") or {}
            top_fams = bd.get("top_families") or []
            for tf in top_fams:
                if isinstance(tf, dict) and tf.get("signal_family_id") is not None:
                    family_ids.add(int(tf["signal_family_id"]))

        families = _fetch_signal_families(conn, family_ids=sorted(family_ids))
        family_by_id = {int(f["id"]): f for f in families}

        macro_domain_ids = [int(x["macro_domain_id"]) for x in exposures]
        influence = _fetch_influence_slice(conn, family_ids=sorted(family_ids), macro_domain_ids=macro_domain_ids)

        # Attach per-market match vectors and compact breakdown.
        packed_markets: list[dict[str, Any]] = []
        for m in markets:
            mid = int(m["market_id"])
            dec = decisions.get(mid) or {}
            mv = matches.get(mid) or []
            mv2 = []
            for it in mv:
                fid = int(it["signal_family_id"])
                fam = family_by_id.get(fid) or {}
                mv2.append(
                    {
                        "signal_family_id": fid,
                        "slug": fam.get("slug"),
                        "title": fam.get("title"),
                        "method": it.get("method"),
                        "match_strength": it.get("match_strength"),
                        "evidence": it.get("evidence") or {},
                    }
                )

            bd = m.get("score_breakdown") or {}
            days_to = _days_to(str(m.get("end_date") or ""), now=now)
            pricing = _derive_pricing(probability=m.get("probability"), outcomes=m.get("outcomes"), probabilities=m.get("probabilities"))
            liquidity_amt = _fmt_usd_short(m.get("liquidity_usd"))
            volume_amt = _fmt_usd_short(m.get("volume_usd"))
            resolve_line = f"Resolves in {days_to}d." if isinstance(days_to, int) else "Resolve date unknown."
            pricing_line = None
            if pricing.get("kind") == "binary" and pricing.get("yes_probability") is not None:
                pricing_line = f"Pricing: Yes {float(pricing['yes_probability'])*100:.0f}%."
            elif pricing.get("kind") == "multi_outcome":
                tops = pricing.get("top_outcomes") or []
                if isinstance(tops, list) and tops:
                    t0 = tops[0]
                    if isinstance(t0, dict) and t0.get("outcome") and t0.get("probability") is not None:
                        pricing_line = f"Pricing: leading outcome '{t0['outcome']}' at {float(t0['probability'])*100:.0f}%."
            if not pricing_line:
                pricing_line = "Pricing: unavailable."

            # Stable buckets (avoid pack-quantiles to keep language consistent across runs).
            buckets = {
                "structural_relevance": _bucket3(float(m.get("base_score") or 0.0), hi=0.70, mid=0.45),
                "actionability": _bucket3(
                    _market_strength(
                        volume_usd=m.get("volume_usd"),
                        liquidity_usd=m.get("liquidity_usd"),
                        quality_multiplier=float(m.get("quality_multiplier") or 1.0),
                        end_date_iso=m.get("end_date"),
                        now=now,
                    ),
                    hi=0.75,
                    mid=0.50,
                ),
                "liquidity": _bucket3(float(m.get("liquidity_usd") or 0.0), hi=100_000.0, mid=10_000.0),
                "volume": _bucket3(float(m.get("volume_usd") or 0.0), hi=1_000_000.0, mid=100_000.0),
                "urgency": "High" if isinstance(days_to, int) and days_to <= 14 else "Medium" if isinstance(days_to, int) and days_to <= 60 else "Low",
                "pricing_available": "Yes" if (pricing.get("kind") != "unknown") else "No",
            }

            packed_markets.append(
                {
                    "rank": int(m["rank"]),
                    "market_id": mid,
                    "event_id": m.get("event_id"),
                    "event_title": m.get("event_title"),
                    "question": m.get("question"),
                    "category": m.get("category"),
                    "tags": m.get("tags") or [],
                    "outcomes": m.get("outcomes"),
                    "probabilities": m.get("probabilities"),
                    "probability": m.get("probability"),
                    "pricing": pricing,
                    "volume_usd": m.get("volume_usd"),
                    "liquidity_usd": m.get("liquidity_usd"),
                    "end_date": m.get("end_date"),
                    "is_rate_like": bool(m.get("is_rate_like")),
                    "buckets": buckets,
                    "market_card": {
                        "headline": str(m.get("question") or ""),
                        "resolve_line": resolve_line,
                        "pricing_line": pricing_line,
                        "context_line": " ".join(
                            [
                                f"Liquidity {buckets['liquidity']}" + (f" ({liquidity_amt})" if liquidity_amt else ""),
                                f"Volume {buckets['volume']}" + (f" ({volume_amt})" if volume_amt else ""),
                                f"Urgency {buckets['urgency']}.",
                            ]
                        ).strip(),
                    },
                    "scores": {
                        "final_score": float(m.get("final_score") or 0.0),
                        "base_score": float(m.get("base_score") or 0.0),
                        "quality_multiplier": float(m.get("quality_multiplier") or 1.0),
                        "market_strength": _market_strength(
                            volume_usd=m.get("volume_usd"),
                            liquidity_usd=m.get("liquidity_usd"),
                            quality_multiplier=float(m.get("quality_multiplier") or 1.0),
                            end_date_iso=m.get("end_date"),
                            now=now,
                        ),
                    },
                    "filter_decision": {
                        "quality_score": dec.get("quality_score"),
                        "template_score": dec.get("template_score"),
                        "equity_relevance_score": dec.get("equity_relevance_score"),
                    },
                    "match_vector_topk": mv2,
                    "score_breakdown_top": {
                        "top_families": bd.get("top_families") or [],
                        "top_domains": bd.get("top_domains") or [],
                    },
                }
            )

        pack: dict[str, Any] = {
            "report_meta": {
                "as_of_utc": now.isoformat(),
                "run_id": versions.run_id,
                "versions": {
                    "filter_version": versions.filter_version,
                    "matcher_version": versions.matcher_version,
                    "scoring_version": versions.scoring_version,
                    "selection_version": versions.selection_version,
                },
                "builder": {
                    "top_k_markets": int(top_k_markets),
                    "top_k_matches_per_market": int(top_k_matches_per_market),
                },
            },
            "security": {
                "security_id": int(sec["id"]),
                "ticker": sec["ticker"],
                "company_name": sec["company_name"],
                "exchange_mic": sec["exchange_mic"],
                "business_description": None,
            },
            "exposure_vector": exp_with_rationale,
            "signal_families": families,
            "influence_matrix_slice": influence,
            "markets": packed_markets,
            "constraints": {
                "no_external_facts": True,
                "prefer_final_score_ordering": True,
                "source_of_candidates": "pm_market_security_relevance_selection",
            },
        }
        pack["report_meta"]["pack_sha256"] = hash_pack(pack)
        return pack
    finally:
        conn.close()
