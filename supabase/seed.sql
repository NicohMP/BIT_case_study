-- Seed canonical taxonomy + initial BIT holdings (v1)
--
-- Notes:
-- - This file is intended for local/dev initialization.
-- - For production, replace with proper migrations + a repeatable ingestion pipeline.

-- 1) Allowed values: INDUSTRY_DOMAINS
insert into kb_industry_domains (slug, label, description) values
  ('crypto', 'Crypto', 'Crypto protocols, exchanges, miners, and infra.'),
  ('cybersecurity', 'Cybersecurity', 'Security software and data protection.'),
  ('fintech', 'Fintech', 'Payments, brokerages, and financial platforms.'),
  ('health', 'Health', 'Digital health and health-tech.'),
  ('insurance', 'Insurance', 'Insurance and insurtech.'),
  ('internet', 'Internet', 'Consumer internet platforms and related.'),
  ('semiconductors', 'Semiconductors', 'Chipmakers, foundries, memory, and AI compute.'),
  ('software', 'Software', 'Enterprise software, cloud, and tooling.')
on conflict (slug) do nothing;

-- 2) Allowed values: SUBDOMAINS (and SUBDOMAIN_TO_DOMAIN mapping via FK)
insert into kb_subdomains (slug, label, industry_domain_slug, description) values
  ('crypto_mining_infrastructure', 'Crypto Mining / Infrastructure', 'crypto', null),
  ('cybersecurity_data', 'Cybersecurity / Data', 'cybersecurity', null),
  ('digital_health', 'Digital Health', 'health', null),
  ('fintech_brokerage', 'Fintech / Brokerage', 'fintech', null),
  ('fintech_payments', 'Fintech / Payments', 'fintech', null),
  ('health_insurance_tech', 'Health Insurance / Tech', 'health', null),
  ('insurtech', 'Insurtech', 'insurance', null),
  ('internet_cloud_ecommerce', 'Internet / Cloud / E-commerce', 'internet', null),
  ('internet_platforms', 'Internet Platforms', 'internet', null),
  ('internet_platforms_ads', 'Internet Platforms / Ads', 'internet', null),
  ('semiconductors_ai', 'Semiconductors / AI', 'semiconductors', null),
  ('semiconductors_foundry', 'Semiconductors / Foundry', 'semiconductors', null),
  ('semiconductors_memory', 'Semiconductors / Memory', 'semiconductors', null),
  ('software_cloud', 'Software / Cloud', 'software', null),
  ('software_observability', 'Software / Observability', 'software', null)
on conflict (slug) do nothing;

-- 3) Allowed values: REGIONS
insert into kb_regions (code, label, description) values
  ('US', 'United States', null),
  ('AU', 'Australia', null),
  ('CA', 'Canada', null),
  ('TW', 'Taiwan', null),
  ('KZ', 'Kazakhstan', null)
on conflict (code) do nothing;

-- 4) Allowed values: SENSITIVITY_TAGS
-- Start small; expand as the filtering logic matures.
insert into kb_sensitivity_tags (slug, label, description) values
  ('rates', 'Rates', 'Exposure to interest rate expectations.'),
  ('tariffs', 'Tariffs', 'Exposure to tariffs/trade policy.'),
  ('regulation', 'Regulation', 'Exposure to regulatory outcomes.'),
  ('geopolitics', 'Geopolitics', 'Exposure to geopolitical events.'),
  ('ai', 'AI', 'Exposure to AI adoption/compute cycles.'),
  ('crypto', 'Crypto', 'Exposure to crypto prices/regulation/mining economics.')
on conflict (slug) do nothing;

-- 5) Optional: SYNONYMS (messy labels -> canonical)
-- These start as identity mappings for the current source strings.
insert into kb_subdomain_synonyms (synonym, subdomain_slug) values
  ('Crypto Mining / Infrastructure', 'crypto_mining_infrastructure'),
  ('Cybersecurity / Data', 'cybersecurity_data'),
  ('Digital Health', 'digital_health'),
  ('Fintech / Brokerage', 'fintech_brokerage'),
  ('Fintech / Payments', 'fintech_payments'),
  ('Health Insurance / Tech', 'health_insurance_tech'),
  ('Insurtech', 'insurtech'),
  ('Internet / Cloud / E-commerce', 'internet_cloud_ecommerce'),
  ('Internet Platforms', 'internet_platforms'),
  ('Internet Platforms / Ads', 'internet_platforms_ads'),
  ('Semiconductors / AI', 'semiconductors_ai'),
  ('Semiconductors / Foundry', 'semiconductors_foundry'),
  ('Semiconductors / Memory', 'semiconductors_memory'),
  ('Software / Cloud', 'software_cloud'),
  ('Software / Observability', 'software_observability')
