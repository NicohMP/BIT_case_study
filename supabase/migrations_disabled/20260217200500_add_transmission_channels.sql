BEGIN;

-- ==========================================
-- Transmission channels + domain exposures
-- ==========================================
-- Purpose:
-- - Provide a stable macro "mechanism" layer to explain how events affect domains.
-- - Enable a simple relevance score: domain_rel * dot(channel_rel, exposure[domain]).

CREATE TABLE IF NOT EXISTS transmission_channel (
    slug TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bit_domain_channel_exposure (
    domain_id BIGINT NOT NULL
        REFERENCES bit_domain(id)
        ON DELETE CASCADE,
    channel_slug TEXT NOT NULL
        REFERENCES transmission_channel(slug)
        ON DELETE RESTRICT,

    exposure DOUBLE PRECISION NOT NULL,
    CONSTRAINT chk_exposure_0_1 CHECK (exposure >= 0.0 AND exposure <= 1.0),

    rationale TEXT NOT NULL DEFAULT '',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (domain_id, channel_slug)
);

CREATE INDEX IF NOT EXISTS ix_bit_domain_channel_exposure_channel
    ON bit_domain_channel_exposure(channel_slug);

-- Seed channels (static)
INSERT INTO transmission_channel (slug, label, description) VALUES
  ('discount_rate', 'Discount Rate', 'Rates/discount factor changes affecting valuation and risk appetite.'),
  ('demand',        'Demand',        'End-demand changes (growth/recession, consumer/enterprise spend, adoption).'),
  ('supply',        'Supply',        'Supply constraints/shocks (export controls, capacity, supply chain).'),
  ('regulation',    'Regulation',    'Policy/regulatory actions affecting economics, permissions, and competition.')
ON CONFLICT (slug) DO NOTHING;

-- Seed exposures (static initial judgment; editable later)
-- Helper: lookup domain_id by name
WITH d AS (
  SELECT id, name FROM bit_domain
)
INSERT INTO bit_domain_channel_exposure (domain_id, channel_slug, exposure, rationale)
SELECT d.id, x.channel_slug, x.exposure, x.rationale
FROM d
JOIN (
  VALUES
    -- AI & Data
    ('AI & Data', 'discount_rate', 0.35, 'High-duration growth narratives; valuation sensitive to rates and risk appetite.'),
    ('AI & Data', 'demand',        0.55, 'Adoption and enterprise/consumer spend on AI products drives revenue expectations.'),
    ('AI & Data', 'supply',        0.35, 'Compute availability (GPUs, datacenter capacity) can bottleneck delivery and margins.'),
    ('AI & Data', 'regulation',    0.45, 'AI safety/regulatory regimes can constrain deployment and raise compliance costs.'),

    -- Compute & Semiconductors
    ('Compute & Semiconductors', 'discount_rate', 0.25, 'Cyclicals are less duration-like than pure software but still impacted by risk-off regimes.'),
    ('Compute & Semiconductors', 'demand',        0.55, 'End-demand (datacenter/PC/AI capex) drives volumes and pricing.'),
    ('Compute & Semiconductors', 'supply',        0.75, 'Capacity constraints and export controls materially affect supply, mix, and margins.'),
    ('Compute & Semiconductors', 'regulation',    0.45, 'Export controls, subsidies, and antitrust actions can shift competitive dynamics.'),

    -- Cloud & Software Infrastructure
    ('Cloud & Software Infrastructure', 'discount_rate', 0.45, 'Software multiples are duration-sensitive and move with rates and liquidity.'),
    ('Cloud & Software Infrastructure', 'demand',        0.65, 'Enterprise IT budgets and cloud spend cycles drive growth.'),
    ('Cloud & Software Infrastructure', 'supply',        0.20, 'Supply issues matter mostly via datacenter capacity and energy constraints.'),
    ('Cloud & Software Infrastructure', 'regulation',    0.30, 'Privacy/security regulation can raise costs; antitrust can affect platform power.'),

    -- Consumer Internet & Digital Media
    ('Consumer Internet & Digital Media', 'discount_rate', 0.35, 'Ad-driven platforms are growth-duration assets; valuation moves with rates.'),
    ('Consumer Internet & Digital Media', 'demand',        0.70, 'User engagement and ad budgets are strongly tied to macro demand conditions.'),
    ('Consumer Internet & Digital Media', 'supply',        0.10, 'Supply constraints are typically not the primary driver (exceptions: devices/app stores).'),
    ('Consumer Internet & Digital Media', 'regulation',    0.50, 'Content, privacy, and platform regulation can directly impact monetization and access.'),

    -- Fintech & Market Infrastructure
    ('Fintech & Market Infrastructure', 'discount_rate', 0.40, 'Rates influence credit conditions, volumes, and equity/crypto risk appetite.'),
    ('Fintech & Market Infrastructure', 'demand',        0.60, 'Transaction volumes, trading activity, and consumer/SMB activity drive revenues.'),
    ('Fintech & Market Infrastructure', 'supply',        0.15, 'Supply constraints are secondary; outages/infra constraints can matter at extremes.'),
    ('Fintech & Market Infrastructure', 'regulation',    0.55, 'Licensing, market-structure rules, and enforcement actions can reshape economics.'),

    -- Digital Assets & Blockchain Infrastructure
    ('Digital Assets & Blockchain Infrastructure', 'discount_rate', 0.55, 'Crypto prices and risk appetite are highly sensitive to liquidity and rates.'),
    ('Digital Assets & Blockchain Infrastructure', 'demand',        0.60, 'Adoption and inflows (spot ETFs, institutional demand) drive usage and price.'),
    ('Digital Assets & Blockchain Infrastructure', 'supply',        0.30, 'Protocol issuance/mining dynamics and infrastructure constraints can matter.'),
    ('Digital Assets & Blockchain Infrastructure', 'regulation',    0.70, 'Approvals/enforcement (ETFs, stablecoins, exchanges) strongly affect participation.')
) AS x(domain_name, channel_slug, exposure, rationale)
  ON x.domain_name = d.name
ON CONFLICT (domain_id, channel_slug) DO UPDATE SET
  exposure = EXCLUDED.exposure,
  rationale = EXCLUDED.rationale,
  updated_at = NOW();

COMMIT;

