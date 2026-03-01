BEGIN;

-- ==========================================
-- Enrich BIT domains with definition fields
-- ==========================================
-- Purpose:
-- - Make domain "themes" explicit and non-overlapping
-- - Provide stable text to embed against (instead of hardcoded notebook strings)

ALTER TABLE bit_domain
    ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '',
    ADD COLUMN IF NOT EXISTS keywords TEXT[] NOT NULL DEFAULT '{}'::text[],
    ADD COLUMN IF NOT EXISTS exclusions TEXT[] NOT NULL DEFAULT '{}'::text[];

-- Seed domain definitions (keep crisp; include exclusions to reduce overlap).
UPDATE bit_domain
SET
    description = 'AI model labs, foundation models, data/ML platforms, and AI regulation that directly impacts AI builders or major AI adopters. Includes AI hardware demand as it relates to model training/inference.',
    keywords = ARRAY['AI','LLM','foundation model','model training','inference','data platform','ML tooling','OpenAI','Anthropic'],
    exclusions = ARRAY['pure cloud price wars without AI linkage','generic consumer internet trends','sports/politics-only markets']
WHERE name = 'AI & Data';

UPDATE bit_domain
SET
    description = 'Semiconductors and compute supply chain: GPUs/CPUs, foundries, semiconductor equipment, memory, and export controls impacting chip supply/demand. Includes datacenter compute capacity constraints.',
    keywords = ARRAY['GPU','CPU','semiconductor','foundry','TSMC','ASML','NVIDIA','AMD','export controls','chips'],
    exclusions = ARRAY['AI model releases without compute supply implication','consumer app/product launches','pure payments/fintech']
WHERE name = 'Compute & Semiconductors';

UPDATE bit_domain
SET
    description = 'Cloud and enterprise infrastructure software: hyperscalers, datacenters, core infra (databases, networking), security and observability, and enterprise SaaS spend cycles. Focus on infra vendors and spending, not consumer apps.',
    keywords = ARRAY['cloud','AWS','Azure','GCP','datacenter','SaaS','enterprise software','security','observability','database'],
    exclusions = ARRAY['consumer social/media','sports/celebrity','AI model labs unless about infra spend']
WHERE name = 'Cloud & Software Infrastructure';

UPDATE bit_domain
SET
    description = 'Consumer internet platforms and digital media: social networks, creators, ad platforms, marketplaces, and distribution channels that drive consumer engagement and digital ad budgets.',
    keywords = ARRAY['social','ads','advertising','e-commerce','marketplace','platform','creator','app store','TikTok'],
    exclusions = ARRAY['enterprise cloud infra','semiconductor supply chain','crypto protocol/asset price markets']
WHERE name = 'Consumer Internet & Digital Media';

UPDATE bit_domain
SET
    description = 'Fintech and market infrastructure: payments rails, card networks, exchanges/brokerages, trading infrastructure, and financial regulation that affects transaction economics and market structure.',
    keywords = ARRAY['payments','fintech','exchange','brokerage','trading','market structure','Visa','Mastercard','Robinhood'],
    exclusions = ARRAY['consumer social/media','AI model releases','chip supply chain']
WHERE name = 'Fintech & Market Infrastructure';

UPDATE bit_domain
SET
    description = 'Digital assets and blockchain infrastructure: major crypto assets, stablecoins, L1/L2 infrastructure, custody/exchanges, and regulation/ETF approval affecting adoption and liquidity.',
    keywords = ARRAY['bitcoin','ethereum','stablecoin','crypto ETF','exchange','custody','blockchain','DeFi'],
    exclusions = ARRAY['sports/celebrity','generic macro politics without crypto linkage','enterprise SaaS spend']
WHERE name = 'Digital Assets & Blockchain Infrastructure';

COMMIT;

