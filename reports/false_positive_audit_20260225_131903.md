# False Positive Audit Snapshot (Step 3)

- as_of_utc: `2026-02-25T13:19:03.464459+00:00`
- filter_version: `hard_filters_v8`
- matcher_version: `matcher_v4`

## Monetary policy surprises (FOMC)
- slug: `fomc_surprises`
- strict_matches: 201

### Top strict matches
- (1.000) `654412` — Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `654415` — Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `654414` — Will there be no change in Fed interest rates after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `654413` — Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?
  - event: Fed decision in March?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `616902` — Will no Fed rate cuts happen in 2026?
  - event: How many Fed rate cuts in 2026?
  - matched_terms: `["fed", "powell", "rate cut"]`
- (1.000) `616908` — Will 6 Fed rate cuts happen in 2026?
  - event: How many Fed rate cuts in 2026?
  - matched_terms: `["fed", "powell", "rate cut"]`
- (1.000) `669660` — Will the Fed decrease interest rates by 50+ bps after the April 2026 meeting?
  - event: Fed decision in April?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `616914` — Will 12 or more Fed rate cuts happen in 2026?
  - event: How many Fed rate cuts in 2026?
  - matched_terms: `["fed", "powell", "rate cut"]`
- (1.000) `669663` — Will the Fed increase interest rates by 25+ bps after the April 2026 meeting?
  - event: Fed decision in April?
  - matched_terms: `["fed", "powell", "interest rate"]`
- (1.000) `949492` — Fed rate cut by January 2026 meeting?
  - event: Fed rate cut by...?
  - matched_terms: `["fed", "powell", "rate cut"]`

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## Real yields / long rates
- slug: `real_yields_long_rates`
- strict_matches: 17

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

## US–China semiconductor export controls
- slug: `us_china_semis_export_controls`
- strict_matches: 0

### Top strict matches
_No strict matches._

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## Taiwan geopolitical risk
- slug: `taiwan_geopolitical_risk`
- strict_matches: 8

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
- (0.850) `1040944` — Will Xi Jinping meet with Cheng Li-wun by June 30?
  - event: Will Xi Jinping meet with Cheng Li-wun by June 30?
  - matched_terms: `["taiwan", "china"]`
- (0.850) `1131161` — Lai Ching-te out as President of Taiwan in 2026?
  - event: Lai Ching-te out as President of Taiwan in 2026?
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
- (sim=0.454, rule=0.000) `677408` — China x Philippines military clash before 2027?
  - event: China x Philippines military clash before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["china"]`
  - exclusions_hit: `[]`
- (sim=0.440, rule=0.000) `687642` — China x Japan military clash before 2027?
  - event: China x Japan military clash before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["china"]`
  - exclusions_hit: `[]`
- (sim=0.432, rule=0.000) `1066556` — Lai Ching-te impeached by June 30?
  - event: Lai Ching-te impeached by June 30?
  - anchors_hit: `[]`
  - keyword_hits: `["taiwan"]`
  - exclusions_hit: `[]`
- (sim=0.410, rule=0.000) `665243` — NATO article 5 before 2027?
  - event: NATO article 5 before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.401, rule=0.000) `681313` — US takes Panama Canal before 2027?
  - event: US takes Panama Canal before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Crypto regulation regime changes
- slug: `crypto_regime_changes`
- strict_matches: 26

### Top strict matches
- (0.850) `1303356` — Will XRP reach $4.00 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303360` — Will XRP reach $3.40 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303368` — Will XRP reach $3.00 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303401` — Will XRP dip to $1.00 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303364` — Will XRP reach $3.20 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303405` — Will XRP dip to $0.80 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303409` — Will XRP dip to $0.60 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303378` — Will XRP reach $2.40 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303385` — Will XRP reach $2.00 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`
- (0.850) `1303382` — Will XRP reach $2.20 in February?
  - event: What price will XRP hit in February?
  - matched_terms: `["ripple", "xrp"]`

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
- (sim=0.470, rule=0.000) `1068733` — Will stablecoins hit $500B before 2027?
  - event: Will stablecoins hit $500B before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["stablecoins"]`
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
  - keyword_hits: `["kraken"]`
  - exclusions_hit: `[]`

