begin;

-- Step 5 (report time): LLM-generated signal report per security.
--
-- The LLM is only used after Steps 1–4b have already produced a deterministic,
-- structured context pack and a diversified set of candidate markets.

create table if not exists pm_security_signal_report (
  report_id text primary key,

  -- Optional pointer to the pipeline run that produced the underlying candidates.
  run_id text null
    references pm_pipeline_run(run_id)
    on delete set null,

  security_id bigint not null
    references bit_security(id)
    on delete cascade,

  filter_version text null,
  matcher_version text null,
  scoring_version text not null,
  selection_version text not null,

  prompt_version text not null,
  model text not null,

  context_pack_hash text not null,

  report_json jsonb not null,
  report_md text null,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists uq_pm_security_signal_report_dedupe
  on pm_security_signal_report (security_id, context_pack_hash, prompt_version, model);

create index if not exists ix_pm_security_signal_report_security_created
  on pm_security_signal_report (security_id, created_at desc);

create index if not exists ix_pm_security_signal_report_run
  on pm_security_signal_report (run_id);

create or replace view v_pm_latest_security_signal_report as
select distinct on (security_id)
  *
from pm_security_signal_report
order by security_id, created_at desc;

commit;

