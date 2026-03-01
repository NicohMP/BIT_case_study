BEGIN;

-- =========================================================
-- Step 4b: Persisted diversified top-K per security
-- =========================================================
-- Rationale:
-- Raw relevance scores are intentionally "truthy" and can be dominated by
-- template ladders (same event_id) or very generic macro/rate markets.
--
-- This table stores a deterministic, parameterized *selection* of top markets
-- per security for downstream consumption (WebUI / LLM), with constraints like:
-- - max markets per event_id
-- - max "rate-like" markets
--
-- Selection does not change the underlying pm_market_security_relevance scores.

CREATE TABLE IF NOT EXISTS pm_market_security_relevance_selection (
    security_id BIGINT NOT NULL
        REFERENCES bit_security(id)
        ON DELETE CASCADE,
    market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,

    scoring_version TEXT NOT NULL,
    selection_version TEXT NOT NULL,

    rank INTEGER NOT NULL,
    final_score DOUBLE PRECISION NOT NULL,

    event_id BIGINT NULL,
    is_rate_like BOOLEAN NOT NULL DEFAULT FALSE,

    selection_params JSONB NOT NULL DEFAULT '{}'::jsonb,
    selection_reason JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (security_id, market_id, scoring_version, selection_version),
    UNIQUE (security_id, scoring_version, selection_version, rank)
);

CREATE INDEX IF NOT EXISTS ix_pmsrs_security_rank
    ON pm_market_security_relevance_selection(security_id, scoring_version, selection_version, rank ASC);

CREATE INDEX IF NOT EXISTS ix_pmsrs_market
    ON pm_market_security_relevance_selection(market_id, scoring_version, selection_version);

CREATE INDEX IF NOT EXISTS ix_pmsrs_updated_at
    ON pm_market_security_relevance_selection(updated_at DESC);

COMMIT;

