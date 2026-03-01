# Hard Filter Audit

## Run metadata

- decided_at_utc: `2026-02-27T11:14:50.089067+00:00`
- filter_version: `hard_filters_v8`
- config_sha256: `6bc7e216020a44917efaabb0fb3155a93019597f530dabb18c0dfe6bf9f470e4`
- evaluated: `61482`
- rejected: `49577` (80.6%)

## Top rejection reasons

- `reject:sports_market`: 27505
- `reject:winner_template`: 13223
- `reject:micro_price_bets`: 6287
- `reject:entertainment_gossip`: 1674
- `reject:price_target_template`: 1473
- `reject:meme_trivia`: 850
- `reject:political_leader_template`: 404
- `reject:appstore_charts`: 65
- `reject:religion_prophecy`: 2

## Samples by rejection reason

### reject:sports_market

- `550694` (event `26313`) q='Will Italy qualify for the 2026 FIFA World Cup?' vol=206397.824685 liq=3052.7612 tmpl=1.00 eq=0.00 qual=0.81 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550695` (event `26313`) q='Will Netherlands qualify for the 2026 FIFA World Cup?' vol=7759.946623 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550696` (event `26313`) q='Will Belgium qualify for the 2026 FIFA World Cup?' vol=16165.628878 liq=None tmpl=1.00 eq=0.00 qual=0.48 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550697` (event `26313`) q='Will Croatia qualify for the 2026 FIFA World Cup?' vol=6400.949231 liq=None tmpl=1.00 eq=0.00 qual=0.44 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550698` (event `26313`) q='Will Colombia qualify for the 2026 FIFA World Cup?' vol=13673.922584 liq=0.0 tmpl=1.00 eq=0.00 qual=0.47 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550699` (event `26313`) q='Will Uruguay qualify for the 2026 FIFA World Cup?' vol=9211.867177 liq=0.0 tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550700` (event `26313`) q='Will Saudi Arabia qualify for the 2026 FIFA World Cup?' vol=10048.89281 liq=None tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550701` (event `26313`) q='Will Australia qualify for the 2026 FIFA World Cup?' vol=67.9616 liq=None tmpl=1.00 eq=0.00 qual=0.27 rej=True reject=['reject:sports_market'] keep=[]
- `550702` (event `26313`) q='Will Oman qualify for the 2026 FIFA World Cup?' vol=7789.699868 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550703` (event `26313`) q='Will Sweden qualify for the 2026 FIFA World Cup?' vol=99359.289159 liq=5300.0145 tmpl=1.00 eq=0.00 qual=0.80 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550704` (event `26313`) q='Will United Arab Emirates qualify for the 2026 FIFA World Cup?' vol=4269.077475 liq=None tmpl=1.00 eq=0.00 qual=0.43 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550705` (event `26313`) q='Will Austria qualify for the 2026 FIFA World Cup?' vol=1754.384306 liq=0.0 tmpl=1.00 eq=0.00 qual=0.39 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']

### reject:winner_template

