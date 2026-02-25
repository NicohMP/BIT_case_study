"""Two-stage signal-family matcher (Step 3).

Stages:
1) DISCOVERY (high recall):
   - lexical keyword discovery
   - optional semantic embedding discovery
2) CLASSIFICATION (high precision):
   - deterministic gated rules evaluated ONLY on discovery candidates

All outputs are persisted to Postgres with `matcher_version` so runs are auditable.
"""

from __future__ import annotations

import csv
import json
import logging
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from polyscanner.db.pg import connect
from polyscanner.filtering.hard_filters import load_hard_filter_rules
from polyscanner.matching.classification import classify_with_rule
from polyscanner.matching.discovery import (
    DiscoveryCandidate,
    embedding_discover_topk_with_stats,
    lexical_discover,
)
from polyscanner.matching.embeddings import DBEmbeddingCache, LocalSentenceTransformerEmbedder
from polyscanner.matching.family_descriptors import build_family_descriptors, load_family_keywords
from polyscanner.signal_family_rules import RULES_BY_SLUG

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class MarketRow:
    market_id: int
    event_id: int | None
    question: str
    category: str | None
    market_slug: str | None
    market_tags: list[Any]
    event_title: str | None
    event_slug: str | None
    event_tags: list[Any]
    volume_usd: float | None
    liquidity_usd: float | None

    def to_text(self) -> str:
        def tags_to_text(tags: list[Any]) -> str:
            parts: list[str] = []
            for t in tags or []:
                if isinstance(t, str):
                    parts.append(t)
                elif isinstance(t, dict):
                    for k in ("slug", "label", "name"):
                        v = t.get(k)
                        if isinstance(v, str) and v.strip():
                            parts.append(v.strip())
            return " ".join(parts)

        parts = [
            self.question,
            self.category or "",
            self.market_slug or "",
            self.event_title or "",
            self.event_slug or "",
            tags_to_text(self.market_tags),
            tags_to_text(self.event_tags),
        ]
        return " ".join([p for p in parts if p]).strip()

    def to_strict_text(self) -> str:
        """Higher-precision text view for strict rule classification.

        We intentionally exclude category/tags here.
        Those fields can be noisy or editorial (e.g. "Big Tech") and cause false-positive
        strict matches. Discovery already uses the full `to_text()`; strict rules should
        rely primarily on the question and event title context.
        """
        parts = [
            self.question,
            self.market_slug or "",
            self.event_title or "",
            self.event_slug or "",
        ]
        return " ".join([p for p in parts if p]).strip()


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _table_exists(conn, *, table_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s);", (f"public.{table_name}",))
        return cur.fetchone()[0] is not None


