BEGIN;

-- ==========================================
-- Step 3 audit tables: matching runs + per-market evaluation stats
-- ==========================================
-- Purpose:
-- - Make Step 3 (discovery + rules) debuggable without guesswork.
-- - Persist threshold diagnostics even when no candidates are written.
--
-- This avoids the "silent failure" mode where only markets above thresholds are stored
-- in `pm_market_signal_family_match`, making it hard to tell if thresholds are too strict
-- or embeddings/keywords aren't working.

CREATE TABLE IF NOT EXISTS pm_market_family_match_run (
    run_id UUID PRIMARY KEY,
    filter_version TEXT NOT NULL,
    matcher_version TEXT NOT NULL,

    params JSONB NOT NULL DEFAULT '{}'::jsonb,

    n_markets_evaluated INTEGER NOT NULL DEFAULT 0,
    n_markets_with_any_candidate INTEGER NOT NULL DEFAULT 0,
    n_markets_with_lexical_candidate INTEGER NOT NULL DEFAULT 0,
    n_markets_with_embedding_candidate INTEGER NOT NULL DEFAULT 0,
    discovery_rows_written INTEGER NOT NULL DEFAULT 0,
    rule_attempt_rows_written INTEGER NOT NULL DEFAULT 0,
    rule_match_rows_written INTEGER NOT NULL DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pm_market_family_match_run_versions
    ON pm_market_family_match_run(filter_version, matcher_version, created_at desc);

CREATE TABLE IF NOT EXISTS pm_market_family_match_eval (
    run_id UUID NOT NULL
        REFERENCES pm_market_family_match_run(run_id)
        ON DELETE CASCADE,
    market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,

    market_text_hash TEXT NOT NULL DEFAULT '',

    lexical_best_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    lexical_best_signal_family_id BIGINT NULL
        REFERENCES signal_family(id)
        ON DELETE SET NULL,
    n_lexical_candidates INTEGER NOT NULL DEFAULT 0,

    embedding_best_similarity DOUBLE PRECISION NULL,
    embedding_best_signal_family_id BIGINT NULL
        REFERENCES signal_family(id)
        ON DELETE SET NULL,
    n_embedding_candidates INTEGER NOT NULL DEFAULT 0,

    n_union_candidates INTEGER NOT NULL DEFAULT 0,
    n_rule_attempts INTEGER NOT NULL DEFAULT 0,
    n_rule_matches INTEGER NOT NULL DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (run_id, market_id)
);

CREATE INDEX IF NOT EXISTS ix_pm_market_family_match_eval_run
    ON pm_market_family_match_eval(run_id);

CREATE INDEX IF NOT EXISTS ix_pm_market_family_match_eval_market
    ON pm_market_family_match_eval(market_id);

COMMIT;

