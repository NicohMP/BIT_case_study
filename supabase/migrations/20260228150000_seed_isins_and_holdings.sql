-- Seed ISINs + BIT holdings market values (USD) for the demo universe.
--
-- Notes:
-- - Some source lines used exchange code "XNGS" for NASDAQ; the canonical MIC we use in
--   this project is "XNAS", so this migration normalizes those rows to XNAS.
-- - HNGE exists twice (XNYS + XNAS) in some local DB states; we keep the row that has
--   domain exposures (XNYS) and delete the exposure-less duplicate if present.
-- - Alphabet exists as GOOG/GOOGL; for the demo we keep GOOGL only to avoid confusion.
-- - NVDA exposure in this snapshot is via an inverse NVDA ETF (NVDD). For the demo UI we
--   attribute that holding value to NVDA (economic exposure proxy) instead of adding NVDD.
--
-- This migration is data-only; it should be safe to re-run (idempotent).

begin;

-- 0) Bugfix: the exposure-weights constraint trigger must allow deleting a security.
-- The trigger is deferrable and runs at COMMIT; during a CASCADE delete of a security,
-- exposure rows are deleted, leaving a temporary 0 sum for that security_id. If the
-- security itself is also deleted in the same transaction, we should not enforce the
-- weights-sum constraint.
create or replace function public.fn_check_security_exposure_weights_sum()
 returns trigger
 language plpgsql
as $function$
declare
  sid bigint;
  total double precision;
begin
  sid := coalesce(new.security_id, old.security_id);

  -- If the security row no longer exists (e.g. deleted in the same transaction),
  -- do not enforce the exposure weight constraint.
  if not exists (select 1 from bit_security where id = sid) then
    return null;
  end if;

  select coalesce(sum(weight), 0.0)
    into total
  from bit_security_macro_domain_exposure
  where security_id = sid;

  -- Allow a small tolerance for floating point weights.
  if total < 0.999 or total > 1.001 then
    raise exception 'Exposure weights for security_id=% must sum to 1.0 (got %)', sid, total;
  end if;

  return null;
end;
$function$;

-- 1) Clean up: drop the HNGE duplicate that has no exposures (keep XNYS which is used by exposures).
delete from bit_security s
where s.ticker = 'HNGE'
  and s.exchange_mic = 'XNAS'
  and not exists (select 1 from bit_security_macro_domain_exposure e where e.security_id = s.id)
  and not exists (select 1 from bit_holding h where h.security_id = s.id);

-- 2) Clean up: keep GOOGL only (GOOG is redundant for this demo; cascades remove derived rows).
delete from bit_security
where ticker = 'GOOG'
  and exchange_mic = 'XNAS';

-- 3) Normalize: BMNR is treated as an NYSE name in the provided snapshot.
update bit_security
set exchange_mic = 'XNYS'
where ticker = 'BMNR'
  and exchange_mic = 'XNAS';

-- 4) Seed ISINs for the demo universe (normalized exchange_mic; XNGS → XNAS).
with data(ticker, exchange_mic, isin) as (
  values
    ('IREN',  'XNAS', 'AU0000185993'),
    ('MSFT',  'XNAS', 'US5949181045'),
    ('HNGE',  'XNYS', 'US4333131039'),
    ('GOOGL', 'XNAS', 'US02079K3059'),
    ('LMND',  'XNYS', 'US52567D1072'),
    ('RDDT',  'XNYS', 'US75734B1008'),
    ('MU',    'XNAS', 'US5951121038'),
    ('TSM',   'XNYS', 'US8740391003'),
    ('HUT',   'XNAS', 'CA44812T1021'),
    ('HOOD',  'XNAS', 'US7707001027'),
    ('DDOG',  'XNAS', 'US23804L1035'),
    ('OSCR',  'XNYS', 'US6877931096'),
    ('AMZN',  'XNAS', 'US0231351067'),
    ('KSPI',  'XNAS', 'US48581R2058'),
    ('RBRK',  'XNYS', 'US78112Q1058'),
    ('META',  'XNAS', 'US30303M1027'),
    ('COIN',  'XNAS', 'US19260Q1076'),
    ('BMNR',  'XNYS', 'US09175A2069')
)
update bit_security s
set isin = d.isin
from data d
where s.ticker = d.ticker
  and s.exchange_mic = d.exchange_mic;

-- 5) Seed holdings market values (USD) so the Web UI isn't all zeros.
-- Values provided as USD millions; we store total_value in USD.
with holdings(ticker, exchange_mic, total_value_usd) as (
  values
    ('IREN',  'XNAS', 262.20::numeric * 1000000),
    ('MSFT',  'XNAS', 236.92::numeric * 1000000),
    ('HNGE',  'XNYS', 154.03::numeric * 1000000),
    ('GOOGL', 'XNAS', 178.16::numeric * 1000000),
    ('LMND',  'XNYS', 132.16::numeric * 1000000),
    ('RDDT',  'XNYS', 129.51::numeric * 1000000),
    ('MU',    'XNAS', 117.27::numeric * 1000000),
    ('TSM',   'XNYS', 116.31::numeric * 1000000),
    ('HUT',   'XNAS',  98.45::numeric * 1000000),
    ('HOOD',  'XNAS',  94.39::numeric * 1000000),
    ('DDOG',  'XNAS',  89.53::numeric * 1000000),
    ('OSCR',  'XNYS',  88.90::numeric * 1000000),
    ('AMZN',  'XNAS',  88.43::numeric * 1000000),
    ('KSPI',  'XNAS',  79.23::numeric * 1000000),
    ('RBRK',  'XNYS',  75.75::numeric * 1000000),
    ('NVDA',  'XNAS',  71.17::numeric * 1000000),
    ('META',  'XNAS',  62.82::numeric * 1000000),
    ('COIN',  'XNAS',  60.05::numeric * 1000000),
    ('BMNR',  'XNYS',  42.15::numeric * 1000000)
)
insert into bit_holding (security_id, as_of, shares, total_value, value_currency, source_note)
select
  s.id as security_id,
  '2025-12-31T00:00:00Z'::timestamptz as as_of,
  0::numeric as shares,
  h.total_value_usd as total_value,
  'USD'::char(3) as value_currency,
  case
    when h.ticker = 'NVDA' then '13F snapshot (provided; NVDA economic exposure via NVDD; common + calls aggregated by ticker)'
    else '13F snapshot (provided; common + calls aggregated by ticker)'
  end as source_note
from holdings h
join bit_security s
  on s.ticker = h.ticker
 and s.exchange_mic = h.exchange_mic
on conflict (security_id) do update
set
  as_of = excluded.as_of,
  shares = excluded.shares,
  total_value = excluded.total_value,
  value_currency = excluded.value_currency,
  source_note = excluded.source_note,
  updated_at = now();

commit;
