# False Positive Audit Snapshot (Step 3)

- as_of_utc: `2026-02-27T17:19:40.964914+00:00`
- filter_version: `hard_filters_v8`
- matcher_version: `matcher_v10`

## Monetary policy surprises (FOMC)
- slug: `fomc_surprises`
- strict_matches: 97

### Top strict matches
- (1.000) `572473` — Will Trump nominate Judy Shelton as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `654412` — Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["anchor:fed", "fed", "interest rate", "bps", "meeting"]`
- (1.000) `654415` — Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["anchor:fed", "fed", "interest rate", "bps", "meeting"]`
- (1.000) `572469` — Will Trump nominate Kevin Warsh as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `572481` — Will Trump nominate Scott Bessent as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `572470` — Will Trump nominate Kevin Hassett as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `572485` — Will Trump nominate Rick Rieder as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `572478` — Will Trump nominate Jerome Powell as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "anchor:powell", "override:fed chair", "fed", "powell", "fed chair", "chair"]`
- (1.000) `572471` — Will Trump nominate Christopher Waller as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`
- (1.000) `572472` — Will Trump nominate Bill Pulte as the next Fed chair?
  - event: Who will Trump nominate as Fed Chair?
  - matched_terms: `["anchor:fed", "override:fed chair", "fed", "fed chair", "chair"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.484, rule=0.000) `1236532` — March Fed Derivative: "25bps cut" flips "Pause" by Feb 28?
  - event: March Fed Derivative: "25bps cut" flips "Pause" by Feb 28?
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.466, rule=0.000) `950064` — Will the Fed Cut–Cut–Cut in the next three decisions (Jan–Mar–Apr)?
  - event: Fed decisions (Jan-Apr)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.465, rule=0.000) `1293515` — Will Stephen Miran dissent the next Fed decision?
  - event: Will Stephen Miran dissent the next Fed decision?
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.464, rule=0.000) `950062` — Will the Fed Cut–Pause–Cut in the next three decisions (Jan–Mar–Apr)?
  - event: Fed decisions (Jan-Apr)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.462, rule=0.000) `950069` — Will the Fed decide differently in the next three decisions (Jan–Mar–Apr)?
  - event: Fed decisions (Jan-Apr)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.460, rule=0.000) `950063` — Will the Fed Cut–Cut–Pause in the next three decisions (Jan–Mar–Apr)?
  - event: Fed decisions (Jan-Apr)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.456, rule=0.000) `677147` — Fed emergency rate cut before 2027?
  - event: Fed emergency rate cut before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["fed", "rate cut"]`
  - exclusions_hit: `[]`
