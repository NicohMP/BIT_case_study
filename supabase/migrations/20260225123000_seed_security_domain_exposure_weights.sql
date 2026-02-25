BEGIN;

-- Seed/override security→macro_domain exposure weights from `security_domain_exposure_scores.md`.
--
-- Source scale (0–3): 0=none, 1=peripheral, 2=material, 3=core/dominant.
-- We convert scores to weights by normalizing per security:
--   weight(domain) = score(domain) / sum_scores(security)
--
-- Notes:
-- - `bit_security.company_name` is the authority key; this supports multiple tickers per company (e.g. GOOG/GOOGL).
-- - We delete existing exposure rows for matched securities and replace with these normalized weights.
-- - We only insert domains with score > 0 (weights still sum to 1.0).

DO $$
DECLARE
  missing_companies INT;
  missing_domains INT;
BEGIN
  WITH scores(company_name) AS (
    VALUES
      ('IREN Limited'),
      ('Microsoft Corp'),
      ('Hinge Health Inc'),
      ('Alphabet Inc'),
      ('Lemonade Inc'),
      ('Reddit Inc'),
      ('Micron Technology Inc'),
      ('Taiwan Semiconductor Mfg. Co. Ltd'),
      ('Hut 8 Corp'),
      ('Robinhood Markets Inc'),
      ('Datadog Inc'),
      ('Oscar Health Inc'),
      ('Amazon.com Inc'),
      ('Kaspi.kz JSC'),
      ('Rubrik Inc'),
      ('NVIDIA Corp'),
      ('Meta Platforms Inc'),
      ('Coinbase Global Inc'),
      ('Bitmine Immersion Technologies Inc')
  )
  SELECT COUNT(*)
    INTO missing_companies
  FROM scores sc
  LEFT JOIN bit_security s
    ON s.company_name = sc.company_name
  WHERE s.id IS NULL;

  IF missing_companies > 0 THEN
    RAISE EXCEPTION 'security_domain_exposure_scores.md: % company_name values not found in bit_security.company_name', missing_companies;
  END IF;

  WITH required(name) AS (
    VALUES
      ('AI & Big Tech'),
      ('Semis & Compute'),
      ('Cloud / Dev'),
      ('Crypto Infra'),
      ('Fintech / CFP'),
      ('Digital Health')
  )
  SELECT COUNT(*)
    INTO missing_domains
  FROM required r
  LEFT JOIN macro_domain d
    ON d.name = r.name
  WHERE d.id IS NULL;

  IF missing_domains > 0 THEN
    RAISE EXCEPTION 'Required macro_domain rows are missing: %', missing_domains;
  END IF;
END $$;

WITH scores(company_name, ai_big_tech, semis_compute, cloud_dev, crypto_infra, fintech_cfp, digital_health) AS (
  VALUES
    ('IREN Limited', 2, 2, 1, 2, 0, 0),
    ('Microsoft Corp', 2, 1, 3, 0, 1, 0),
    ('Hinge Health Inc', 1, 0, 1, 0, 0, 3),
    ('Alphabet Inc', 2, 1, 2, 0, 0, 0),
    ('Lemonade Inc', 1, 0, 0, 0, 3, 0),
    ('Reddit Inc', 1, 0, 1, 0, 0, 0),
    ('Micron Technology Inc', 1, 3, 0, 1, 0, 0),
    ('Taiwan Semiconductor Mfg. Co. Ltd', 1, 3, 0, 1, 0, 0),
    ('Hut 8 Corp', 0, 1, 1, 3, 0, 0),
    ('Robinhood Markets Inc', 0, 0, 1, 1, 3, 0),
    ('Datadog Inc', 1, 0, 3, 0, 0, 0),
    ('Oscar Health Inc', 1, 0, 0, 0, 1, 3),
    ('Amazon.com Inc', 1, 1, 3, 0, 1, 0),
    ('Kaspi.kz JSC', 0, 0, 1, 0, 3, 0),
    ('Rubrik Inc', 1, 0, 3, 0, 0, 0),
    ('NVIDIA Corp', 2, 3, 1, 1, 0, 0),
    ('Meta Platforms Inc', 2, 1, 1, 0, 0, 0),
    ('Coinbase Global Inc', 0, 0, 1, 3, 2, 0),
    ('Bitmine Immersion Technologies Inc', 0, 1, 0, 3, 0, 0)
),
matched AS (
  SELECT
    s.id AS security_id,
    sc.company_name,
    sc.ai_big_tech,
    sc.semis_compute,
    sc.cloud_dev,
    sc.crypto_infra,
    sc.fintech_cfp,
    sc.digital_health
  FROM scores sc
  JOIN bit_security s
    ON s.company_name = sc.company_name
),
expanded AS (
  SELECT security_id, 'AI & Big Tech'::text AS domain_name, ai_big_tech::int AS score FROM matched
  UNION ALL
  SELECT security_id, 'Semis & Compute'::text, semis_compute::int FROM matched
  UNION ALL
  SELECT security_id, 'Cloud / Dev'::text, cloud_dev::int FROM matched
  UNION ALL
  SELECT security_id, 'Crypto Infra'::text, crypto_infra::int FROM matched
  UNION ALL
  SELECT security_id, 'Fintech / CFP'::text, fintech_cfp::int FROM matched
  UNION ALL
  SELECT security_id, 'Digital Health'::text, digital_health::int FROM matched
),
totals AS (
  SELECT security_id, SUM(score)::int AS total_score
  FROM expanded
  GROUP BY security_id
),
target AS (
  SELECT security_id
  FROM totals
  WHERE total_score > 0
),
weights AS (
  SELECT
    e.security_id,
    d.id AS macro_domain_id,
    (e.score::double precision / t.total_score::double precision) AS weight
  FROM expanded e
  JOIN totals t
    ON t.security_id = e.security_id
  JOIN macro_domain d
    ON d.name = e.domain_name
  WHERE e.score > 0
    AND t.total_score > 0
)
DELETE FROM bit_security_macro_domain_exposure x
WHERE x.security_id IN (SELECT security_id FROM target);

