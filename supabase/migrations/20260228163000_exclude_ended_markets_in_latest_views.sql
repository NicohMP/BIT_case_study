-- Exclude ended markets from "latest" downstream views.
--
-- Motivation:
-- - The pipeline refresh runs on a schedule (e.g. every 2h), but markets can end in-between runs.
-- - Downstream consumers (Web UI, report-time context packs) should focus on "what matters now".
-- - Keeping ended markets out of these views avoids confusing demos and stale reports.

begin;

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
where d.is_rejected = false
  and (m.end_date is null or m.end_date >= now());

create or replace view v_pm_security_market_relevance_selected_latest as
select sel.*
from pm_market_security_relevance_selection sel
join v_pm_latest_pipeline_run r
  on r.scoring_version = sel.scoring_version
 and r.selection_version = sel.selection_version
join pm_market m
  on m.pm_market_id = sel.market_id
where (m.end_date is null or m.end_date >= now());

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