## AI regulation + Big Tech enforcement
- slug: `ai_regulation_big_tech_enforcement`
- strict_matches: 7

### Top strict matches
- (0.700) `700396` — Will Perplexity AI be acquired before 2027?
  - event: Which companies will be acquired before 2027?
  - matched_terms: `["big tech"]`
- (0.700) `691340` — AI Industry Downturn by December 31, 2026?
  - event: AI bubble burst by...?
  - matched_terms: `["big tech"]`
- (0.700) `692245` — AI Industry Downturn by December 31, 2025?
  - event: AI bubble burst by...?
  - matched_terms: `["big tech"]`
- (0.700) `691336` — AI Industry Downturn by March 31, 2026?
  - event: AI bubble burst by...?
  - matched_terms: `["big tech"]`
- (0.700) `810179` — Will AI be charged with a crime before 2027?
  - event: Will AI be charged with a crime before 2027?
  - matched_terms: `["big tech"]`
- (0.700) `676847` — AI model scores ≥ 90% on FrontierMath Benchmark before 2027?
  - event: AI model scores ≥ 90% on FrontierMath Benchmark before 2027?
  - matched_terms: `["big tech"]`
- (0.700) `1228017` — SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?
  - event: SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?
  - matched_terms: `["ftc"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.525, rule=0.000) `676842` — U.S. enacts AI safety bill before 2027?
  - event: U.S. enacts AI safety bill before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.461, rule=0.000) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.404, rule=0.000) `1163699` — Clarity Act signed into law in 2026?
  - event: Clarity Act signed into law in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Data-center power / grid constraints
- slug: `datacenter_power_grid_constraints`
- strict_matches: 0

### Top strict matches
_No strict matches._

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.460, rule=0.000) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `["data center"]`
  - exclusions_hit: `[]`
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
- strict_matches: 2

### Top strict matches
- (0.700) `1302430` — AWS service disrupted by March 31?
  - event: AWS service disrupted by March 31?
  - matched_terms: `["aws"]`
- (0.700) `1363808` — Services Down Parlay
  - event: Services Down Parlay
  - matched_terms: `["aws"]`

### Borderline discovery (high similarity, rejected by rules)
- (sim=0.463, rule=0.000) `957986` — AI data center moratorium passed before 2027?
  - event: AI data center moratorium passed before 2027?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.438, rule=0.000) `691340` — AI Industry Downturn by December 31, 2026?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.432, rule=0.000) `692245` — AI Industry Downturn by December 31, 2025?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.418, rule=0.000) `1370612` — Will Google be the first company to have an AI model hit 1550 on Chatbot Arena in 2026?
  - event: Which company's AI will first hit 1550 on Chatbot Arena in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.415, rule=0.000) `691336` — AI Industry Downturn by March 31, 2026?
  - event: AI bubble burst by...?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.402, rule=0.000) `1277248` — Will Google have the third-best AI model at the end of February 2026?
  - event: Which company has the third best AI model end of February?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.402, rule=0.000) `1277495` — Will Google have the #3 AI model at the end of February 2026?
  - event: Which company has the #3 AI model end of February? (Style Control On)
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`
- (sim=0.400, rule=0.000) `1370611` — Will Anthropic be the first company to have an AI model hit 1550 on Chatbot Arena in 2026?
  - event: Which company's AI will first hit 1550 on Chatbot Arena in 2026?
  - anchors_hit: `[]`
  - keyword_hits: `[]`
  - exclusions_hit: `[]`

## Healthcare policy (reform, reimbursement)
- slug: `healthcare_policy_reimbursement`
- strict_matches: 4

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

### Borderline discovery (high similarity, rejected by rules)
_None found (or embeddings disabled)._

## Consumer credit conditions / cycle
- slug: `consumer_credit_conditions_cycle`
- strict_matches: 2

### Top strict matches
- (0.700) `1169842` — Will Trump cap credit card interest rates by January 20, 2026?
  - event: Will Trump cap credit card interest rates by...?
  - matched_terms: `["credit card"]`
- (0.700) `1169843` — Will Trump cap credit card interest rates by March 31, 2026?
  - event: Will Trump cap credit card interest rates by...?
  - matched_terms: `["credit card"]`

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
