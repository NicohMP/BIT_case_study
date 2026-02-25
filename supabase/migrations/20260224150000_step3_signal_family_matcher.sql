BEGIN;

-- ==========================================
--  Signal-family matching (v2 schema)
-- ==========================================
-- We keep the original `pm_market_signal_family_match` migration for history,
-- but rename the table to *_legacy and create a new evidence-rich, versioned
-- match table suitable for multi-method + audit.

DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name = 'pm_market_signal_family_match'
  ) AND NOT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name = 'pm_market_signal_family_match_legacy'
  ) THEN
    ALTER TABLE pm_market_signal_family_match RENAME TO pm_market_signal_family_match_legacy;
  END IF;
END $$;

-- New match table (versioned, multi-method)
CREATE TABLE IF NOT EXISTS pm_market_signal_family_match (
    market_id BIGINT NOT NULL
        REFERENCES pm_market(pm_market_id)
        ON DELETE CASCADE,
    signal_family_id BIGINT NOT NULL
        REFERENCES signal_family(id)
        ON DELETE CASCADE,

    method TEXT NOT NULL,
    matcher_version TEXT NOT NULL,

    match_strength DOUBLE PRECISION NOT NULL,
    CONSTRAINT chk_match_strength_0_1 CHECK (match_strength >= 0.0 AND match_strength <= 1.0),

    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    rationale TEXT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (market_id, signal_family_id, method, matcher_version)
);

CREATE INDEX IF NOT EXISTS ix_pmsfm_version
    ON pm_market_signal_family_match(matcher_version);

CREATE INDEX IF NOT EXISTS ix_pmsfm_family
    ON pm_market_signal_family_match(signal_family_id, matcher_version, method, match_strength desc);

CREATE INDEX IF NOT EXISTS ix_pmsfm_market
    ON pm_market_signal_family_match(market_id, matcher_version);

COMMIT;

BEGIN;

-- Optional: embedding cache (stored as jsonb list; cosine computed in Python).
CREATE TABLE IF NOT EXISTS pm_text_embedding_cache (
    text_hash TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    model_name TEXT NOT NULL,
    embedding JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pm_text_embedding_cache_model
    ON pm_text_embedding_cache(model_name);

COMMIT;

