-- Pipeline run metadata + stable downstream query surfaces.
--
-- Goal: make the ingestion → filtering → matching → relevance → selection pipeline
-- auditable, restartable, and easy for downstream services (WebUI/LLM) to query.

begin;

create table if not exists pm_pipeline_run (
  run_id text primary key,

  status text not null, -- running | success | failed
  started_at timestamptz not null default now(),
  finished_at timestamptz null,

  filter_version text null,
  matcher_version text null,
  scoring_version text null,
  selection_version text null,

  params jsonb not null default '{}'::jsonb,
  ingestion_summary jsonb not null default '{}'::jsonb,
  hard_filters_summary jsonb not null default '{}'::jsonb,
  matching_summary jsonb not null default '{}'::jsonb,
  scoring_summary jsonb not null default '{}'::jsonb,
  selection_summary jsonb not null default '{}'::jsonb,
  audit_summary jsonb not null default '{}'::jsonb,

  error text null,

  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_pm_pipeline_run_status_started on pm_pipeline_run (status, started_at desc);
create index if not exists idx_pm_pipeline_run_finished on pm_pipeline_run (finished_at desc);

-- Latest successful run (single-row view). Downstream should use this to avoid hardcoding versions.
create or replace view v_pm_latest_pipeline_run as
select *
from pm_pipeline_run
where status = 'success'
order by finished_at desc nulls last, started_at desc
limit 1;

-- Latest kept market universe (post Step 2) for downstream systems.
create or replace view v_pm_market_kept_latest as
select
  m.*,
  d.filter_version,
  d.quality_score,
  d.template_score,
  d.equity_relevance_score,
  d.is_rejected,
  d.rejection_reasons
from pm_market m
join v_pm_latest_pipeline_run r
  on true
join pm_market_filter_decision d
  on d.market_id = m.pm_market_id
 and d.filter_version = r.filter_version
where d.is_rejected = false;

-- Latest trusted (strict) market → signal family matches (post Step 3).
create or replace view v_pm_market_signal_family_match_latest_trusted as
select x.*
from pm_market_signal_family_match x
join v_pm_latest_pipeline_run r
  on r.matcher_version = x.matcher_version
where x.method = 'rule_classification'
  and x.match_strength > 0.0;

-- Latest diversified top-K per security (stable product output for WebUI/LLM).
create or replace view v_pm_security_market_relevance_selected_latest as
select sel.*
from pm_market_security_relevance_selection sel
join v_pm_latest_pipeline_run r
  on r.scoring_version = sel.scoring_version
 and r.selection_version = sel.selection_version;

-- Enriched view: join in security + market metadata + scoring breakdown for explanation UIs/LLMs.
create or replace view v_pm_security_market_relevance_selected_latest_enriched as
select
  sel.security_id,
  s.company_name,
  s.ticker,
  s.exchange_mic,
  sel.market_id,
  sel.rank,
  sel.final_score,
  sel.event_id,
  sel.is_rate_like,
  m.question as market_question,
  m.volume_usd as market_volume_usd,
  m.liquidity_usd as market_liquidity_usd,
  e.title as event_title,
  r.base_score,
  r.quality_multiplier,
  r.score_breakdown,
  sel.scoring_version,
  sel.selection_version,
  sel.created_at
from v_pm_security_market_relevance_selected_latest sel
join bit_security s on s.id = sel.security_id
join pm_market m on m.pm_market_id = sel.market_id
left join pm_event e on e.event_id = m.event_id
join pm_market_security_relevance r
  on r.security_id = sel.security_id
 and r.market_id = sel.market_id
 and r.scoring_version = sel.scoring_version;

commit;
