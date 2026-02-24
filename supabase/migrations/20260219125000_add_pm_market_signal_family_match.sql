BEGIN;

-- ==========================================
-- Link Polymarket markets -> signal families
-- ==========================================
-- Purpose:
-- - Persist matching decisions (debuggable, iterative)
-- - Enable report generation without recomputing everything each time

CREATE TABLE IF NOT EXISTS pm_market_signal_family_match (
    pm_market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,
    signal_family_id BIGINT NOT NULL
        REFERENCES signal_family(id)
        ON DELETE CASCADE,

    match_method TEXT NOT NULL DEFAULT 'keyword',
    match_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    CONSTRAINT chk_match_score_0_1 CHECK (match_score >= 0.0 AND match_score <= 1.0),

    matched_terms JSONB NOT NULL DEFAULT '[]'::jsonb,
    match_rationale TEXT NOT NULL DEFAULT '',

    matched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (pm_market_id, signal_family_id)
);

CREATE INDEX IF NOT EXISTS ix_pm_market_signal_family_match_family
    ON pm_market_signal_family_match(signal_family_id);

CREATE INDEX IF NOT EXISTS ix_pm_market_signal_family_match_market
    ON pm_market_signal_family_match(pm_market_id);

CREATE INDEX IF NOT EXISTS ix_pm_market_signal_family_match_score
    ON pm_market_signal_family_match(match_score DESC);

COMMIT;

