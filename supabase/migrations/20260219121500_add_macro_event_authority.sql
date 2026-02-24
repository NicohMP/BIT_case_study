BEGIN;

-- ==========================================
-- Macro-event "authority layer" (MVP)
-- ==========================================
-- This schema represents a curated library of macro events ("signal families")
-- and an influence matrix that scores how strongly each event affects each
-- industry segment (domain) of interest.
--
-- Design notes:
-- - We keep this taxonomy separate from `bit_domain` for now, because the
--   domains used in `event_domain_scores.md` don't necessarily match the BIT
--   domain taxonomy one-to-one.
-- - The influence matrix is stored as a normalized join table for queryability.
--   You can always render it as a matrix via a view or in pandas.

CREATE TABLE IF NOT EXISTS macro_domain (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS macro_event (
    id BIGSERIAL PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS macro_event_domain_influence (
    macro_event_id BIGINT NOT NULL
        REFERENCES macro_event(id)
        ON DELETE CASCADE,
    macro_domain_id BIGINT NOT NULL
        REFERENCES macro_domain(id)
        ON DELETE CASCADE,

    score SMALLINT NOT NULL,
    CONSTRAINT chk_macro_event_domain_score_0_5 CHECK (score >= 0 AND score <= 5),

    -- Optional for now: you can backfill from `event_domain_rationale.md`
    rationale_md TEXT NOT NULL DEFAULT '',
    sources JSONB NOT NULL DEFAULT '[]'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (macro_event_id, macro_domain_id)
);

CREATE INDEX IF NOT EXISTS ix_macro_event_domain_influence_event
    ON macro_event_domain_influence(macro_event_id);

CREATE INDEX IF NOT EXISTS ix_macro_event_domain_influence_domain
    ON macro_event_domain_influence(macro_domain_id);

-- ==========================================
-- Seed domains (columns of `event_domain_scores.md`)
-- ==========================================
INSERT INTO macro_domain (name) VALUES
  ('AI & Big Tech'),
  ('Semis & Compute'),
  ('Cloud / Dev'),
  ('Crypto Infra'),
  ('Fintech / CFP'),
  ('Digital Health')
ON CONFLICT (name) DO NOTHING;

-- ==========================================
-- Seed macro events (rows of `event_domain_scores.md`)
-- ==========================================
INSERT INTO macro_event (slug, title) VALUES
  ('fomc_surprises', 'Monetary policy surprises (FOMC)'),
  ('real_yields_long_rates', 'Real yields / long rates'),
  ('us_china_semis_export_controls', 'US–China semiconductor export controls'),
  ('taiwan_geopolitical_risk', 'Taiwan geopolitical risk'),
  ('crypto_regime_changes', 'Crypto regulation regime changes'),
  ('ai_regulation_big_tech_enforcement', 'AI regulation + Big Tech enforcement'),
  ('datacenter_power_grid_constraints', 'Data-center power / grid constraints'),
  ('antitrust_platforms_app_stores_ads', 'Antitrust (platforms, app stores, ad markets)'),
  ('it_spending_cycle_enterprise_cloud_ai', 'IT spending cycle (enterprise / cloud / AI)'),
  ('healthcare_policy_reimbursement', 'Healthcare policy (reform, reimbursement)'),
  ('consumer_credit_conditions_cycle', 'Consumer credit conditions / cycle')
ON CONFLICT (slug) DO NOTHING;

-- ==========================================
-- Seed influence scores (0..5) from `event_domain_scores.md`
-- ==========================================
WITH e AS (
  SELECT id, title FROM macro_event
),
d AS (
  SELECT id, name FROM macro_domain
)
INSERT INTO macro_event_domain_influence (macro_event_id, macro_domain_id, score)
SELECT e.id, d.id, x.score
FROM (VALUES
  -- 1) Monetary policy surprises (FOMC)
  ('Monetary policy surprises (FOMC)', 'AI & Big Tech', 5),
  ('Monetary policy surprises (FOMC)', 'Semis & Compute', 3),
  ('Monetary policy surprises (FOMC)', 'Cloud / Dev', 5),
  ('Monetary policy surprises (FOMC)', 'Crypto Infra', 3),
  ('Monetary policy surprises (FOMC)', 'Fintech / CFP', 4),
  ('Monetary policy surprises (FOMC)', 'Digital Health', 3),

  -- 2) Real yields / long rates
  ('Real yields / long rates', 'AI & Big Tech', 5),
  ('Real yields / long rates', 'Semis & Compute', 3),
  ('Real yields / long rates', 'Cloud / Dev', 5),
  ('Real yields / long rates', 'Crypto Infra', 3),
  ('Real yields / long rates', 'Fintech / CFP', 3),
  ('Real yields / long rates', 'Digital Health', 3),

  -- 3) US–China semiconductor export controls
  ('US–China semiconductor export controls', 'AI & Big Tech', 3),
  ('US–China semiconductor export controls', 'Semis & Compute', 5),
  ('US–China semiconductor export controls', 'Cloud / Dev', 3),
  ('US–China semiconductor export controls', 'Crypto Infra', 2),
  ('US–China semiconductor export controls', 'Fintech / CFP', 0),
  ('US–China semiconductor export controls', 'Digital Health', 0),

  -- 4) Taiwan geopolitical risk
  ('Taiwan geopolitical risk', 'AI & Big Tech', 3),
  ('Taiwan geopolitical risk', 'Semis & Compute', 5),
  ('Taiwan geopolitical risk', 'Cloud / Dev', 3),
  ('Taiwan geopolitical risk', 'Crypto Infra', 2),
  ('Taiwan geopolitical risk', 'Fintech / CFP', 1),
  ('Taiwan geopolitical risk', 'Digital Health', 1),

  -- 5) Crypto regulation regime changes
  ('Crypto regulation regime changes', 'AI & Big Tech', 1),
  ('Crypto regulation regime changes', 'Semis & Compute', 0),
  ('Crypto regulation regime changes', 'Cloud / Dev', 1),
  ('Crypto regulation regime changes', 'Crypto Infra', 5),
  ('Crypto regulation regime changes', 'Fintech / CFP', 3),
  ('Crypto regulation regime changes', 'Digital Health', 0),

  -- 6) AI regulation + Big Tech enforcement
  ('AI regulation + Big Tech enforcement', 'AI & Big Tech', 5),
  ('AI regulation + Big Tech enforcement', 'Semis & Compute', 2),
  ('AI regulation + Big Tech enforcement', 'Cloud / Dev', 4),
  ('AI regulation + Big Tech enforcement', 'Crypto Infra', 0),
  ('AI regulation + Big Tech enforcement', 'Fintech / CFP', 1),
  ('AI regulation + Big Tech enforcement', 'Digital Health', 3),

  -- 7) Data-center power / grid constraints
  ('Data-center power / grid constraints', 'AI & Big Tech', 4),
  ('Data-center power / grid constraints', 'Semis & Compute', 3),
  ('Data-center power / grid constraints', 'Cloud / Dev', 4),
  ('Data-center power / grid constraints', 'Crypto Infra', 5),
  ('Data-center power / grid constraints', 'Fintech / CFP', 1),
  ('Data-center power / grid constraints', 'Digital Health', 1),

  -- 8) Antitrust (platforms, app stores, ad markets)
  ('Antitrust (platforms, app stores, ad markets)', 'AI & Big Tech', 5),
  ('Antitrust (platforms, app stores, ad markets)', 'Semis & Compute', 1),
  ('Antitrust (platforms, app stores, ad markets)', 'Cloud / Dev', 3),
  ('Antitrust (platforms, app stores, ad markets)', 'Crypto Infra', 0),
  ('Antitrust (platforms, app stores, ad markets)', 'Fintech / CFP', 2),
  ('Antitrust (platforms, app stores, ad markets)', 'Digital Health', 1),

  -- 9) IT spending cycle (enterprise / cloud / AI)
  ('IT spending cycle (enterprise / cloud / AI)', 'AI & Big Tech', 3),
  ('IT spending cycle (enterprise / cloud / AI)', 'Semis & Compute', 3),
  ('IT spending cycle (enterprise / cloud / AI)', 'Cloud / Dev', 4),
  ('IT spending cycle (enterprise / cloud / AI)', 'Crypto Infra', 1),
  ('IT spending cycle (enterprise / cloud / AI)', 'Fintech / CFP', 1),
  ('IT spending cycle (enterprise / cloud / AI)', 'Digital Health', 3),

  -- 10) Healthcare policy (reform, reimbursement)
  ('Healthcare policy (reform, reimbursement)', 'AI & Big Tech', 1),
  ('Healthcare policy (reform, reimbursement)', 'Semis & Compute', 0),
  ('Healthcare policy (reform, reimbursement)', 'Cloud / Dev', 0),
  ('Healthcare policy (reform, reimbursement)', 'Crypto Infra', 0),
  ('Healthcare policy (reform, reimbursement)', 'Fintech / CFP', 1),
  ('Healthcare policy (reform, reimbursement)', 'Digital Health', 5),

  -- 11) Consumer credit conditions / cycle
  ('Consumer credit conditions / cycle', 'AI & Big Tech', 1),
  ('Consumer credit conditions / cycle', 'Semis & Compute', 0),
  ('Consumer credit conditions / cycle', 'Cloud / Dev', 0),
  ('Consumer credit conditions / cycle', 'Crypto Infra', 2),
  ('Consumer credit conditions / cycle', 'Fintech / CFP', 5),
  ('Consumer credit conditions / cycle', 'Digital Health', 1)
) AS x(event_title, domain_name, score)
JOIN e ON e.title = x.event_title
JOIN d ON d.name = x.domain_name
ON CONFLICT (macro_event_id, macro_domain_id) DO UPDATE SET
  score = EXCLUDED.score,
  updated_at = NOW();

COMMIT;

