BEGIN;

-- ==========================================
-- Security → macro_domain exposure weights (authority layer)
-- ==========================================
-- Purpose:
-- - Express how much each BIT security is exposed to each macro domain (industry segment).
-- - Used by the deterministic relevance engine:
--     relevance(market, security) = Σ_f Σ_d match(market→family_f) × influence(family_f→domain_d) × exposure(security→domain_d)
--
-- Notes:
-- - We keep this separate from `bit_security_domain` (which is unweighted and references `bit_domain`).
-- - We cannot enforce "weights sum to 1.0 per security" via a simple CHECK constraint, so we add a
--   DEFERRABLE constraint trigger to enforce it at transaction commit.

CREATE TABLE IF NOT EXISTS bit_security_macro_domain_exposure (
    security_id BIGINT NOT NULL
        REFERENCES bit_security(id)
        ON DELETE CASCADE,
    macro_domain_id BIGINT NOT NULL
        REFERENCES macro_domain(id)
        ON DELETE CASCADE,

    weight DOUBLE PRECISION NOT NULL,
    CONSTRAINT chk_bit_security_macro_domain_exposure_weight_0_1 CHECK (weight >= 0.0 AND weight <= 1.0),

    -- Auditability
    weight_basis TEXT NOT NULL DEFAULT 'revenue'
        CHECK (weight_basis IN ('revenue', 'operating_income', 'custom')),
    source_ref TEXT NOT NULL DEFAULT '',
    as_of_date DATE NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (security_id, macro_domain_id)
);

CREATE INDEX IF NOT EXISTS ix_bit_security_macro_domain_exposure_security
    ON bit_security_macro_domain_exposure(security_id);

CREATE INDEX IF NOT EXISTS ix_bit_security_macro_domain_exposure_domain
    ON bit_security_macro_domain_exposure(macro_domain_id);

-- =========================
-- Enforce sum(weights)=1 per security (deferred)
-- =========================
-- This constraint is enforced at COMMIT time (INITIALLY DEFERRED), so callers can
-- insert multiple rows for a security within one transaction.

CREATE OR REPLACE FUNCTION fn_check_security_exposure_weights_sum()
RETURNS TRIGGER AS $$
DECLARE
  sid BIGINT;
  total DOUBLE PRECISION;
BEGIN
  sid := COALESCE(NEW.security_id, OLD.security_id);

  SELECT COALESCE(SUM(weight), 0.0)
    INTO total
  FROM bit_security_macro_domain_exposure
  WHERE security_id = sid;

  -- Allow a small tolerance for floating point weights.
  IF total < 0.999 OR total > 1.001 THEN
    RAISE EXCEPTION 'Exposure weights for security_id=% must sum to 1.0 (got %)', sid, total;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
  -- Avoid duplicate triggers if migrations are re-run.
  IF NOT EXISTS (
    SELECT 1
    FROM pg_trigger
    WHERE tgname = 'trg_check_security_exposure_weights_sum'
  ) THEN
    CREATE CONSTRAINT TRIGGER trg_check_security_exposure_weights_sum
    AFTER INSERT OR UPDATE OR DELETE ON bit_security_macro_domain_exposure
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW
    EXECUTE FUNCTION fn_check_security_exposure_weights_sum();
  END IF;
END $$;

-- =========================
-- MVP seed exposures (single-domain, weight=1.0) for seeded holdings
-- =========================
-- These are intentionally simple case-study defaults to enable end-to-end scoring.
-- Adjust to multi-domain revenue splits as you refine the knowledge base.

WITH sec AS (
  SELECT id, ticker FROM bit_security
),
dom AS (
  SELECT id, name FROM macro_domain
),
rows AS (
  SELECT s.id AS security_id, d.id AS macro_domain_id, 1.0::double precision AS weight,
         'custom'::text AS weight_basis,
         'case-study heuristic (single-domain default)'::text AS source_ref,
         '2025-12-31'::date AS as_of_date
  FROM sec s
  JOIN dom d ON (
    (s.ticker IN ('MSFT','GOOGL','GOOG','META') AND d.name = 'AI & Big Tech') OR
    (s.ticker IN ('NVDA','MU','TSM') AND d.name = 'Semis & Compute') OR
    (s.ticker IN ('AMZN','DDOG','RBRK') AND d.name = 'Cloud / Dev') OR
    (s.ticker IN ('COIN','HUT','IREN','BMNR') AND d.name = 'Crypto Infra') OR
    (s.ticker IN ('HOOD','KSPI','LMND') AND d.name = 'Fintech / CFP') OR
    (s.ticker IN ('HNGE','OSCR') AND d.name = 'Digital Health')
  )
)
INSERT INTO bit_security_macro_domain_exposure (
  security_id,
  macro_domain_id,
  weight,
  weight_basis,
  source_ref,
  as_of_date
)
SELECT security_id, macro_domain_id, weight, weight_basis, source_ref, as_of_date
FROM rows
ON CONFLICT (security_id, macro_domain_id) DO UPDATE SET
  weight = EXCLUDED.weight,
  weight_basis = EXCLUDED.weight_basis,
  source_ref = EXCLUDED.source_ref,
  as_of_date = EXCLUDED.as_of_date,
  updated_at = NOW();

COMMIT;