def _fetch_kept_markets(
    db_url: str,
    *,
    filter_version: str,
    limit: int,
) -> list[MarketRow]:
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                  m.pm_market_id,
                  m.event_id,
                  m.question,
                  m.category,
                  m.slug as market_slug,
                  m.tags as market_tags,
                  e.title as event_title,
                  e.slug as event_slug,
                  e.tags as event_tags,
                  m.volume_usd,
                  m.liquidity_usd
                from pm_market m
                join pm_event e on e.event_id = m.event_id
                join pm_market_filter_decision d
                  on d.market_id = m.pm_market_id
                 and d.filter_version = %s
                 and d.is_rejected = false
                where e.active = true and e.closed = false
                order by m.volume_usd desc nulls last, m.liquidity_usd desc nulls last, m.pm_market_id
                limit %s;
                """,
                (str(filter_version), int(limit)),
            )
            rows = cur.fetchall()
        out: list[MarketRow] = []
        for r in rows:
            out.append(
                MarketRow(
                    market_id=int(r[0]),
                    event_id=int(r[1]) if r[1] is not None else None,
                    question=str(r[2] or ""),
                    category=str(r[3]) if r[3] is not None else None,
                    market_slug=str(r[4]) if r[4] is not None else None,
                    market_tags=r[5] if isinstance(r[5], list) else [],
                    event_title=str(r[6]) if r[6] is not None else None,
                    event_slug=str(r[7]) if r[7] is not None else None,
                    event_tags=r[8] if isinstance(r[8], list) else [],
                    volume_usd=float(r[9]) if r[9] is not None else None,
                    liquidity_usd=float(r[10]) if r[10] is not None else None,
                )
            )
        return out
    finally:
        conn.close()


def _upsert_matches(db_url: str, rows: list[dict[str, Any]]) -> int:
    if not rows:
        return 0
    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.executemany(
                """
                insert into pm_market_signal_family_match (
                  market_id,
                  signal_family_id,
                  method,
                  matcher_version,
                  match_strength,
                  evidence,
                  rationale,
                  created_at,
                  updated_at
                ) values (
                  %(market_id)s,
                  %(signal_family_id)s,
                  %(method)s,
                  %(matcher_version)s,
                  %(match_strength)s,
                  %(evidence)s::jsonb,
                  %(rationale)s,
                  now(),
                  now()
                )
                on conflict (market_id, signal_family_id, method, matcher_version) do update set
                  match_strength = excluded.match_strength,
                  evidence = excluded.evidence,
                  rationale = excluded.rationale,
                  updated_at = now();
                """,
                rows,
            )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def run_family_matching(
    *,
    db_url: str,
    filter_version: str | None,
    matcher_version: str,
    limit: int = 5000,
    use_embeddings: bool = True,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    embedding_device: str | None = None,
    embedding_top_k: int = 5,
    embedding_min_similarity: float = 0.40,
    lexical_target_hits: int = 2,
    lexical_min_score: float = 0.30,
    max_candidates_per_market: int = 12,
    classification_min_score: float = 0.70,
    out_dir: str = "reports",
) -> dict[str, Any]:
    """Run Step-3 matching and write audit artifacts."""
    if filter_version is None:
        filter_version = load_hard_filter_rules().filter_version

    run_id = uuid.uuid4()

    markets = _fetch_kept_markets(db_url, filter_version=str(filter_version), limit=int(limit))
    if not markets:
        # Provide actionable diagnostics. This failure usually means:
        # - Step 2 hasn't been run for this filter_version (no decisions),
        # - or Step 2 rejected everything for this version,
        # - or Step 1 ingestion hasn't populated pm_event/pm_market.
        conn = connect(db_url)
        try:
            with conn.cursor() as cur:
                cur.execute("select count(*) from pm_market_filter_decision where filter_version = %s;", (str(filter_version),))
                n_decisions = int((cur.fetchone() or [0])[0] or 0)
                cur.execute(
                    "select count(*) from pm_market_filter_decision where filter_version = %s and is_rejected = false;",
                    (str(filter_version),),
                )
                n_kept = int((cur.fetchone() or [0])[0] or 0)
                cur.execute("select count(*) from pm_event where active = true and closed = false;")
                n_active_events = int((cur.fetchone() or [0])[0] or 0)
                cur.execute(
                    """
                    select filter_version, count(*) as n
                    from pm_market_filter_decision
                    group by filter_version
                    order by n desc
                    limit 10;
                    """
                )
                versions = [(str(r[0]), int(r[1])) for r in (cur.fetchall() or [])]
        finally:
            conn.close()

        msg = (
            f"No kept markets found for filter_version={filter_version!r}.\n"
            f"- pm_market_filter_decision rows for this version: {n_decisions}\n"
            f"- kept (is_rejected=false) for this version: {n_kept}\n"
            f"- active events in pm_event (active=true & closed=false): {n_active_events}\n"
            f"- available filter_versions (top 10 by rowcount): {versions}\n"
            "Next steps:\n"
            "1) Ensure Step 1 ran: `./venv/bin/python scripts/ingest_active_events.py ...`\n"
            f"2) Run Step 2 for this version: `./venv/bin/python scripts/run_hard_filters.py` (writes {filter_version})\n"
        )
        raise RuntimeError(msg)

    conn = connect(db_url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, slug, title, description
                from signal_family
                where is_active = true
                order by id;
                """
            )
            families_rows = cur.fetchall()
        signal_families = [
            {"id": int(r[0]), "slug": str(r[1]), "title": str(r[2]), "description": str(r[3] or "")}
            for r in families_rows
        ]
    finally:
        conn.close()

    keywords_by_slug = load_family_keywords()
    families = build_family_descriptors(signal_families=signal_families, keywords_by_slug=keywords_by_slug)
    family_by_id = {f.signal_family_id: f for f in families}
    market_by_id = {m.market_id: m for m in markets}

    # Optional: persist per-market threshold diagnostics if audit tables exist.
    audit_tables_ready = False
    try:
        conn_audit = connect(db_url)
        try:
            audit_tables_ready = _table_exists(conn_audit, table_name="pm_market_family_match_run") and _table_exists(
                conn_audit, table_name="pm_market_family_match_eval"
            )
            if audit_tables_ready:
                with conn_audit.cursor() as cur:
                    cur.execute(
                        """
                        insert into pm_market_family_match_run (
                          run_id, filter_version, matcher_version, params, created_at
                        ) values (
                          %(run_id)s, %(filter_version)s, %(matcher_version)s, %(params)s::jsonb, now()
                        );
                        """,
                        {
                            "run_id": str(run_id),
                            "filter_version": str(filter_version),
                            "matcher_version": str(matcher_version),
                            "params": json.dumps(
                                {
                                    "limit": int(limit),
                                    "use_embeddings": bool(use_embeddings),
                                    "embedding_model": str(embedding_model),
                                    "embedding_device": embedding_device,
                                    "embedding_top_k": int(embedding_top_k),
                                    "embedding_min_similarity": float(embedding_min_similarity),
                                    "lexical_target_hits": int(lexical_target_hits),
                                    "lexical_min_score": float(lexical_min_score),
                                    "max_candidates_per_market": int(max_candidates_per_market),
                                    "classification_min_score": float(classification_min_score),
                                },
                                ensure_ascii=False,
                            ),
                        },
                    )
                conn_audit.commit()
        finally:
            conn_audit.close()
    except Exception:
        audit_tables_ready = False

    # ----- Discovery: lexical -----
    discovery_by_market: dict[int, list[DiscoveryCandidate]] = {}
    lexical_best_by_market: dict[int, tuple[float, int] | None] = {}
    discovery_markets_by_family: dict[int, set[int]] = defaultdict(set)
    for m in markets:
        mt = m.to_text()
        all_cands: list[DiscoveryCandidate] = []
        kept_cands: list[DiscoveryCandidate] = []
        for f in families:
            dc = lexical_discover(market_text=mt, family=f, target_hits=int(lexical_target_hits))
            if dc is None:
                continue
            all_cands.append(dc)
            if dc.score >= float(lexical_min_score):
                kept_cands.append(dc)

        if all_cands:
            best = max(all_cands, key=lambda x: float(x.score))
            lexical_best_by_market[m.market_id] = (float(best.score), int(best.signal_family_id))
        else:
            lexical_best_by_market[m.market_id] = None

        # keep top lexical candidates (score desc, then hit_count)
        cands_sorted = sorted(
            kept_cands,
            key=lambda x: (float(x.score), int(x.evidence.get("hit_count") or 0)),
            reverse=True,
        )
        kept = cands_sorted[: max(1, int(max_candidates_per_market))]
        discovery_by_market[m.market_id] = kept
        for dc in kept:
            discovery_markets_by_family[int(dc.signal_family_id)].add(int(m.market_id))

    # ----- Discovery: embeddings -----
    embedding_by_market: dict[int, list[DiscoveryCandidate]] = {}
    embedding_best_by_market: dict[int, dict[str, Any]] = {}
    embedding_sim_by_family_market: dict[int, dict[int, float]] = defaultdict(dict)
    if use_embeddings:
        provider = LocalSentenceTransformerEmbedder(model_name=str(embedding_model), device=embedding_device)
        market_texts_by_id = {m.market_id: m.to_text() for m in markets}
        embedding_by_market, embedding_best_by_market = embedding_discover_topk_with_stats(
            market_texts_by_id=market_texts_by_id,
            families=families,
            provider=provider,
            db_url=db_url,
            top_k=int(embedding_top_k),
            min_similarity=float(embedding_min_similarity),
        )
        for mid, cands in embedding_by_market.items():
            for dc in cands:
                discovery_markets_by_family[int(dc.signal_family_id)].add(int(mid))
                prev = embedding_sim_by_family_market[int(dc.signal_family_id)].get(int(mid))
                if prev is None or float(dc.score) > float(prev):
                    embedding_sim_by_family_market[int(dc.signal_family_id)][int(mid)] = float(dc.score)

    # ----- Candidate union (per market) -----
    candidates_by_market: dict[int, list[int]] = {}
    for m in markets:
        ids: list[int] = []
        for dc in discovery_by_market.get(m.market_id, []):
            ids.append(int(dc.signal_family_id))
        for dc in embedding_by_market.get(m.market_id, []):
            ids.append(int(dc.signal_family_id))
        # stable unique preserving order
        seen: set[int] = set()
        uniq: list[int] = []
        for x in ids:
            if x in seen:
                continue
            seen.add(x)
            uniq.append(x)
        candidates_by_market[m.market_id] = uniq[: max(1, int(max_candidates_per_market))]

    # ----- Classification on candidates -----
    now = _utcnow()
    match_rows: list[dict[str, Any]] = []
    discovery_rows_written = 0
    rule_rows_written = 0
    coverage_counts: Counter[int] = Counter()
    rule_attempts_by_market: Counter[int] = Counter()
    rule_matches_by_market: Counter[int] = Counter()

    # For diagnosis artifact: store best discovery similarity per (family, market).
    best_embedding_by_family: dict[int, list[tuple[float, int, dict[str, Any]]]] = defaultdict(list)
    best_lexical_by_family: dict[int, list[tuple[float, int, dict[str, Any]]]] = defaultdict(list)
    classification_attempts_by_family: dict[int, list[dict[str, Any]]] = defaultdict(list)

    for m in markets:
        mt = m.to_text()
        strict_text = m.to_strict_text()
        market_id = int(m.market_id)

        # persist discovery candidates
        for dc in discovery_by_market.get(market_id, []):
            match_rows.append(
                {
                    "market_id": market_id,
                    "signal_family_id": int(dc.signal_family_id),
                    "method": dc.method,
                    "matcher_version": str(matcher_version),
                    "match_strength": float(dc.score),
                    "evidence": json.dumps(dc.evidence, ensure_ascii=False),
                    "rationale": None,
                }
            )
            discovery_rows_written += 1
            best_lexical_by_family[int(dc.signal_family_id)].append((float(dc.score), market_id, dc.evidence))

        for dc in embedding_by_market.get(market_id, []):
            match_rows.append(
                {
                    "market_id": market_id,
                    "signal_family_id": int(dc.signal_family_id),
                    "method": dc.method,
                    "matcher_version": str(matcher_version),
                    "match_strength": float(dc.score),
                    "evidence": json.dumps(dc.evidence, ensure_ascii=False),
                    "rationale": None,
                }
            )
            discovery_rows_written += 1
            best_embedding_by_family[int(dc.signal_family_id)].append((float(dc.score), market_id, dc.evidence))

        # classify candidates (always persist attempts for audit)
        for fid in candidates_by_market.get(market_id, []):
            fam = family_by_id.get(int(fid))
            if fam is None:
                continue
            rule = RULES_BY_SLUG.get(fam.slug)
            if rule is None:
                continue
            rule_attempts_by_market[market_id] += 1
            dec = classify_with_rule(
                market_text=strict_text,
                family_slug=fam.slug,
                family_id=int(fid),
                rule=rule,
                min_score=float(classification_min_score),
            )
            classification_attempts_by_family[int(fid)].append(
                {
                    "market_id": market_id,
                    "question": m.question,
                    "event_title": m.event_title,
                    "rule_score": float(dec.rule_score),
                    "is_match": bool(dec.is_match),
                    "evidence": dec.evidence,
                    "volume_usd": m.volume_usd,
                }
            )
            if dec.is_match:
                match_rows.append(
                    {
                        "market_id": market_id,
                        "signal_family_id": int(fid),
                        "method": "rule_classification",
                        "matcher_version": str(matcher_version),
                        "match_strength": float(dec.rule_score),
                        "evidence": json.dumps(dec.evidence, ensure_ascii=False),
                        "rationale": None,
                    }
                )
                rule_rows_written += 1
                coverage_counts[int(fid)] += 1
                rule_matches_by_market[market_id] += 1

    upserted = _upsert_matches(db_url, match_rows)
    log.info("Upserted %s match rows (matcher_version=%s)", upserted, matcher_version)

    # Persist per-market evaluation diagnostics (optional).
    if audit_tables_ready:
        try:
            cache = DBEmbeddingCache(db_url=db_url)
            eval_rows: list[dict[str, Any]] = []
            n_with_lex = 0
            n_with_emb = 0
            n_with_any = 0

            for m in markets:
                mid = int(m.market_id)
                lex_cands = discovery_by_market.get(mid, []) or []
                emb_cands = embedding_by_market.get(mid, []) or []
                union = candidates_by_market.get(mid, []) or []

                if lex_cands:
                    n_with_lex += 1
                if emb_cands:
                    n_with_emb += 1
                if union:
                    n_with_any += 1

                lex_best = lexical_best_by_market.get(mid)
                lex_best_score = float(lex_best[0]) if lex_best is not None else 0.0
                lex_best_fid = int(lex_best[1]) if lex_best is not None else None

                emb_best = embedding_best_by_market.get(mid) or {}
                emb_best_sim = emb_best.get("best_similarity")
                emb_best_fid = emb_best.get("best_signal_family_id")

                mt = m.to_text()
                eval_rows.append(
                    {
                        "run_id": str(run_id),
                        "market_id": mid,
                        "market_text_hash": (
                            str(cache.key(model_name=str(embedding_model), text=mt)) if use_embeddings else ""
                        ),
                        "lexical_best_score": float(lex_best_score),
                        "lexical_best_signal_family_id": int(lex_best_fid) if lex_best_fid is not None else None,
                        "n_lexical_candidates": int(len(lex_cands)),
                        "embedding_best_similarity": float(emb_best_sim) if emb_best_sim is not None else None,
                        "embedding_best_signal_family_id": int(emb_best_fid) if emb_best_fid is not None else None,
                        "n_embedding_candidates": int(len(emb_cands)),
                        "n_union_candidates": int(len(union)),
                        "n_rule_attempts": int(rule_attempts_by_market.get(mid, 0)),
                        "n_rule_matches": int(rule_matches_by_market.get(mid, 0)),
                    }
                )

            conn_audit = connect(db_url)
            try:
                with conn_audit.cursor() as cur:
                    cur.executemany(
                        """
                        insert into pm_market_family_match_eval (
                          run_id,
                          market_id,
                          market_text_hash,
                          lexical_best_score,
                          lexical_best_signal_family_id,
                          n_lexical_candidates,
                          embedding_best_similarity,
                          embedding_best_signal_family_id,
                          n_embedding_candidates,
                          n_union_candidates,
                          n_rule_attempts,
                          n_rule_matches,
                          created_at
                        ) values (
                          %(run_id)s,
                          %(market_id)s,
                          %(market_text_hash)s,
                          %(lexical_best_score)s,
                          %(lexical_best_signal_family_id)s,
                          %(n_lexical_candidates)s,
                          %(embedding_best_similarity)s,
                          %(embedding_best_signal_family_id)s,
                          %(n_embedding_candidates)s,
                          %(n_union_candidates)s,
                          %(n_rule_attempts)s,
                          %(n_rule_matches)s,
                          now()
                        )
                        on conflict (run_id, market_id) do update set
                          market_text_hash = excluded.market_text_hash,
                          lexical_best_score = excluded.lexical_best_score,
                          lexical_best_signal_family_id = excluded.lexical_best_signal_family_id,
                          n_lexical_candidates = excluded.n_lexical_candidates,
                          embedding_best_similarity = excluded.embedding_best_similarity,
                          embedding_best_signal_family_id = excluded.embedding_best_signal_family_id,
                          n_embedding_candidates = excluded.n_embedding_candidates,
                          n_union_candidates = excluded.n_union_candidates,
                          n_rule_attempts = excluded.n_rule_attempts,
                          n_rule_matches = excluded.n_rule_matches;
                        """,
                        eval_rows,
                    )
                    cur.execute(
                        """
                        update pm_market_family_match_run
                        set
                          n_markets_evaluated = %(n_eval)s,
                          n_markets_with_any_candidate = %(n_any)s,
                          n_markets_with_lexical_candidate = %(n_lex)s,
                          n_markets_with_embedding_candidate = %(n_emb)s,
                          discovery_rows_written = %(disc_rows)s,
                          rule_attempt_rows_written = %(rule_attempts)s,
                          rule_match_rows_written = %(rule_rows)s
                        where run_id = %(run_id)s;
                        """,
                        {
                            "run_id": str(run_id),
                            "n_eval": int(len(markets)),
                            "n_any": int(n_with_any),
                            "n_lex": int(n_with_lex),
                            "n_emb": int(n_with_emb),
                            "disc_rows": int(discovery_rows_written),
                            "rule_attempts": int(sum(rule_attempts_by_market.values())),
                            "rule_rows": int(rule_rows_written),
                        },
                    )
                conn_audit.commit()
            finally:
                conn_audit.close()
        except Exception:
            pass

    # ----- Audit artifacts -----
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d_%H%M%S")

    # Coverage: count distinct markets with strict (rule) matches >= threshold.
    cov_rows: list[dict[str, Any]] = []
    for f in families:
        fid = int(f.signal_family_id)
        # Examples: a few top strict matches (by rule_score then volume) for quick sanity.
        attempts = classification_attempts_by_family.get(fid, [])
        strict = [a for a in attempts if bool(a.get("is_match"))]
        strict_sorted = sorted(
            strict,
            key=lambda a: (float(a.get("rule_score") or 0.0), float(a.get("volume_usd") or 0.0)),
            reverse=True,
        )
        examples = [str(a.get("question") or "") for a in strict_sorted[:3] if str(a.get("question") or "").strip()]
        cov_rows.append(
            {
                "slug": f.slug,
                "family_id": fid,
                "title": f.title,
                "matched_markets_rule": int(coverage_counts.get(fid, 0)),
                "matched_markets_discovery": int(len(discovery_markets_by_family.get(fid, set()))),
                "examples": " | ".join(examples),
            }
        )
    cov_rows_sorted = sorted(
        cov_rows,
        key=lambda r: (-int(r["matched_markets_rule"]), -int(r["matched_markets_discovery"]), str(r["slug"])),
    )
    cov_path = out_path / f"family_coverage_{stamp}.csv"
    with cov_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["slug", "family_id", "title", "matched_markets_rule", "matched_markets_discovery", "examples"],
        )
        w.writeheader()
        for r in cov_rows_sorted:
            w.writerow(r)

    # False-positive audit markdown: top + borderline per family.
    fp_lines: list[str] = []
    fp_lines.append("# False Positive Audit Snapshot (Step 3)")
    fp_lines.append("")
    fp_lines.append(f"- as_of_utc: `{now.isoformat()}`")
    fp_lines.append(f"- filter_version: `{filter_version}`")
    fp_lines.append(f"- matcher_version: `{matcher_version}`")
    fp_lines.append("")

    for f in families:
        fid = int(f.signal_family_id)
        attempts = classification_attempts_by_family.get(fid, [])
        strict = [a for a in attempts if bool(a.get("is_match"))]
        strict_sorted = sorted(strict, key=lambda a: (float(a.get("rule_score") or 0.0), float(a.get("volume_usd") or 0.0)), reverse=True)
        # Borderline discovery: high similarity from embeddings, but rule rejected.
        # (Helps distinguish retrieval failures vs rule strictness.)
        emb_sims = embedding_sim_by_family_market.get(fid, {})
        borderline_disc: list[dict[str, Any]] = []
        if emb_sims:
            for a in attempts:
                mid = int(a.get("market_id") or 0)
                if bool(a.get("is_match")):
                    continue
                sim = emb_sims.get(mid)
                if sim is None:
                    continue
                borderline_disc.append({**a, "similarity": float(sim)})
        borderline_disc_sorted = sorted(borderline_disc, key=lambda a: (float(a.get("similarity") or 0.0), float(a.get("rule_score") or 0.0)), reverse=True)

        fp_lines.append(f"## {f.title}")
        fp_lines.append(f"- slug: `{f.slug}`")
        fp_lines.append(f"- strict_matches: {len(strict_sorted)}")
        fp_lines.append("")

        fp_lines.append("### Top strict matches")
        if not strict_sorted:
            fp_lines.append("_No strict matches._")
        else:
            for a in strict_sorted[:10]:
                fp_lines.append(f"- ({a['rule_score']:.3f}) `{a['market_id']}` — {a['question']}")
                if a.get("event_title"):
                    fp_lines.append(f"  - event: {a['event_title']}")
                ev = a.get("evidence") or {}
                mt = ev.get("matched_terms") or []
                fp_lines.append(f"  - matched_terms: `{json.dumps(mt, ensure_ascii=False)}`")
        fp_lines.append("")

        fp_lines.append("### Borderline discovery (high similarity, rejected by rules)")
        if not borderline_disc_sorted:
            fp_lines.append("_None found (or embeddings disabled)._")
        else:
            for a in borderline_disc_sorted[:10]:
                fp_lines.append(
                    f"- (sim={float(a.get('similarity') or 0.0):.3f}, rule={float(a.get('rule_score') or 0.0):.3f}) "
                    f"`{a['market_id']}` — {a['question']}"
                )
                if a.get("event_title"):
                    fp_lines.append(f"  - event: {a['event_title']}")
                ev = a.get("evidence") or {}
                fp_lines.append(f"  - anchors_hit: `{json.dumps(ev.get('anchors_hit') or [], ensure_ascii=False)}`")
                fp_lines.append(f"  - keyword_hits: `{json.dumps(ev.get('keyword_hits') or [], ensure_ascii=False)}`")
                fp_lines.append(f"  - exclusions_hit: `{json.dumps(ev.get('exclusions_hit') or [], ensure_ascii=False)}`")
        fp_lines.append("")

    fp_path = out_path / f"false_positive_audit_{stamp}.md"
    fp_path.write_text("\n".join(fp_lines), encoding="utf-8")

    # Missing family diagnosis: show discovery candidates and rule failures.
    miss_lines: list[str] = []
    miss_lines.append("# Missing Family Diagnosis (Step 3)")
    miss_lines.append("")
    miss_lines.append(f"- as_of_utc: `{now.isoformat()}`")
    miss_lines.append(f"- filter_version: `{filter_version}`")
    miss_lines.append(f"- matcher_version: `{matcher_version}`")
    miss_lines.append("")

    for f in families:
        fid = int(f.signal_family_id)
        strict_n = int(coverage_counts.get(fid, 0))
        if strict_n > 0:
            continue
        miss_lines.append(f"## {f.title}")
        miss_lines.append(f"- slug: `{f.slug}`")
        miss_lines.append("")

        emb = sorted(best_embedding_by_family.get(fid, []), key=lambda t: t[0], reverse=True)[:10]
        lex = sorted(best_lexical_by_family.get(fid, []), key=lambda t: t[0], reverse=True)[:10]

        if not emb and not lex:
            miss_lines.append("_No discovery candidates found (embedding + lexical)._")
            miss_lines.append("")
            continue

        if emb:
            miss_lines.append("### Top discovery candidates (embedding)")
            for sim, mid, ev in emb:
                attempt = next(
                    (a for a in classification_attempts_by_family.get(fid, []) if int(a.get("market_id") or 0) == int(mid)),
                    None,
                )
                mrow = market_by_id.get(int(mid))
                q = (attempt.get("question") if attempt else None) or (mrow.question if mrow else "")
                et = (attempt.get("event_title") if attempt else None) or (mrow.event_title if mrow else None)
                miss_lines.append(f"- (sim={sim:.3f}) `{mid}` — {q}")
                if et:
                    miss_lines.append(f"  - event: {et}")
                if attempt:
                    miss_lines.append(f"  - rule_score: {float(attempt.get('rule_score') or 0.0):.3f}")
                    cev = attempt.get("evidence") or {}
                    miss_lines.append(f"  - anchors_hit: `{json.dumps(cev.get('anchors_hit') or [], ensure_ascii=False)}`")
                    miss_lines.append(f"  - keyword_hits: `{json.dumps(cev.get('keyword_hits') or [], ensure_ascii=False)}`")
                    miss_lines.append(f"  - exclusions_hit: `{json.dumps(cev.get('exclusions_hit') or [], ensure_ascii=False)}`")
                miss_lines.append(f"  - discovery_evidence: `{json.dumps(ev, ensure_ascii=False)}`")
            miss_lines.append("")

        if lex:
            miss_lines.append("### Top discovery candidates (lexical)")
            for score, mid, ev in lex:
                mrow = market_by_id.get(int(mid))
                q = mrow.question if mrow else ""
                et = mrow.event_title if mrow else None
                miss_lines.append(f"- (score={score:.3f}) `{mid}` — {q}")
                if et:
                    miss_lines.append(f"  - event: {et}")
                miss_lines.append(f"  - discovery_evidence: `{json.dumps(ev, ensure_ascii=False)}`")
            miss_lines.append("")

    miss_path = out_path / f"missing_family_diagnosis_{stamp}.md"
    miss_path.write_text("\n".join(miss_lines), encoding="utf-8")

    return {
        "filter_version": filter_version,
        "matcher_version": matcher_version,
        "n_markets_evaluated": len(markets),
        "discovery_candidates_written": int(discovery_rows_written),
        "rule_matches_written": int(rule_rows_written),
        "n_match_rows_upserted": int(upserted),
        "family_coverage_csv": str(cov_path),
        "false_positive_audit_md": str(fp_path),
        "missing_family_diagnosis_md": str(miss_path),
    }