on conflict (synonym_norm) do nothing;

insert into kb_region_synonyms (synonym, region_code) values
  ('US', 'US'),
  ('USA', 'US'),
  ('United States', 'US'),
  ('AU', 'AU'),
  ('Australia', 'AU'),
  ('CA', 'CA'),
  ('Canada', 'CA'),
  ('TW', 'TW'),
  ('Taiwan', 'TW'),
  ('KZ', 'KZ'),
  ('Kazakhstan', 'KZ')
on conflict (synonym_norm) do nothing;

-- 6) Seed holdings by coercing raw labels via synonym tables
with src(ticker, company_name, total_value_usd, shares, subdomain_raw, region_raw, as_of, shares_change) as (
  values
    ('IREN', 'IREN Limited', 262199000, 6941992, 'Crypto Mining / Infrastructure', 'AU', date '2025-12-31', 1147765),
    ('MSFT', 'Microsoft Corp', 43570000, 90092, 'Software / Cloud', 'US', date '2025-12-31', 14845),
    ('HNGE', 'Hinge Health Inc', 154033000, 3316101, 'Digital Health', 'US', date '2025-12-31', 1466577),
    ('GOOGL', 'Alphabet Inc', 143325000, 457908, 'Internet Platforms / Ads', 'US', date '2025-12-31', 196208),
    ('LMND', 'Lemonade Inc', 130017000, 1826593, 'Insurtech', 'US', date '2025-12-31', 572248),
    ('RDDT', 'Reddit Inc', 129514000, 563421, 'Internet Platforms', 'US', date '2025-12-31', -218584),
    ('MU', 'Micron Technology Inc', 117213000, 410683, 'Semiconductors / Memory', 'US', date '2025-12-31', 25724),
    ('TSM', 'Taiwan Semiconductor Mfg Ltd', 116314000, 382751, 'Semiconductors / Foundry', 'TW', date '2025-12-31', 4572),
    ('HUT', 'Hut 8 Corp', 95920000, 2087941, 'Crypto Mining / Infrastructure', 'CA', date '2025-12-31', -89570),
    ('HOOD', 'Robinhood Markets Inc', 94391000, 834578, 'Fintech / Brokerage', 'US', date '2025-12-31', 127087),
    ('DDOG', 'Datadog Inc', 89525000, 658321, 'Software / Observability', 'US', date '2025-12-31', 365684),
    ('OSCR', 'Oscar Health Inc', 88897000, 6186267, 'Health Insurance / Tech', 'US', date '2025-12-31', 5227152),
    ('AMZN', 'Amazon.com Inc', 28619000, 123987, 'Internet / Cloud / E-commerce', 'US', date '2025-12-31', 35514),
    ('KSPI', 'Kaspi KZ JSC', 79232000, 1014104, 'Fintech / Payments', 'KZ', date '2025-12-31', 134068),
    ('RBRK', 'Rubrik Inc', 69626000, 910382, 'Cybersecurity / Data', 'US', date '2025-12-31', 326421),
    ('NVDA', 'NVIDIA Corporation', 71165000, 381582, 'Semiconductors / AI', 'US', date '2025-12-31', -40723),
    ('META', 'Meta Platforms Inc', 62821000, 95171, 'Internet Platforms', 'US', date '2025-12-31', -149214)
),
coerced as (
  select
    s.ticker,
    s.company_name,
    s.total_value_usd::numeric(20, 2) as total_value_usd,
    s.shares::numeric(20, 6) as shares,
    s.shares_change::numeric(20, 6) as shares_change,
    sd.subdomain_slug as subdomain_slug,
    r.region_code as region_code,
    s.as_of,
    'holdingschannel.com (snapshot 2025-12-31)'::text as source
  from src s
  join kb_subdomain_synonyms sd on sd.synonym_norm = lower(trim(s.subdomain_raw))
  join kb_region_synonyms r on r.synonym_norm = lower(trim(s.region_raw))
)
insert into bit_holdings (
  ticker, company_name, total_value_usd, shares, shares_change,
  subdomain_slug, region_code, as_of, source
)
select
  c.ticker, c.company_name, c.total_value_usd, c.shares, c.shares_change,
  c.subdomain_slug, c.region_code, c.as_of, c.source
from coerced c
on conflict (ticker, as_of) do update set
  company_name = excluded.company_name,
  total_value_usd = excluded.total_value_usd,
  shares = excluded.shares,
  shares_change = excluded.shares_change,
  subdomain_slug = excluded.subdomain_slug,
  region_code = excluded.region_code,
  source = excluded.source;