- (sim=0.455, rule=0.000) `1288246` — Will the Fed Cut–Cut–Cut in the next three decisions (Mar–Apr–Jun)?
  - event: Fed decisions (Mar-Jun)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.454, rule=0.000) `1288244` — Will the Fed Cut–Pause–Cut in the next three decisions (Mar–Apr–Jun)?
  - event: Fed decisions (Mar-Jun)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`
- (sim=0.452, rule=0.000) `950068` — Will the Fed Pause–Cut–Cut in the next three decisions (Jan–Mar–Apr)?
  - event: Fed decisions (Jan-Apr)
  - anchors_hit: `[]`
  - keyword_hits: `["fed"]`
  - exclusions_hit: `[]`

## Real yields / long rates
- slug: `real_yields_long_rates`
- strict_matches: 25

### Top strict matches
- (0.700) `677023` — Will the 10-year Treasury yield hit 4.8% before 2027?
  - event: How high will 10-year Treasury yield go before 2027?
  - matched_terms: `["treasury yield"]`
- (0.700) `677142` — Will the 10-year Treasury yield dip below 1.0% before 2027?
  - event: How low will 10-year Treasury yield get before 2027?
  - matched_terms: `["treasury yield"]`
- (0.700) `902258` — Will the 10-year treasury yield hit 4.5% by March 31?
  - event: How high will 10-year Treasury yield go by March 31?
  - matched_terms: `["treasury yield"]`
- (0.700) `902255` — Will the 10-year treasury yield hit 4.4% by March 31?
  - event: How high will 10-year Treasury yield go by March 31?
  - matched_terms: `["treasury yield"]`
- (0.700) `677144` — Will the 10-year Treasury yield dip below 3.7% before 2027?
  - event: How low will 10-year Treasury yield get before 2027?
  - matched_terms: `["treasury yield"]`
- (0.700) `902253` — Will the 10-year treasury yield hit 4.3% by March 31?
  - event: How high will 10-year Treasury yield go by March 31?
  - matched_terms: `["treasury yield"]`
- (0.700) `677024` — Will the 10-year Treasury yield hit 5.0% before 2027?
  - event: How high will 10-year Treasury yield go before 2027?
  - matched_terms: `["treasury yield"]`
- (0.700) `902265` — Will the 10-year treasury yield hit 5.0% by March 31?
  - event: How high will 10-year Treasury yield go by March 31?
  - matched_terms: `["treasury yield"]`
- (0.700) `902263` — Will the 10-year treasury yield hit 4.8% by March 31?
  - event: How high will 10-year Treasury yield go by March 31?
  - matched_terms: `["treasury yield"]`
- (0.700) `677022` — Will the 10-year Treasury yield hit 4.6% before 2027?
  - event: How high will 10-year Treasury yield go before 2027?
  - matched_terms: `["treasury yield"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.413, rule=0.000) `616912` — Will 10 Fed rate cuts happen in 2026?
  - event: How many Fed rate cuts in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.412, rule=0.000) `908713` — Fed rate hike in 2026?
  - event: Fed rate hike in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.409, rule=0.000) `1227992` — Nothing Ever Happens: Interest Rates
  - event: Nothing Ever Happens: Interest Rates
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.403, rule=0.000) `680954` — Will inflation reach more than 10% in 2026?
  - event: How high will inflation get in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## US–China semiconductor export controls
- slug: `us_china_semis_export_controls`
- strict_matches: 1

### Top strict matches
- (0.700) `1426260` — Will AI-chip export licensing become law this year?
  - event: Which bills will become law in 2026?
  - matched_terms: `["anchor:export licensing", "export licensing"]`

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## Taiwan geopolitical risk
- slug: `taiwan_geopolitical_risk`
- strict_matches: 6

### Top strict matches
- (1.000) `604470` — Will China blockade Taiwan by June 30?
  - event: Will China blockade Taiwan by June 30?
  - matched_terms: `["taiwan", "china", "blockade"]`
- (0.850) `567621` — Will China invade Taiwan by end of 2026?
  - event: Will China invade Taiwan by end of 2026?
  - matched_terms: `["taiwan", "china"]`
- (0.850) `701290` — Will China invade Taiwan by March 31, 2026?
  - event: Will China invade Taiwan by March 31, 2026?
  - matched_terms: `["taiwan", "china"]`
- (0.850) `540843` — Will China invades Taiwan before GTA VI?
  - event: What will happen before GTA VI?
  - matched_terms: `["taiwan", "china"]`
- (0.850) `677407` — China x Taiwan military clash before 2027?
  - event: China x Taiwan military clash before 2027?
  - matched_terms: `["taiwan", "china"]`
- (0.850) `956590` — Will China invade Taiwan by June 30, 2026?
  - event: Will China invade Taiwan by June 30, 2026?
  - matched_terms: `["taiwan", "china"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.508, rule=0.000) `1176221` — U.S. agrees to a new trade deal with "Taiwan" before 2027?
  - event: Which countries will Trump make new trade deals with before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["taiwan"]`
  - exclusions_hit: `[]`
- (sim=0.488, rule=0.000) `665270` — Will Donald Trump visit Taiwan in 2026?
  - event: Which countries will Donald Trump visit in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `["taiwan"]`
  - exclusions_hit: `[]`
- (sim=0.473, rule=0.000) `1131161` — Lai Ching-te out as President of Taiwan in 2026?
  - event: Lai Ching-te out as President of Taiwan in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `["taiwan"]`
  - exclusions_hit: `[]`
