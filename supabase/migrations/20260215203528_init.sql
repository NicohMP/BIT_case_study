BEGIN;

-- =========================
-- 1) Static security registry
-- =========================
CREATE TABLE IF NOT EXISTS bit_security (
    id              BIGSERIAL PRIMARY KEY,

    -- Identifiers
    company_name    TEXT NOT NULL,
    ticker          TEXT NOT NULL,
    exchange_mic    TEXT NOT NULL,          -- e.g., XNAS, XNYS, XETR (ISO 10383 MIC)
    isin            TEXT NULL,              -- e.g., US67066G1040

    -- Currency and region (optional)
    country_iso2    CHAR(2) NULL,           -- e.g., US, DE, FR
    currency_iso3   CHAR(3) NULL,           -- e.g., USD, EUR

    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Natural uniqueness: one security per (exchange, ticker)
CREATE UNIQUE INDEX IF NOT EXISTS uq_bit_security_ticker_exchange
    ON bit_security (exchange_mic, ticker);

-- ISIN is unique when present
CREATE UNIQUE INDEX IF NOT EXISTS uq_bit_security_isin
    ON bit_security (isin)
    WHERE isin IS NOT NULL;



-- =========================
-- 2) Current holdings snapshot (equities only)
--    One row per security currently tracked
-- =========================
CREATE TABLE IF NOT EXISTS bit_holding (
    security_id BIGINT PRIMARY KEY
        REFERENCES bit_security(id)
        ON DELETE RESTRICT,

    -- Snapshot timestamp (when this row was last updated)
    as_of TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Shares held (equities only)
    shares NUMERIC(20,6) NOT NULL DEFAULT 0,
    CONSTRAINT chk_shares_nonnegative CHECK (shares >= 0),

    -- Total holding value (optional, depending on what you have)
    total_value NUMERIC(20,2) NULL,
    value_currency CHAR(3) NULL, -- e.g., USD, EUR
    CONSTRAINT chk_total_value_nonnegative CHECK (total_value IS NULL OR total_value >= 0),

    -- Latest change metadata (optional)
    latest_change_side TEXT NULL CHECK (latest_change_side IN ('BUY', 'SELL')),
    latest_change_shares NUMERIC(20,6) NULL,
    latest_change_at TIMESTAMPTZ NULL,
    CONSTRAINT chk_latest_change_shares_positive CHECK (latest_change_shares IS NULL OR latest_change_shares > 0),

    -- Provenance / note
    source_note TEXT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_bit_holding_as_of
    ON bit_holding (as_of);

COMMIT;