- `553824` (event `27829`) q='Will the Carolina Hurricanes win the 2026 NHL Stanley Cup?' vol=127611.604778 liq=100884.6935 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553825` (event `27829`) q='Will the Florida Panthers win the 2026 NHL Stanley Cup?' vol=631070.542737 liq=73292.54254 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553826` (event `27829`) q='Will the Edmonton Oilers win the 2026 NHL Stanley Cup?' vol=285975.199469 liq=44376.7553 tmpl=1.00 eq=0.00 qual=0.91 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553827` (event `27829`) q='Will the Dallas Stars win the 2026 NHL Stanley Cup?' vol=341754.348044 liq=73750.02072 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553828` (event `27829`) q='Will the Colorado Avalanche win the 2026 NHL Stanley Cup?' vol=6767096.369217 liq=108865.21119 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553829` (event `27829`) q='Will the Vegas Golden Knights win the 2026 NHL Stanley Cup?' vol=644293.69311 liq=105395.08773 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553830` (event `27829`) q='Will the Tampa Bay Lightning win the 2026 NHL Stanley Cup?' vol=169882.510332 liq=76300.34943 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553831` (event `27829`) q='Will the Los Angeles Kings win the 2026 NHL Stanley Cup?' vol=6130061.359951 liq=98759.69704 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553832` (event `27829`) q='Will the New Jersey Devils win the 2026 NHL Stanley Cup?' vol=318068.074095 liq=80102.7917 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553833` (event `27829`) q='Will the Winnipeg Jets win the 2026 NHL Stanley Cup?' vol=316653.377617 liq=118210.60258 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553834` (event `27829`) q='Will the Toronto Maple Leafs win the 2026 NHL Stanley Cup?' vol=574165.058892 liq=84921.97403 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553835` (event `27829`) q='Will the Washington Capitals win the 2026 NHL Stanley Cup?' vol=291392.514379 liq=95462.88587 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:micro_price_bets

- `964332` (event `109965`) q='Ethereum Up or Down - December 19, 11:30AM-11:35AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964334` (event `109967`) q='XRP Up or Down - December 19, 11:30AM-11:35AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964335` (event `109968`) q='Bitcoin Up or Down - December 19, 11:35AM-11:40AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964336` (event `109969`) q='XRP Up or Down - December 19, 11:35AM-11:40AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964337` (event `109970`) q='Ethereum Up or Down - December 19, 11:35AM-11:40AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964338` (event `109971`) q='Solana Up or Down - December 19, 11:35AM-11:40AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964343` (event `109976`) q='XRP Up or Down - December 19, 11:40AM-11:45AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964344` (event `109977`) q='Ethereum Up or Down - December 19, 11:40AM-11:45AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964345` (event `109979`) q='Bitcoin Up or Down - December 19, 11:40AM-11:45AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964346` (event `109978`) q='Solana Up or Down - December 19, 11:40AM-11:45AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964347` (event `109980`) q='Bitcoin Up or Down - December 19, 11:45AM-11:50AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']
- `964348` (event `109982`) q='Solana Up or Down - December 19, 11:45AM-11:50AM ET' vol=0.0 liq=0.0 tmpl=0.90 eq=0.00 qual=0.01 rej=True reject=['reject:micro_price_bets'] keep=['quality:ended_penalty']

### reject:entertainment_gossip

- `540817` (event `23784`) q='New Rihanna Album before GTA VI?' vol=640948.909833 liq=25229.5291 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `540818` (event `23784`) q='New Playboi Carti Album before GTA VI?' vol=676414.59404 liq=20605.6005 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613835` (event `50251`) q='Will One Battle After Another win Best Picture at the 98th Academy Awards?' vol=1361396.422424 liq=95754.7114 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613836` (event `50251`) q='Will Hamnet win Best Picture at the 98th Academy Awards?' vol=1706677.981067 liq=76207.71169 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613837` (event `50251`) q='Will Sinners win Best Picture at the 98th Academy Awards?' vol=1177858.38173 liq=56286.33278 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613838` (event `50251`) q='Will Sentimental Value win Best Picture at the 98th Academy Awards?' vol=1018030.748138 liq=97105.91348 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613839` (event `50251`) q='Will Marty Supreme win Best Picture at the 98th Academy Awards?' vol=1788210.225371 liq=46688.96239 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613840` (event `50251`) q='Will Wicked: For Good win Best Picture at the 98th Academy Awards?' vol=655563.816875 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613841` (event `50251`) q='Will Bugonia win Best Picture at the 98th Academy Awards?' vol=1312876.303103 liq=93071.30962 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613842` (event `50251`) q='Will It Was Just an Accident win Best Picture at the 98th Academy Awards?' vol=767105.915249 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613843` (event `50251`) q='Will Jay Kelly win Best Picture at the 98th Academy Awards?' vol=928426.551636 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613844` (event `50251`) q='Will A House of Dynamite win Best Picture at the 98th Academy Awards?' vol=1056888.310835 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']

### reject:price_target_template