- (sim=0.454, rule=0.000) `677408` — China x Philippines military clash before 2027?
  - event: China x Philippines military clash before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["china"]`
  - exclusions_hit: `[]`
- (sim=0.449, rule=0.000) `1171824` — Taiwanese Premier Cho Jung-tai out by June 30, 2026?
  - event: Taiwanese Premier Cho Jung-tai out by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.448, rule=0.000) `1171825` — Taiwanese Premier Cho Jung-tai out by December 31, 2026?
  - event: Taiwanese Premier Cho Jung-tai out by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.440, rule=0.000) `687642` — China x Japan military clash before 2027?
  - event: China x Japan military clash before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["china"]`
  - exclusions_hit: `[]`
- (sim=0.432, rule=0.000) `1066556` — Lai Ching-te impeached by June 30?
  - event: Lai Ching-te impeached by June 30?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.423, rule=0.000) `1323317` — Will the US federal government take a stake in Taiwan Semiconductor Manufacturing Company Limited?
  - event: Which companies will the US take a stake in?
  - anchors_hit: `[]`
  - keyword_hits: `["taiwan"]`
  - exclusions_hit: `[]`
- (sim=0.410, rule=0.000) `665243` — NATO article 5 before 2027?
  - event: NATO article 5 before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Crypto regulation regime changes
- slug: `crypto_regime_changes`
- strict_matches: 25

### Top strict matches
- (0.700) `1426021` — Ethereum ETF Flows on February 26?
  - event: Ethereum ETF Flows on February 26?
  - matched_terms: `["anchor:ethereum etf", "ethereum etf"]`
- (0.700) `1068733` — Will stablecoins hit $500B before 2027?
  - event: Will stablecoins hit $500B before 2027?
  - matched_terms: `["anchor:stablecoins", "stablecoins"]`
- (0.700) `1108760` — Will USD-denominated stablecoin market share fall below 99% in 2026?
  - event: Will USD-denominated stablecoin market share fall below 99% in 2026?
  - matched_terms: `["anchor:stablecoin", "stablecoin"]`
- (0.700) `1058192` — USDC depeg by December 31?
  - event: Stablecoins depeg before 2027?
  - matched_terms: `["anchor:stablecoins", "stablecoins"]`
- (0.700) `1425994` — Bitcoin ETF Flows on February 26?
  - event: Bitcoin ETF Flows on February 26?
  - matched_terms: `["anchor:bitcoin etf", "bitcoin etf"]`
- (0.700) `1058196` — USD1 depeg by December 31?
  - event: Stablecoins depeg before 2027?
  - matched_terms: `["anchor:stablecoins", "stablecoins"]`
- (0.700) `1162155` — Will X launch a USD stablecoin in 2026?
  - event: Will X launch a USD stablecoin in 2026?
  - matched_terms: `["anchor:stablecoin", "stablecoin"]`
- (0.700) `1058193` — USDE depeg by December 31?
  - event: Stablecoins depeg before 2027?
  - matched_terms: `["anchor:stablecoins", "stablecoins"]`
- (0.700) `1162208` — Will Revolut launch a USD stablecoin in 2026?
  - event: Will Revolut launch a USD stablecoin in 2026?
  - matched_terms: `["anchor:stablecoin", "stablecoin"]`
