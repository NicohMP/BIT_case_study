BEGIN;

-- =========================================================
-- Step 4: Deterministic market → security relevance scoring
-- =========================================================
-- Stores per-(security, market) relevance scores derived from:
-- - pm_market_signal_family_match (Step 3)
-- - signal_family_domain_influence (authority)
-- - bit_security_macro_domain_exposure (authority)
-- - pm_market_filter_decision.quality_score (optional multiplier)

CREATE TABLE IF NOT EXISTS pm_market_security_relevance (
    security_id BIGINT NOT NULL
        REFERENCES bit_security(id)
        ON DELETE CASCADE,
    market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,

    scoring_version TEXT NOT NULL,

    base_score DOUBLE PRECISION NOT NULL,
    quality_multiplier DOUBLE PRECISION NOT NULL,
    final_score DOUBLE PRECISION NOT NULL,

    score_breakdown JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (security_id, market_id, scoring_version)
);

CREATE INDEX IF NOT EXISTS ix_pmsr_security_rank
    ON pm_market_security_relevance(security_id, scoring_version, final_score DESC);

CREATE INDEX IF NOT EXISTS ix_pmsr_market
    ON pm_market_security_relevance(market_id, scoring_version);

CREATE INDEX IF NOT EXISTS ix_pmsr_created_at
    ON pm_market_security_relevance(created_at DESC);

COMMIT;

