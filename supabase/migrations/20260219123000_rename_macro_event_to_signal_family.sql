BEGIN;

-- ==========================================
-- Rename macro-event tables to "signal families"
-- ==========================================
-- Motivation:
-- - Avoid confusion with Polymarket "events"
-- - Keep semantics: curated macro signal families -> domain influence matrix

DO $$
BEGIN
  IF to_regclass('public.macro_event_domain_influence') IS NOT NULL THEN
    -- Rename FK column first so the final table name reads cleanly.
    IF EXISTS (
      SELECT 1
      FROM information_schema.columns
      WHERE table_schema = 'public'
        AND table_name = 'macro_event_domain_influence'
        AND column_name = 'macro_event_id'
    ) THEN
      ALTER TABLE macro_event_domain_influence
        RENAME COLUMN macro_event_id TO signal_family_id;
    END IF;

    -- Rename constraint if present (Postgres auto-names can vary).
    IF EXISTS (
      SELECT 1 FROM pg_constraint
      WHERE conname = 'chk_macro_event_domain_score_0_5'
    ) THEN
      ALTER TABLE macro_event_domain_influence
        RENAME CONSTRAINT chk_macro_event_domain_score_0_5 TO chk_signal_family_domain_score_0_5;
    END IF;

    ALTER TABLE macro_event_domain_influence
      RENAME TO signal_family_domain_influence;
  END IF;

  IF to_regclass('public.macro_event') IS NOT NULL THEN
    ALTER TABLE macro_event
      RENAME TO signal_family;
  END IF;
END $$;

COMMIT;

