BEGIN;

-- Seed a small, predefined security universe for the case-study demo.
--
-- Why this exists:
-- - `supabase db reset` recreates an empty DB and replays migrations.
-- - Later migrations (e.g. security→domain exposure weights) assume these `bit_security`
--   rows exist and will fail fast if they don't.
--
-- This keeps the local demo reproducible for reviewers.

INSERT INTO bit_security (
  company_name,
  ticker,
  exchange_mic,
  country_iso2,
  currency_iso3,
  created_at,
  updated_at
)
VALUES
  ('IREN Limited', 'IREN', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Microsoft Corp', 'MSFT', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Hinge Health Inc', 'HNGE', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('Alphabet Inc', 'GOOG', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Alphabet Inc', 'GOOGL', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Lemonade Inc', 'LMND', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('Reddit Inc', 'RDDT', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('Micron Technology Inc', 'MU', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Taiwan Semiconductor Mfg. Co. Ltd', 'TSM', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('Hut 8 Corp', 'HUT', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Robinhood Markets Inc', 'HOOD', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Datadog Inc', 'DDOG', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Oscar Health Inc', 'OSCR', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('Amazon.com Inc', 'AMZN', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Kaspi.kz JSC', 'KSPI', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Rubrik Inc', 'RBRK', 'XNYS', 'US', 'USD', NOW(), NOW()),
  ('NVIDIA Corp', 'NVDA', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Meta Platforms Inc', 'META', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Coinbase Global Inc', 'COIN', 'XNAS', 'US', 'USD', NOW(), NOW()),
  ('Bitmine Immersion Technologies Inc', 'BMNR', 'XNAS', 'US', 'USD', NOW(), NOW())
ON CONFLICT (exchange_mic, ticker) DO UPDATE SET
  company_name = EXCLUDED.company_name,
  country_iso2 = EXCLUDED.country_iso2,
  currency_iso3 = EXCLUDED.currency_iso3,
  updated_at = NOW();

COMMIT;