WITH scores(company_name, ai_big_tech, semis_compute, cloud_dev, crypto_infra, fintech_cfp, digital_health) AS (
  VALUES
    ('IREN Limited', 2, 2, 1, 2, 0, 0),
    ('Microsoft Corp', 2, 1, 3, 0, 1, 0),
    ('Hinge Health Inc', 1, 0, 1, 0, 0, 3),
    ('Alphabet Inc', 2, 1, 2, 0, 0, 0),
    ('Lemonade Inc', 1, 0, 0, 0, 3, 0),
    ('Reddit Inc', 1, 0, 1, 0, 0, 0),
    ('Micron Technology Inc', 1, 3, 0, 1, 0, 0),
    ('Taiwan Semiconductor Mfg. Co. Ltd', 1, 3, 0, 1, 0, 0),
    ('Hut 8 Corp', 0, 1, 1, 3, 0, 0),
    ('Robinhood Markets Inc', 0, 0, 1, 1, 3, 0),
    ('Datadog Inc', 1, 0, 3, 0, 0, 0),
    ('Oscar Health Inc', 1, 0, 0, 0, 1, 3),
    ('Amazon.com Inc', 1, 1, 3, 0, 1, 0),
    ('Kaspi.kz JSC', 0, 0, 1, 0, 3, 0),
    ('Rubrik Inc', 1, 0, 3, 0, 0, 0),
    ('NVIDIA Corp', 2, 3, 1, 1, 0, 0),
    ('Meta Platforms Inc', 2, 1, 1, 0, 0, 0),
    ('Coinbase Global Inc', 0, 0, 1, 3, 2, 0),
    ('Bitmine Immersion Technologies Inc', 0, 1, 0, 3, 0, 0)
),
matched AS (
  SELECT
    s.id AS security_id,
    sc.ai_big_tech,
    sc.semis_compute,
    sc.cloud_dev,
    sc.crypto_infra,
    sc.fintech_cfp,
    sc.digital_health
  FROM scores sc
  JOIN bit_security s
    ON s.company_name = sc.company_name
),
expanded AS (
  SELECT security_id, 'AI & Big Tech'::text AS domain_name, ai_big_tech::int AS score FROM matched
  UNION ALL
  SELECT security_id, 'Semis & Compute'::text, semis_compute::int FROM matched
  UNION ALL
  SELECT security_id, 'Cloud / Dev'::text, cloud_dev::int FROM matched
  UNION ALL
  SELECT security_id, 'Crypto Infra'::text, crypto_infra::int FROM matched
  UNION ALL
  SELECT security_id, 'Fintech / CFP'::text, fintech_cfp::int FROM matched
  UNION ALL
  SELECT security_id, 'Digital Health'::text, digital_health::int FROM matched
),
totals AS (
  SELECT security_id, SUM(score)::int AS total_score
  FROM expanded
  GROUP BY security_id
),
weights AS (
  SELECT
    e.security_id,
    d.id AS macro_domain_id,
    (e.score::double precision / t.total_score::double precision) AS weight
  FROM expanded e
  JOIN totals t
    ON t.security_id = e.security_id
  JOIN macro_domain d
    ON d.name = e.domain_name
  WHERE e.score > 0
    AND t.total_score > 0
)
INSERT INTO bit_security_macro_domain_exposure (
  security_id,
  macro_domain_id,
  weight,
  weight_basis,
  source_ref,
  as_of_date,
  created_at,
  updated_at
)
SELECT
  w.security_id,
  w.macro_domain_id,
  w.weight,
  'custom'::text AS weight_basis,
  'security_domain_exposure_scores.md (0-3 scores normalized to weights)'::text AS source_ref,
  '2026-02-25'::date AS as_of_date,
  NOW(),
  NOW()
FROM weights w
ON CONFLICT (security_id, macro_domain_id) DO UPDATE SET
  weight = EXCLUDED.weight,
  weight_basis = EXCLUDED.weight_basis,
  source_ref = EXCLUDED.source_ref,
  as_of_date = EXCLUDED.as_of_date,
  updated_at = NOW();

COMMIT;
