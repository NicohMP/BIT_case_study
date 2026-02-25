BEGIN;

-- ==========================================
-- Hard-filter decisions (auditable artifacts)
-- ==========================================
-- One row per (market, filter_version). This allows repeatable experiments:
-- - You can bump `filter_version` when rules change
-- - Re-running for the same version is idempotent (upsert)

CREATE TABLE IF NOT EXISTS pm_market_filter_decision (
    market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,

    filter_version TEXT NOT NULL,

    is_rejected BOOLEAN NOT NULL,
    template_score DOUBLE PRECISION NULL,
    equity_relevance_score DOUBLE PRECISION NULL,
    quality_score DOUBLE PRECISION NULL,

    rejection_reasons TEXT[] NOT NULL DEFAULT ARRAY[]::text[],
    keep_reasons TEXT[] NOT NULL DEFAULT ARRAY[]::text[],

    decided_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (market_id, filter_version)
);

CREATE INDEX IF NOT EXISTS ix_pm_market_filter_decision_version
    ON pm_market_filter_decision(filter_version);

CREATE INDEX IF NOT EXISTS ix_pm_market_filter_decision_rejected
    ON pm_market_filter_decision(filter_version, is_rejected);

COMMIT;

BEGIN;

-- Optional run-level stats (written by the filter runner script)
CREATE TABLE IF NOT EXISTS pm_market_filter_stats (
    run_id UUID PRIMARY KEY,
    filter_version TEXT NOT NULL,
    config_sha256 TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    n_evaluated BIGINT NOT NULL DEFAULT 0,
    n_rejected BIGINT NOT NULL DEFAULT 0,

    top_reasons JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_pm_market_filter_stats_created_at
    ON pm_market_filter_stats(created_at desc);

COMMIT;