- `665324` (event `73105`) q='Will Trump sell over 100k Gold Cards in 2026?' vol=5534.323376 liq=8770.17672 tmpl=0.70 eq=0.00 qual=0.70 rej=True reject=['reject:price_target_template'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `701486` (event `89502`) q='Will Bitcoin reach $200,000 by December 31, 2026?' vol=650154.589024 liq=50570.6697 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701487` (event `89502`) q='Will Bitcoin reach $190,000 by December 31, 2026?' vol=335613.562877 liq=42028.7524 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701488` (event `89502`) q='Will Bitcoin reach $180,000 by December 31, 2026?' vol=314075.590481 liq=45883.0285 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701489` (event `89502`) q='Will Bitcoin reach $170,000 by December 31, 2026?' vol=194970.287251 liq=29348.1428 tmpl=0.70 eq=0.00 qual=0.88 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701490` (event `89502`) q='Will Bitcoin reach $160,000 by December 31, 2026?' vol=298566.019779 liq=53562.3906 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701491` (event `89502`) q='Will Bitcoin reach $150,000 by December 31, 2026?' vol=599872.852897 liq=58401.6567 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701492` (event `89502`) q='Will Bitcoin reach $140,000 by December 31, 2026?' vol=551824.917114 liq=65107.5765 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701493` (event `89502`) q='Will Bitcoin reach $130,000 by December 31, 2026?' vol=547323.919592 liq=64531.4427 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701494` (event `89502`) q='Will Bitcoin reach $120,000 by December 31, 2026?' vol=420413.430851 liq=42126.078 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701495` (event `89502`) q='Will Bitcoin reach $110,000 by December 31, 2026?' vol=471822.342913 liq=36027.1289 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701496` (event `89502`) q='Will Bitcoin reach $100,000 by December 31, 2026?' vol=817818.148363 liq=126401.2006 tmpl=0.70 eq=0.00 qual=0.98 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:meme_trivia

- `1083039` (event `137384`) q='Will Trump say "America" or "American" 25+ times during the 2026 State of the Union address?' vol=150435.955856 liq=16293.34088 tmpl=0.60 eq=0.00 qual=0.77 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty']
- `1083040` (event `137384`) q='Will Trump say "Job" 20+ times during the 2026 State of the Union address?' vol=60793.810796 liq=6086.9446 tmpl=0.60 eq=0.00 qual=0.70 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083041` (event `137384`) q='Will Trump say "Million" or "Billion" or "Trillion" 15+ times during the 2026 State of the Union address?' vol=76203.920752 liq=13085.9011 tmpl=0.60 eq=0.00 qual=0.73 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty']
- `1083042` (event `137384`) q='Will Trump say "Biden" 10+ times during the 2026 State of the Union address?' vol=108464.463556 liq=16205.673 tmpl=0.60 eq=0.00 qual=0.75 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty']
- `1083043` (event `137384`) q='Will Trump say "Border" 7+ times during the 2026 State of the Union address?' vol=21364.591709 liq=5935.4815 tmpl=0.60 eq=0.00 qual=0.66 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083044` (event `137384`) q='Will Trump say "AI" or "Artificial Intelligence" 2+ times during the 2026 State of the Union address?' vol=30614.91011 liq=2844.936 tmpl=0.60 eq=0.00 qual=0.65 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083045` (event `137384`) q='Will Trump say "Hottest" during the 2026 State of the Union address?' vol=49220.445234 liq=5265.8112 tmpl=0.60 eq=0.00 qual=0.69 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083046` (event `137384`) q='Will Trump say "Kamala" or "Harris" during the 2026 State of the Union address?' vol=27235.760777 liq=2320.5604 tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083047` (event `137384`) q='Will Trump say "Kennedy" or "Autism" during the 2026 State of the Union address?' vol=12650.905379 liq=2686.6908 tmpl=0.60 eq=0.00 qual=0.62 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083048` (event `137384`) q='Will Trump say "Middle East" during the 2026 State of the Union address?' vol=10927.31832 liq=5485.5072 tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1083049` (event `137384`) q='Will Trump say "Crypto" or "Bitcoin" during the 2026 State of the Union address?' vol=165406.66799 liq=31897.5641 tmpl=0.60 eq=0.00 qual=0.79 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty']
- `1083050` (event `137384`) q='Will Trump say "Israel" or "Gaza" during the 2026 State of the Union address?' vol=23589.538625 liq=4556.761 tmpl=0.60 eq=0.00 qual=0.66 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']

### reject:political_leader_template

- `562793` (event `32224`) q='Will the Democratic Party control the Senate after the 2026 Midterm elections?' vol=238645.447452 liq=116710.5169 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562794` (event `32224`) q='Will the Republican Party control the Senate after the 2026 Midterm elections?' vol=360167.95281 liq=89542.7146 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562795` (event `32224`) q='Will Party A control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562796` (event `32224`) q='Will Party B control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562797` (event `32224`) q='Will Party C control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562798` (event `32224`) q='Will Party D control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562799` (event `32224`) q='Will Party E control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562800` (event `32224`) q='Will Party F control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562801` (event `32224`) q='Will another party control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562802` (event `32225`) q='Will the Democratic Party control the House after the 2026 Midterm elections?' vol=1758473.692887 liq=224748.0169 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562803` (event `32225`) q='Will the Republican Party control the House after the 2026 Midterm elections?' vol=1642608.84706 liq=215312.2961 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562804` (event `32225`) q='Will Party A control the House after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.01 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:ended_penalty']

