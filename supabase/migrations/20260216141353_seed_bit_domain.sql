BEGIN;

-- ==========================================
-- Seed BIT taxonomy: Domains (Level 1 only)
-- ==========================================

INSERT INTO bit_domain (name)
VALUES
  ('AI & Data'),
  ('Compute & Semiconductors'),
  ('Cloud & Software Infrastructure'),
  ('Consumer Internet & Digital Media'),
  ('Fintech & Market Infrastructure'),
  ('Digital Assets & Blockchain Infrastructure')
ON CONFLICT (name) DO NOTHING;

COMMIT;