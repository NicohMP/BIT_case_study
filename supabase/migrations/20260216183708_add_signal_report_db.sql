BEGIN;

-- ==========================================
-- Signal reports (LLM output stored for UI)
-- ==========================================
CREATE TABLE IF NOT EXISTS signal_report (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- optional metadata
    title TEXT NULL,

    -- main report body
    report_md TEXT NOT NULL,

    -- list of polymarket market ids (and/or other inputs) used to generate the report
    inputs_json JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE INDEX IF NOT EXISTS ix_signal_report_created_at
    ON signal_report(created_at DESC);

COMMIT;