BEGIN;

-- ==========================================
-- Seed BIT taxonomy: Domain → Subdomain
-- ==========================================

-- ---------
-- Domains
-- ---------
INSERT INTO bit_domain (name, description)
VALUES
  ('AI & Data', 'AI platforms, data/observability, cybersecurity & trust'),
  ('Compute & Semiconductors', 'AI compute, semiconductor supply chain, hardware enablement'),
  ('Cloud & Software Infrastructure', 'Hyperscale cloud, enterprise software, developer tools'),
  ('Consumer Internet & Digital Media', 'Social/community platforms, advertising, e-commerce/marketplaces'),
  ('Fintech & Market Infrastructure', 'Brokerage/trading, payments/finops, insurtech/health finance'),
  ('Digital Assets & Blockchain Infrastructure', 'Exchanges/on-ramps, mining/compute operations, protocols/scaling')
ON CONFLICT (name) DO UPDATE
SET description = EXCLUDED.description,
    updated_at = NOW();


-- ------------
-- Subdomains
-- ------------
WITH d AS (
  SELECT id, name FROM bit_domain
)
INSERT INTO bit_subdomain (domain_id, name, description)
SELECT d.id, v.name, v.description
FROM d
JOIN (
  VALUES
    -- AI & Data
    ('AI & Data', 'AI Platforms & Applications', 'GenAI platforms, enterprise AI apps, MLOps/dev tools'),
    ('AI & Data', 'Data & Observability', 'Monitoring/observability and data platforms/analytics'),
    ('AI & Data', 'Cyber & Trust', 'Identity/access, security analytics and trust infrastructure'),

    -- Compute & Semiconductors
    ('Compute & Semiconductors', 'AI Compute', 'GPU/accelerators and AI inference/edge compute'),
    ('Compute & Semiconductors', 'Semiconductor Supply Chain', 'Foundry/manufacturing ecosystem and memory/storage semiconductors'),
    ('Compute & Semiconductors', 'Hardware Enablement', 'Networking/interconnect and edge/specialized hardware'),

    -- Cloud & Software Infrastructure
    ('Cloud & Software Infrastructure', 'Cloud Platforms', 'Hyperscale cloud platforms and cloud developer ecosystems'),
    ('Cloud & Software Infrastructure', 'Enterprise Software', 'Productivity platforms and enterprise SaaS'),
    ('Cloud & Software Infrastructure', 'Developer Tools', 'Developer platforms, CI/CD and integration tooling'),

    -- Consumer Internet & Digital Media
    ('Consumer Internet & Digital Media', 'Social & Communities', 'Social networks and community/forum platforms'),
    ('Consumer Internet & Digital Media', 'Digital Advertising', 'Advertising platforms and monetization engines'),
    ('Consumer Internet & Digital Media', 'Commerce & Marketplaces', 'E-commerce platforms and consumer marketplaces'),

    -- Fintech & Market Infrastructure
    ('Fintech & Market Infrastructure', 'Brokerage & Trading', 'Retail brokerage and trading/market data analytics'),
    ('Fintech & Market Infrastructure', 'Payments & FinOps', 'Payments rails/processors and treasury/spend management'),
    ('Fintech & Market Infrastructure', 'Insurtech & Health Finance', 'Digital insurance and healthcare finance/benefits platforms'),

    -- Digital Assets & Blockchain Infrastructure
    ('Digital Assets & Blockchain Infrastructure', 'Exchanges & On-ramps', 'Crypto exchanges/brokers and custody/prime services'),
    ('Digital Assets & Blockchain Infrastructure', 'Mining & Compute Operations', 'Bitcoin mining operators and mining infrastructure/hosting'),
    ('Digital Assets & Blockchain Infrastructure', 'Protocol & Scaling', 'Layer-1 networks and Layer-2/scaling tech (optional future holdings)')
) AS v(domain_name, name, description)
  ON d.name = v.domain_name
ON CONFLICT (domain_id, name) DO UPDATE
SET description = EXCLUDED.description,
    updated_at = NOW();

COMMIT;