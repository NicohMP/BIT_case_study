BEGIN;

-- ==========================================
-- Polymarket markets (normalized + raw JSON)
-- ==========================================
-- MVP goal:
-- - store the latest known state per market id
-- - keep `raw` so schema can evolve without data loss
CREATE TABLE IF NOT EXISTS pm_market (
    pm_market_id BIGINT PRIMARY KEY,

    question     TEXT NOT NULL,
    category     TEXT NULL,

    -- "current" snapshot fields (latest observed)
    probability  DOUBLE PRECISION NULL,
    volume_usd   DOUBLE PRECISION NULL,

    raw          JSONB NOT NULL,

    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pm_market_last_seen_at
    ON pm_market(last_seen_at DESC);

CREATE INDEX IF NOT EXISTS ix_pm_market_category
    ON pm_market(category);

COMMIT;