### reject:appstore_charts

- `1402465` (event `219250`) q='Will Shadowrocket be #1 Paid App in the US Apple App Store on February 27?' vol=7778.501935 liq=1160.5975 tmpl=0.80 eq=0.00 qual=0.57 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402466` (event `219250`) q='Will HotSchedules be #1 Paid App in the US Apple App Store on February 27?' vol=5202.460017 liq=1331.7343 tmpl=0.80 eq=0.00 qual=0.56 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402467` (event `219250`) q='Will SkyView be #1 Paid App in the US Apple App Store on February 27?' vol=5375.911505 liq=2016.0971 tmpl=0.80 eq=0.00 qual=0.57 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402468` (event `219250`) q='Will Procreate Pocket be #1 Paid App in the US Apple App Store on February 27?' vol=1398.9151 liq=1111.90938 tmpl=0.80 eq=0.00 qual=0.50 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402469` (event `219250`) q='Will AnkiMobile Flashcards be #1 Paid App in the US Apple App Store on February 27?' vol=1096.9925 liq=1703.62095 tmpl=0.80 eq=0.00 qual=0.51 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402470` (event `219250`) q='Will TeamSpeak 3 be #1 Paid App in the US Apple App Store on February 27?' vol=212.616845 liq=1607.96775 tmpl=0.80 eq=0.00 qual=0.44 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1402471` (event `219250`) q='Will TonalEnergy Tuner & Metronome be #1 Paid App in the US Apple App Store on February 27?' vol=896.538 liq=1980.34728 tmpl=0.80 eq=0.00 qual=0.50 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1402472` (event `219250`) q='Will Current Reader be #1 Paid App in the US Apple App Store on February 27?' vol=1923.631 liq=1234.89995 tmpl=0.80 eq=0.00 qual=0.52 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402473` (event `219250`) q='Will App A be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402474` (event `219250`) q='Will App B be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402475` (event `219250`) q='Will App C be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402476` (event `219250`) q='Will App D be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']

### reject:religion_prophecy

- `540819` (event `23784`) q='Will Jesus Christ return before GTA VI?' vol=9555220.2173 liq=895699.9108 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']
- `703258` (event `90178`) q='Will Jesus Christ return before 2027?' vol=34105337.680513 liq=4128023.1497 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']

## Kept high relevance (examples)

