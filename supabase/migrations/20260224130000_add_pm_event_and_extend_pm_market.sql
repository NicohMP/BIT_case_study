BEGIN;

-- ==========================================
-- Polymarket events (normalized + raw JSON)
-- ==========================================
-- Purpose:
-- - Ingest complete coverage via Gamma `/events` pagination
-- - Persist event metadata and raw payloads for debugging
CREATE TABLE IF NOT EXISTS pm_event (
    event_id      BIGINT PRIMARY KEY,

    slug          TEXT NULL,
    title         TEXT NULL,
    active        BOOLEAN NULL,
    closed        BOOLEAN NULL,

    start_date    TIMESTAMPTZ NULL,
    end_date      TIMESTAMPTZ NULL,

    volume_usd    DOUBLE PRECISION NULL,
    liquidity_usd DOUBLE PRECISION NULL,

    tags          JSONB NOT NULL DEFAULT '[]'::jsonb,
    raw_event     JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Source timestamp if provided by the API; not guaranteed
    updated_at    TIMESTAMPTZ NULL,

    ingested_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_pm_event_active_closed
    ON pm_event(active, closed);

COMMIT;

BEGIN;

-- ==========================================
-- Extend pm_market for event-based ingestion
-- ==========================================

-- Rename `raw` -> `raw_market` (legacy schema used `raw`)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'pm_market'
      AND column_name = 'raw'
  ) AND NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'pm_market'
      AND column_name = 'raw_market'
  ) THEN
    ALTER TABLE pm_market RENAME COLUMN raw TO raw_market;
  END IF;
END $$;

ALTER TABLE pm_market
    ADD COLUMN IF NOT EXISTS event_id BIGINT NULL,
    ADD COLUMN IF NOT EXISTS slug TEXT NULL,
    ADD COLUMN IF NOT EXISTS active BOOLEAN NULL,
    ADD COLUMN IF NOT EXISTS closed BOOLEAN NULL,
    ADD COLUMN IF NOT EXISTS end_date TIMESTAMPTZ NULL,
    ADD COLUMN IF NOT EXISTS liquidity_usd DOUBLE PRECISION NULL,
    ADD COLUMN IF NOT EXISTS outcomes JSONB NULL,
    ADD COLUMN IF NOT EXISTS tokens JSONB NULL,
    ADD COLUMN IF NOT EXISTS prices JSONB NULL,
    ADD COLUMN IF NOT EXISTS probabilities JSONB NULL,
    ADD COLUMN IF NOT EXISTS tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS raw_market JSONB NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

-- Keep raw_market non-null and defaulted (covers rename path too)
ALTER TABLE pm_market
    ALTER COLUMN raw_market SET DEFAULT '{}'::jsonb;

-- Optional FK: allow NULL for legacy rows
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'fk_pm_market_event'
  ) THEN
    ALTER TABLE pm_market
      ADD CONSTRAINT fk_pm_market_event
      FOREIGN KEY (event_id)
      REFERENCES pm_event(event_id)
      ON DELETE SET NULL;
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS ix_pm_market_event_id
    ON pm_market(event_id);

COMMIT;

