-- supabase/seed.sql
-- Seeds core BIT holdings (equities-only) from holdingschannel.com snapshot
-- Change period shown: 2025-09-30 to 2025-12-31

-- -------------------------
-- 1) Upsert securities
-- -------------------------
INSERT INTO bit_security (company_name, ticker, exchange_mic, country_iso2, currency_iso3)
VALUES
  ('IREN Limited',                         'IREN',  'XNAS', 'AU', 'USD'),
  ('Microsoft Corp',                       'MSFT',  'XNAS', 'US', 'USD'),
  ('Hinge Health Inc',                     'HNGE',  'XNAS', 'US', 'USD'),  -- verify ticker/exchange
  ('Alphabet Inc',                         'GOOGL', 'XNAS', 'US', 'USD'),
  ('Alphabet Inc',                         'GOOG',  'XNAS', 'US', 'USD'),
  ('Lemonade Inc',                         'LMND',  'XNYS', 'US', 'USD'),
  ('Reddit Inc',                           'RDDT',  'XNYS', 'US', 'USD'),
  ('Micron Technology Inc',                'MU',    'XNAS', 'US', 'USD'),
  ('Taiwan Semiconductor Mfg. Co. Ltd',     'TSM',   'XNYS', 'TW', 'USD'),
  ('Hut 8 Corp',                            'HUT',   'XNAS', 'US', 'USD'),
  ('Robinhood Markets Inc',                'HOOD',  'XNAS', 'US', 'USD'),
  ('Datadog Inc',                          'DDOG',  'XNAS', 'US', 'USD'),
  ('Oscar Health Inc',                     'OSCR',  'XNYS', 'US', 'USD'),
  ('Amazon.com Inc',                       'AMZN',  'XNAS', 'US', 'USD'),
  ('Kaspi.kz JSC',                         'KSPI',  'XNAS', 'KZ', 'USD'),
  ('Rubrik Inc',                           'RBRK',  'XNYS', 'US', 'USD'),
  ('NVIDIA Corp',                          'NVDA',  'XNAS', 'US', 'USD'),
  ('Meta Platforms Inc',                   'META',  'XNAS', 'US', 'USD'),
  ('Coinbase Global Inc',                  'COIN',  'XNAS', 'US', 'USD'),
  ('Bitmine Immersion Technologies Inc',   'BMNR',  'XNAS', 'US', 'USD')   -- verify ticker/exchange
ON CONFLICT (exchange_mic, ticker)
DO UPDATE SET
  company_name  = EXCLUDED.company_name,
  country_iso2  = EXCLUDED.country_iso2,
  currency_iso3 = EXCLUDED.currency_iso3,
  updated_at    = NOW();


-- -------------------------
-- 2) Upsert holdings snapshot
-- -------------------------
-- Columns in VALUES:
-- (exchange_mic, ticker, shares, change_shares, position_size_thousands)
INSERT INTO bit_holding (
  security_id,
  as_of,
  shares,
  total_value,
  value_currency,
  latest_change_side,
  latest_change_shares,
  latest_change_at,
  source_note,
  updated_at
)
SELECT
  s.id                                         AS security_id,
  '2025-12-31T00:00:00Z'::timestamptz           AS as_of,
  v.shares                                     AS shares,
  (v.position_k * 1000)::numeric(20,2)          AS total_value,
  'USD'                                        AS value_currency,
  CASE
    WHEN v.change_shares IS NULL THEN NULL
    WHEN v.change_shares > 0 THEN 'BUY'
    WHEN v.change_shares < 0 THEN 'SELL'
    ELSE NULL
  END                                          AS latest_change_side,
  CASE
    WHEN v.change_shares IS NULL THEN NULL
    WHEN v.change_shares = 0 THEN NULL
    ELSE ABS(v.change_shares)
  END                                          AS latest_change_shares,
  NULL::timestamptz                             AS latest_change_at,
  'holdingschannel.com; change 2025-09-30→2025-12-31' AS source_note,
  NOW()                                        AS updated_at
FROM (
  VALUES
    ('XNAS','IREN',   6941992::numeric,  1147765::numeric, 262199::numeric),
    ('XNAS','MSFT',     90092::numeric,    14845::numeric,  43570::numeric),
    ('XNAS','HNGE',   3316101::numeric,  1466577::numeric, 154033::numeric), -- verify ticker/exchange
    ('XNAS','GOOGL',   457908::numeric,   196208::numeric, 143325::numeric),
    ('XNAS','GOOG',    111000::numeric,  -153600::numeric,  34832::numeric),
    ('XNYS','LMND',   1826593::numeric,   572248::numeric, 130017::numeric),
    ('XNYS','RDDT',    563421::numeric,  -218584::numeric, 129514::numeric),
    ('XNAS','MU',      410683::numeric,    25724::numeric, 117213::numeric),
    ('XNYS','TSM',     382751::numeric,     4572::numeric, 116314::numeric),
    ('XNAS','HUT',    2087941::numeric,   -89570::numeric,  95920::numeric),
    ('XNAS','HOOD',    834578::numeric,   127087::numeric,  94391::numeric),
    ('XNAS','DDOG',    658321::numeric,   365684::numeric,  89525::numeric),
    ('XNYS','OSCR',   6186267::numeric,  5227152::numeric,  88897::numeric),
    ('XNAS','AMZN',    123987::numeric,    35514::numeric,  28619::numeric),
    ('XNAS','KSPI',   1014104::numeric,   134068::numeric,  79232::numeric),
    ('XNYS','RBRK',    910382::numeric,   326421::numeric,  69626::numeric),
    ('XNAS','NVDA',    381582::numeric,   -40723::numeric,  71165::numeric),
    ('XNAS','META',     95171::numeric,  -149214::numeric,  62821::numeric),
    ('XNAS','COIN',     53312::numeric,   -58829::numeric,  12056::numeric),
    ('XNAS','BMNR',    355139::numeric, -1439069::numeric,   9642::numeric)  -- verify ticker/exchange
) AS v(exchange_mic, ticker, shares, change_shares, position_k)
JOIN bit_security s
  ON s.exchange_mic = v.exchange_mic AND s.ticker = v.ticker
ON CONFLICT (security_id)
DO UPDATE SET
  as_of                = EXCLUDED.as_of,
  shares               = EXCLUDED.shares,
  total_value          = EXCLUDED.total_value,
  value_currency       = EXCLUDED.value_currency,
  latest_change_side   = EXCLUDED.latest_change_side,
  latest_change_shares = EXCLUDED.latest_change_shares,
  latest_change_at     = EXCLUDED.latest_change_at,
  source_note          = EXCLUDED.source_note,
  updated_at           = NOW();