- (0.700) `1058199` — USD0 depeg by December 31?
  - event: Stablecoins depeg before 2027?
  - matched_terms: `["anchor:stablecoins", "stablecoins"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.586, rule=0.000) `665205` — US national Bitcoin reserve before 2027?
  - event: US national Bitcoin reserve before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.518, rule=0.000) `665375` — US national Ethereum reserve before 2027?
  - event: US national Ethereum reserve before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.487, rule=0.000) `1163699` — Clarity Act signed into law in 2026?
  - event: Clarity Act signed into law in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.485, rule=0.000) `1346362` — Did a crypto hedge fund blow up?
  - event: Did a crypto hedge fund blow up?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.482, rule=0.000) `1090479` — Record crypto liquidation in 2026?
  - event: Record crypto liquidation in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.467, rule=0.000) `516926` — MicroStrategy sells any Bitcoin in 2025?
  - event: MicroStrategy sells any Bitcoin by ___ ?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.466, rule=0.000) `1122084` — OKX IPO in 2026?
  - event: OKX IPO in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.465, rule=0.000) `1121549` — Nothing Ever Happens: MicroStrategy
  - event: Nothing Ever Happens: MicroStrategy
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.457, rule=0.000) `678876` — Kraken IPO by March 31, 2026?
  - event: Kraken IPO by ___ ?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.451, rule=0.000) `692258` — MicroStrategy sells any Bitcoin by June 30, 2026?
  - event: MicroStrategy sells any Bitcoin by ___ ?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## AI regulation + Big Tech enforcement
- slug: `ai_regulation_big_tech_enforcement`
- strict_matches: 2

### Top strict matches
- (0.700) `676842` — U.S. enacts AI safety bill before 2027?
  - event: U.S. enacts AI safety bill before 2027?
  - matched_terms: `["anchor:ai safety bill", "ai safety bill"]`
- (0.700) `1228017` — SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?
  - event: SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?
  - matched_terms: `["anchor:ftc", "ftc"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.511, rule=0.000) `1426260` — Will AI-chip export licensing become law this year?
  - event: Which bills will become law in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.461, rule=0.000) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.453, rule=0.000) `1426259` — Will Export-control chip security become law this year?
  - event: Which bills will become law in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.452, rule=0.000) `810179` — Will AI be charged with a crime before 2027?
  - event: Will AI be charged with a crime before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.442, rule=0.000) `691340` — AI Industry Downturn by December 31, 2026?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.435, rule=0.000) `691336` — AI Industry Downturn by March 31, 2026?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.430, rule=0.000) `692245` — AI Industry Downturn by December 31, 2025?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.420, rule=0.000) `700396` — Will Perplexity AI be acquired before 2027?
  - event: Which companies will be acquired before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `["acquired"]`
- (sim=0.420, rule=0.000) `676847` — AI model scores ≥ 90% on FrontierMath Benchmark before 2027?
  - event: AI model scores ≥ 90% on FrontierMath Benchmark before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.415, rule=0.000) `1426261` — Will Data center utility cost protection become law this year?
  - event: Which bills will become law in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Data-center power / grid constraints
- slug: `datacenter_power_grid_constraints`
- strict_matches: 2

### Top strict matches
- (0.850) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - matched_terms: `["data center", "moratorium"]`
- (0.850) `1426261` — Will Data center utility cost protection become law this year?
  - event: Which bills will become law in 2026?
  - matched_terms: `["data center", "utility"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.401, rule=0.000) `676796` — Databricks IPO before 2027?
  - event: IPOs before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Antitrust (platforms, app stores, ad markets)
- slug: `antitrust_platforms_app_stores_ads`
- strict_matches: 0

### Top strict matches
_No strict matches._

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## IT spending cycle (enterprise / cloud / AI)
- slug: `it_spending_cycle_enterprise_cloud_ai`
- strict_matches: 24

### Top strict matches
- (1.000) `1322993` — Will the Silicon Data H100 Index (SDH100RT) hit $2.45 (HIGH) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322996` — Will the Silicon Data H100 Index (SDH100RT) hit $2.25 (LOW) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322973` — Will the Silicon Data H100 Index (SDH100RT) hit $2.50 (HIGH) by April 30, 2026?
  - event: GPU rental prices (H100) hit___ by April 30?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322994` — Will the Silicon Data H100 Index (SDH100RT) hit $2.40 (HIGH) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322972` — Will the Silicon Data H100 Index (SDH100RT) hit $2.75 (HIGH) by April 30, 2026?
  - event: GPU rental prices (H100) hit___ by April 30?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322990` — Will the Silicon Data H100 Index (SDH100RT) hit $2.80 (HIGH) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322975` — Will the Silicon Data H100 Index (SDH100RT) hit $2.20 (LOW) by April 30, 2026?
  - event: GPU rental prices (H100) hit___ by April 30?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322992` — Will the Silicon Data H100 Index (SDH100RT) hit $2.50 (HIGH) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322997` — Will the Silicon Data H100 Index (SDH100RT) hit $2.20 (LOW) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`
