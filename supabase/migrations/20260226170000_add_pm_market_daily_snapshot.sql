begin;

-- Daily snapshots of market state for Δp / sentiment-intensity features (Step 6+).
-- MVP intent: record one row per market per UTC day (idempotent), using the latest
-- normalized fields from pm_market. Downstream can compute Δp from snapshots later.

create table if not exists pm_market_daily_snapshot (
  snapshot_date date not null,
  market_id bigint not null,

  -- Latest observed market state (copied from pm_market at snapshot time)
  probability double precision null,
  probabilities jsonb null,
  outcomes jsonb null,
  volume_usd double precision null,
  liquidity_usd double precision null,
  end_date timestamptz null,
  active boolean null,
  closed boolean null,

  -- Optional metadata (helps debugging / reproducibility)
  filter_version text null,
  is_kept boolean null,
  run_id text null,
  source text not null default 'pm_market',

  created_at timestamptz not null default now(),

  primary key (snapshot_date, market_id)
);

-- Optional FK: allow NULL if rows predate pm_market ids (defensive)
do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'fk_pm_market_daily_snapshot_market'
  ) then
    alter table pm_market_daily_snapshot
      add constraint fk_pm_market_daily_snapshot_market
      foreign key (market_id)
      references pm_market(pm_market_id)
      on delete cascade;
  end if;
end $$;

create index if not exists idx_pm_market_daily_snapshot_market_date
  on pm_market_daily_snapshot (market_id, snapshot_date desc);

create index if not exists idx_pm_market_daily_snapshot_date
  on pm_market_daily_snapshot (snapshot_date desc);

commit;