- `1403678` (event `219797`) q='Trump sued over tariff powers again by March 31?' vol=43286.238691 liq=27311.87699 tmpl=0.00 eq=1.00 qual=0.82 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:macro', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_high']
- `665729` (event `73332`) q='US congress stock trading ban before 2027?' vol=14682.654232 liq=4284.859 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693776` (event `86397`) q='Will Aristotle self-certify sports event contracts by March 31, 2026?' vol=22947.622966 liq=93.4784 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693777` (event `86397`) q='Will Railbird self-certify sports event contracts by March 31, 2026?' vol=40261.723251 liq=2012.7129 tmpl=0.00 eq=0.80 qual=0.74 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693778` (event `86397`) q='Will ForecastEx self-certify sports event contracts by March 31, 2026?' vol=30723.221938 liq=2891.6704 tmpl=0.00 eq=0.80 qual=0.74 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693779` (event `86397`) q='Will the Chicago Mercantile Exchange self-certify sports event contracts by March 31, 2026?' vol=None liq=None tmpl=0.00 eq=0.80 qual=0.10 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `693780` (event `86397`) q='Will Cboe Futures Exchange self-certify sports event contracts by March 31, 2026?' vol=9225.0 liq=58.3071 tmpl=0.00 eq=0.80 qual=0.58 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `693781` (event `86397`) q='Will Intercontinental Exchange self-certify sports event contracts by March 31, 2026?' vol=23491.180908 liq=111.4527 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693782` (event `86397`) q='Will the Small Exchange self-certify sports event contracts by March 31, 2026?' vol=23975.494914 liq=2353.6064 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693783` (event `86397`) q='Will LedgerX self-certify sports event contracts by March 31, 2026?' vol=2.0 liq=79.9014 tmpl=0.00 eq=0.80 qual=0.27 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `701299` (event `86397`) q='Will The Clearing Company self-certify sports event contracts by March 31, 2026?' vol=512.546 liq=97.18274 tmpl=0.00 eq=0.80 qual=0.48 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1198966` (event `168384`) q='Von der Leyen out as European Commission President in 2026?' vol=10548.925687 liq=6521.4604 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `1199759` (event `168607`) q='Will Marine Le Pen win her appeal to lift ineligibility ban in 2026?' vol=4909.17138 liq=4922.9656 tmpl=0.00 eq=0.80 qual=0.68 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1228017` (event `176964`) q='SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?' vol=1244.150963 liq=110.21883 tmpl=0.00 eq=0.80 qual=0.52 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `1236477` (event `179563`) q='Will Trump act to ban mail-in voting or voting machines by June 30?' vol=1890.656968 liq=7221.2236 tmpl=0.00 eq=0.80 qual=0.66 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1243055` (event `181500`) q='Jack Smith charged by March 31?' vol=879.509461 liq=130.9506 tmpl=0.00 eq=0.80 qual=0.51 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1300240` (event `193766`) q='Will CA River Plate win on 2026-02-26?' vol=1744.343619 liq=27601.4826 tmpl=0.00 eq=0.80 qual=0.61 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_high', 'quality:ended_penalty']
- `1300242` (event `193766`) q='Will CA Banfield win on 2026-02-26?' vol=861.574593 liq=24466.4749 tmpl=0.00 eq=0.80 qual=0.58 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high', 'quality:ended_penalty']
- `1327734` (event `197715`) q='Will CA Banfield win on 2026-03-02?' vol=None liq=19721.7332 tmpl=0.00 eq=0.80 qual=0.39 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1327736` (event `197715`) q='Will CA Aldosivi win on 2026-03-02?' vol=None liq=19713.7222 tmpl=0.00 eq=0.80 qual=0.39 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']

## Kept low quality (examples)

- `651492` (event `66156`) q='Will A rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651493` (event `66156`) q='Will B rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651494` (event `66156`) q='Will C rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651495` (event `66156`) q='Will D rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651496` (event `66156`) q='Will E rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651497` (event `66156`) q='Will F rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651498` (event `66156`) q='Will G rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651499` (event `66156`) q='Will H rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651500` (event `66156`) q='Will I rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651501` (event `66156`) q='Will J rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651502` (event `66156`) q='Will K rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651503` (event `66156`) q='Will L rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651504` (event `66156`) q='Will M rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651505` (event `66156`) q='Will N rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651506` (event `66156`) q='Will O rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651507` (event `66156`) q='Will P rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651508` (event `66156`) q='Will Q rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651509` (event `66156`) q='Will R rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651510` (event `66156`) q='Will S rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']
- `651511` (event `66156`) q='Will T rank #1 among boy names on the SSA’s official list for 2025?' vol=0.0 liq=0.0 tmpl=0.00 eq=0.00 qual=0.01 rej=False reject=[] keep=['quality:ended_penalty']

## Top kept by volume_usd

- `572473` (event `35908`) vol=97459856.293881 liq=1320633.1048 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Judy Shelton as the next Fed chair?'
- `654412` (event `67284`) vol=72622688.170742 liq=2244282.92974 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?'
- `654415` (event `67284`) vol=62496973.798652 liq=1870913.44267 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?'
- `1198423` (event `114242`) vol=53935700.816245 liq=242410.1544 tmpl=0.0 eq=0.0 qual=0.915 reasons=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty'] q='US strikes Iran by February 28, 2026?'
- `572469` (event `35908`) vol=43563388.236807 liq=327596.69724 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Warsh as the next Fed chair?'
- `1092199` (event `114242`) vol=41754060.055673 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by January 31, 2026?'
- `572481` (event `35908`) vol=38196117.661053 liq=1680035.34537 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Scott Bessent as the next Fed chair?'
- `572470` (event `35908`) vol=31345456.756387 liq=742054.15524 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Hassett as the next Fed chair?'
- `572485` (event `35908`) vol=28598076.075916 liq=1014220.81837 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Rick Rieder as the next Fed chair?'
- `997488` (event `118172`) vol=28546167.301582 liq=580267.97877 tmpl=0.0 eq=0.7 qual=1.0 reasons=['relevance:corporate_actions', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump acquire Greenland before 2027?'
- `572478` (event `35908`) vol=27746129.76542 liq=5252930.2246 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Jerome Powell as the next Fed chair?'
- `572471` (event `35908`) vol=24461176.31611 liq=280154.26548 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Christopher Waller as the next Fed chair?'
- `572472` (event `35908`) vol=24458475.328131 liq=2402541.82671 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Bill Pulte as the next Fed chair?'
- `1105752` (event `143443`) vol=23900005.664566 liq=87087.55533 tmpl=0.0 eq=0.0 qual=0.981761522088125 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Frank Donovan be the leader of Venezuela end of 2026?'
- `572494` (event `35908`) vol=23505646.036 liq=3044492.48983 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate himself as the next Fed chair?'
- `572486` (event `35908`) vol=22217565.278402 liq=296625.91678 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Michelle Bowman as the next Fed chair?'
- `654413` (event `67284`) vol=21696499.659679 liq=1504336.98874 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?'
- `572489` (event `35908`) vol=21309692.069942 liq=3014856.58931 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Janet Yellen as the next Fed chair?'
- `654414` (event `67284`) vol=21166187.866522 liq=1102608.34206 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will there be no change in Fed interest rates after the March 2026 meeting?'
- `572476` (event `35908`) vol=21107894.068664 liq=3197495.37364 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Arthur Laffer as the next Fed chair?'
- `572492` (event `35908`) vol=20877940.96291 liq=3323115.04179 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Barron Trump as the next Fed chair?'
- `572480` (event `35908`) vol=20393611.682784 liq=418664.42691 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Stephen Miran as the next Fed chair?'
- `572506` (event `35908`) vol=20105469.609432 liq=322628.08537 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate no one before 2027?'
- `561829` (event `31759`) vol=20009997.689384 liq=710843.01573 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Russia x Ukraine ceasefire by March 31, 2026?'
- `984441` (event `114242`) vol=19441112.027333 liq=304094.1148 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='US strikes Iran by March 31, 2026?'
- `1320793` (event `114242`) vol=18810054.309004 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 20, 2026?'
- `516926` (event `16167`) vol=17976157.529867 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='MicroStrategy sells any Bitcoin in 2025?'
- `572484` (event `35908`) vol=17905674.56491 liq=2869822.68439 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate David Zervos as the next Fed chair?'
- `1335520` (event `114242`) vol=17561112.38258 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 9, 2026?'
- `916732` (event `102773`) vol=17304500.136419 liq=407764.2897 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Khamenei out as Supreme Leader of Iran by March 31?'

## Top rejected by volume_usd

- `553861` (event `27830`) vol=47812063.36217 liq=377148.11239 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Indiana Pacers win the 2026 NBA Finals?'
- `559684` (event `30829`) vol=40080473.3229 liq=507736.05902 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Chelsea Clinton win the 2028 Democratic presidential nomination?'
- `566203` (event `33507`) vol=38355230.032948 liq=1783573.3612 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Leeds win the 2025–26 English Premier League?'
- `559687` (event `30829`) vol=35866844.916393 liq=1853514.73112 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Oprah Winfrey win the 2028 Democratic presidential nomination?'
- `703258` (event `90178`) vol=34105337.680513 liq=4128023.1497 tmpl=0.9 eq=0.0 qual=1.0 reasons=['reject:religion_prophecy'] q='Will Jesus Christ return before 2027?'
- `559688` (event `30829`) vol=32425588.266853 liq=1467327.87372 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Andrew Yang win the 2028 Democratic presidential nomination?'
- `559683` (event `30829`) vol=32128976.969983 liq=592809.79963 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will George Clooney win the 2028 Democratic presidential nomination?'
- `561247` (event `31552`) vol=32125095.507029 liq=1197356.07634 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 US Presidential Election?'
- `561251` (event `31552`) vol=31946663.985108 liq=452814.15904 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 US Presidential Election?'
- `553874` (event `27830`) vol=31894293.028182 liq=1048305.61047 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Memphis Grizzlies win the 2026 NBA Finals?'
- `559677` (event `30829`) vol=31106412.706477 liq=1106211.62521 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hillary Clinton win the 2028 Democratic presidential nomination?'
- `559685` (event `30829`) vol=30561727.365933 liq=1834840.02484 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will MrBeast win the 2028 Democratic presidential nomination?'
- `566192` (event `33507`) vol=30340641.717611 liq=1322651.92165 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Tottenham win the 2025–26 English Premier League?'
- `559671` (event `30829`) vol=30050479.071768 liq=1598232.87096 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Zohran Mamdani win the 2028 Democratic presidential nomination?'
- `559679` (event `30829`) vol=29945747.722596 liq=1378385.8334 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Bernie Sanders win the 2028 Democratic presidential nomination?'
- `559681` (event `30829`) vol=28800765.471987 liq=1826425.77141 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 Democratic presidential nomination?'
- `566174` (event `33506`) vol=28392439.058395 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Slavia Pragu win the 2025–26 Champions League?'
- `1303355` (event `194107`) vol=28318696.73917 liq=3430108.38457 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:price_target_template'] q='Will Bitcoin reach $150,000 in February?'
- `561249` (event `31552`) vol=28194177.939292 liq=426718.20567 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Greg Abbott win the 2028 US Presidential Election?'
- `559680` (event `30829`) vol=27752874.667152 liq=1589622.22343 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Phil Murphy win the 2028 Democratic presidential nomination?'
- `559678` (event `30829`) vol=27324608.069839 liq=1196702.70707 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Liz Cheney win the 2028 Democratic presidential nomination?'
- `559666` (event `30829`) vol=26642145.223795 liq=1636018.0661 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 Democratic presidential nomination?'
- `559682` (event `30829`) vol=25470214.834375 liq=1544838.47411 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hunter Biden win the 2028 Democratic presidential nomination?'
- `561995` (event `31875`) vol=25027479.980739 liq=717463.09827 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Mike Pence win the 2028 Republican presidential nomination?'
- `561242` (event `31552`) vol=24490282.800928 liq=698287.92068 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tulsi Gabbard win the 2028 US Presidential Election?'
- `559690` (event `30829`) vol=23737153.606912 liq=1883630.52707 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Kim Kardashian win the 2028 Democratic presidential nomination?'
- `559670` (event `30829`) vol=23187493.777775 liq=830771.62195 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Gina Raimondo win the 2028 Democratic presidential nomination?'
- `559689` (event `30829`) vol=23001201.569776 liq=858738.81201 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Beto O’Rourke win the 2028 Democratic presidential nomination?'
- `561248` (event `31552`) vol=21365784.304414 liq=716254.00856 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Vivek Ramaswamy win the 2028 US Presidential Election?'
- `566167` (event `33506`) vol=21360158.2305 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Olympiakos win the 2025–26 Champions League?'