- (1.000) `1322995` — Will the Silicon Data H100 Index (SDH100RT) hit $2.35 (HIGH) by February 28, 2026?
  - event: GPU rental prices (H100) hit___ in February?
  - matched_terms: `["gpu rental", "gpu rental prices", "h100 index"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.448, rule=0.000) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.416, rule=0.000) `691340` — AI Industry Downturn by December 31, 2026?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.414, rule=0.000) `1370612` — Will Google be the first company to have an AI model hit 1550 on Chatbot Arena in 2026?
  - event: Which company's AI will first hit 1550 on Chatbot Arena in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.405, rule=0.000) `692245` — AI Industry Downturn by December 31, 2025?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.402, rule=0.000) `1370622` — Will Company G be the first company to have an AI model hit 1550 on Chatbot Arena in 2026?
  - event: Which company's AI will first hit 1550 on Chatbot Arena in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Healthcare policy (reform, reimbursement)
- slug: `healthcare_policy_reimbursement`
- strict_matches: 5

### Top strict matches
- (0.850) `902968` — Will ACA premium tax credits be extended and will the Democratic Party win the House in 2026?
  - event: ACA credits extended & House Winner 2026?
  - matched_terms: `["anchor:aca", "premium", "aca"]`
- (0.850) `902969` — Will ACA premium tax credits be extended and will the Republican Party win the House in 2026?
  - event: ACA credits extended & House Winner 2026?
  - matched_terms: `["anchor:aca", "premium", "aca"]`
- (0.850) `902970` — Will ACA premium tax credits not be extended and will the Democratic Party win the House in 2026?
  - event: ACA credits extended & House Winner 2026?
  - matched_terms: `["anchor:aca", "premium", "aca"]`
- (0.850) `902971` — Will ACA premium tax credits not be extended and will the Republican Party win the House in 2026?
  - event: ACA credits extended & House Winner 2026?
  - matched_terms: `["anchor:aca", "premium", "aca"]`
- (0.700) `902972` — Will something else occur?
  - event: ACA credits extended & House Winner 2026?
  - matched_terms: `["anchor:aca", "aca"]`

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## Consumer credit conditions / cycle
- slug: `consumer_credit_conditions_cycle`
- strict_matches: 6

### Top strict matches
- (0.700) `1169842` — Will Trump cap credit card interest rates by January 20, 2026?
  - event: Will Trump cap credit card interest rates by...?
  - matched_terms: `["credit card"]`
- (0.700) `1169843` — Will Trump cap credit card interest rates by March 31, 2026?
  - event: Will Trump cap credit card interest rates by...?
  - matched_terms: `["credit card"]`
- (0.700) `1327147` — Will the U.S. 30-year Fixed-Rate Mortgage hit 6.00% (LOW) by December 31, 2026?
  - event: Will the 30-year Mortgage Rate hit __ in 2026?
  - matched_terms: `["mortgage"]`
- (0.700) `1327142` — Will the U.S. 30-year Fixed-Rate Mortgage hit 7.00% (HIGH) by December 31, 2026?
  - event: Will the 30-year Mortgage Rate hit __ in 2026?
  - matched_terms: `["mortgage"]`
- (0.700) `1327143` — Will the U.S. 30-year Fixed-Rate Mortgage hit 6.75% (HIGH) by December 31, 2026?
  - event: Will the 30-year Mortgage Rate hit __ in 2026?
  - matched_terms: `["mortgage"]`
- (0.700) `1327146` — Will the U.S. 30-year Fixed-Rate Mortgage hit 6.20% (HIGH) by December 31, 2026?
  - event: Will the 30-year Mortgage Rate hit __ in 2026?
  - matched_terms: `["mortgage"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.420, rule=0.000) `665735` — Another US debt downgrade before 2027?
  - event: Another US debt downgrade before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.410, rule=0.000) `665728` — US defaults on debt by 2027?
  - event: US defaults on debt by 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.401, rule=0.000) `677341` — Major U.S. bank bailout before 2027?
  - event: Major U.S. bank bailout before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
