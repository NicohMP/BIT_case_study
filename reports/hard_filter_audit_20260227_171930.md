# Hard Filter Audit

## Run metadata

- decided_at_utc: `2026-02-27T17:19:30.324284+00:00`
- filter_version: `hard_filters_v8`
- config_sha256: `6bc7e216020a44917efaabb0fb3155a93019597f530dabb18c0dfe6bf9f470e4`
- evaluated: `62640`
- rejected: `50598` (80.8%)

## Top rejection reasons

- `reject:sports_market`: 28081
- `reject:winner_template`: 13235
- `reject:micro_price_bets`: 6697
- `reject:entertainment_gossip`: 1674
- `reject:price_target_template`: 1508
- `reject:meme_trivia`: 850
- `reject:political_leader_template`: 404
- `reject:appstore_charts`: 65
- `reject:religion_prophecy`: 2

## Samples by rejection reason

### reject:sports_market

- `550694` (event `26313`) q='Will Italy qualify for the 2026 FIFA World Cup?' vol=206464.37391 liq=3157.4053 tmpl=1.00 eq=0.00 qual=0.82 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550695` (event `26313`) q='Will Netherlands qualify for the 2026 FIFA World Cup?' vol=7759.946623 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550696` (event `26313`) q='Will Belgium qualify for the 2026 FIFA World Cup?' vol=16165.628878 liq=None tmpl=1.00 eq=0.00 qual=0.48 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550697` (event `26313`) q='Will Croatia qualify for the 2026 FIFA World Cup?' vol=6400.949231 liq=None tmpl=1.00 eq=0.00 qual=0.44 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550698` (event `26313`) q='Will Colombia qualify for the 2026 FIFA World Cup?' vol=13673.922584 liq=0.0 tmpl=1.00 eq=0.00 qual=0.47 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550699` (event `26313`) q='Will Uruguay qualify for the 2026 FIFA World Cup?' vol=9211.867177 liq=0.0 tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550700` (event `26313`) q='Will Saudi Arabia qualify for the 2026 FIFA World Cup?' vol=10048.89281 liq=None tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550701` (event `26313`) q='Will Australia qualify for the 2026 FIFA World Cup?' vol=67.9616 liq=None tmpl=1.00 eq=0.00 qual=0.27 rej=True reject=['reject:sports_market'] keep=[]
- `550702` (event `26313`) q='Will Oman qualify for the 2026 FIFA World Cup?' vol=7789.699868 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550703` (event `26313`) q='Will Sweden qualify for the 2026 FIFA World Cup?' vol=99727.838125 liq=4878.3786 tmpl=1.00 eq=0.00 qual=0.80 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550704` (event `26313`) q='Will United Arab Emirates qualify for the 2026 FIFA World Cup?' vol=4269.077475 liq=None tmpl=1.00 eq=0.00 qual=0.43 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550705` (event `26313`) q='Will Austria qualify for the 2026 FIFA World Cup?' vol=1754.384306 liq=0.0 tmpl=1.00 eq=0.00 qual=0.39 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']

### reject:winner_template

- `553824` (event `27829`) q='Will the Carolina Hurricanes win the 2026 NHL Stanley Cup?' vol=128233.070503 liq=101428.3708 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553825` (event `27829`) q='Will the Florida Panthers win the 2026 NHL Stanley Cup?' vol=633084.937887 liq=70776.82205 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553826` (event `27829`) q='Will the Edmonton Oilers win the 2026 NHL Stanley Cup?' vol=287062.768567 liq=44747.6508 tmpl=1.00 eq=0.00 qual=0.91 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553827` (event `27829`) q='Will the Dallas Stars win the 2026 NHL Stanley Cup?' vol=344392.97687 liq=72687.71782 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553828` (event `27829`) q='Will the Colorado Avalanche win the 2026 NHL Stanley Cup?' vol=6822113.515287 liq=109337.15957 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553829` (event `27829`) q='Will the Vegas Golden Knights win the 2026 NHL Stanley Cup?' vol=645752.953381 liq=104872.69816 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553830` (event `27829`) q='Will the Tampa Bay Lightning win the 2026 NHL Stanley Cup?' vol=170212.843976 liq=75422.94193 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553831` (event `27829`) q='Will the Los Angeles Kings win the 2026 NHL Stanley Cup?' vol=6130846.247495 liq=99209.62125 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553832` (event `27829`) q='Will the New Jersey Devils win the 2026 NHL Stanley Cup?' vol=318810.140095 liq=80170.08818 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553833` (event `27829`) q='Will the Winnipeg Jets win the 2026 NHL Stanley Cup?' vol=318210.855493 liq=117518.847 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553834` (event `27829`) q='Will the Toronto Maple Leafs win the 2026 NHL Stanley Cup?' vol=574593.465011 liq=95570.3534 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553835` (event `27829`) q='Will the Washington Capitals win the 2026 NHL Stanley Cup?' vol=291724.843844 liq=97632.07721 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `540817` (event `23784`) q='New Rihanna Album before GTA VI?' vol=640961.779833 liq=25046.7081 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `540818` (event `23784`) q='New Playboi Carti Album before GTA VI?' vol=676427.836261 liq=21519.291 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613835` (event `50251`) q='Will One Battle After Another win Best Picture at the 98th Academy Awards?' vol=1365112.507227 liq=97382.7029 tmpl=0.60 eq=0.00 qual=0.99 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613836` (event `50251`) q='Will Hamnet win Best Picture at the 98th Academy Awards?' vol=1715682.923439 liq=78052.17903 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613837` (event `50251`) q='Will Sinners win Best Picture at the 98th Academy Awards?' vol=1180688.940636 liq=55167.06039 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613838` (event `50251`) q='Will Sentimental Value win Best Picture at the 98th Academy Awards?' vol=1020045.043938 liq=96155.47482 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613839` (event `50251`) q='Will Marty Supreme win Best Picture at the 98th Academy Awards?' vol=1795225.945913 liq=48292.39465 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613840` (event `50251`) q='Will Wicked: For Good win Best Picture at the 98th Academy Awards?' vol=655563.816875 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613841` (event `50251`) q='Will Bugonia win Best Picture at the 98th Academy Awards?' vol=1321056.703103 liq=92867.46188 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613842` (event `50251`) q='Will It Was Just an Accident win Best Picture at the 98th Academy Awards?' vol=767105.915249 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613843` (event `50251`) q='Will Jay Kelly win Best Picture at the 98th Academy Awards?' vol=928426.551636 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613844` (event `50251`) q='Will A House of Dynamite win Best Picture at the 98th Academy Awards?' vol=1056888.310835 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']

### reject:price_target_template

- `665324` (event `73105`) q='Will Trump sell over 100k Gold Cards in 2026?' vol=5534.323376 liq=8480.87703 tmpl=0.70 eq=0.00 qual=0.70 rej=True reject=['reject:price_target_template'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `701486` (event `89502`) q='Will Bitcoin reach $200,000 by December 31, 2026?' vol=653721.092509 liq=50966.3638 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701487` (event `89502`) q='Will Bitcoin reach $190,000 by December 31, 2026?' vol=338336.112877 liq=44466.463 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701488` (event `89502`) q='Will Bitcoin reach $180,000 by December 31, 2026?' vol=314789.870481 liq=47010.4806 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701489` (event `89502`) q='Will Bitcoin reach $170,000 by December 31, 2026?' vol=196651.222964 liq=31400.9883 tmpl=0.70 eq=0.00 qual=0.88 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701490` (event `89502`) q='Will Bitcoin reach $160,000 by December 31, 2026?' vol=299911.839779 liq=55067.7412 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701491` (event `89502`) q='Will Bitcoin reach $150,000 by December 31, 2026?' vol=600649.352897 liq=59489.4017 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701492` (event `89502`) q='Will Bitcoin reach $140,000 by December 31, 2026?' vol=551879.790592 liq=66166.8425 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701493` (event `89502`) q='Will Bitcoin reach $130,000 by December 31, 2026?' vol=547331.611898 liq=65671.929 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701494` (event `89502`) q='Will Bitcoin reach $120,000 by December 31, 2026?' vol=420489.861326 liq=41773.7996 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701495` (event `89502`) q='Will Bitcoin reach $110,000 by December 31, 2026?' vol=472210.391921 liq=36060.7965 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701496` (event `89502`) q='Will Bitcoin reach $100,000 by December 31, 2026?' vol=819405.995981 liq=93579.4551 tmpl=0.70 eq=0.00 qual=0.97 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `562793` (event `32224`) q='Will the Democratic Party control the Senate after the 2026 Midterm elections?' vol=238706.417452 liq=115976.5189 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562794` (event `32224`) q='Will the Republican Party control the Senate after the 2026 Midterm elections?' vol=360176.286142 liq=91031.4006 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562795` (event `32224`) q='Will Party A control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562796` (event `32224`) q='Will Party B control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562797` (event `32224`) q='Will Party C control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562798` (event `32224`) q='Will Party D control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562799` (event `32224`) q='Will Party E control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562800` (event `32224`) q='Will Party F control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562801` (event `32224`) q='Will another party control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562802` (event `32225`) q='Will the Democratic Party control the House after the 2026 Midterm elections?' vol=1764188.179629 liq=220223.1778 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562803` (event `32225`) q='Will the Republican Party control the House after the 2026 Midterm elections?' vol=1661822.807135 liq=212953.3341 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562804` (event `32225`) q='Will Party A control the House after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.01 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:ended_penalty']

### reject:appstore_charts

- `1402465` (event `219250`) q='Will Shadowrocket be #1 Paid App in the US Apple App Store on February 27?' vol=11055.947879 liq=4084.937 tmpl=0.80 eq=0.00 qual=0.62 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402466` (event `219250`) q='Will HotSchedules be #1 Paid App in the US Apple App Store on February 27?' vol=6448.145274 liq=4794.65263 tmpl=0.80 eq=0.00 qual=0.61 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402467` (event `219250`) q='Will SkyView be #1 Paid App in the US Apple App Store on February 27?' vol=5375.911505 liq=3843.71328 tmpl=0.80 eq=0.00 qual=0.59 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402468` (event `219250`) q='Will Procreate Pocket be #1 Paid App in the US Apple App Store on February 27?' vol=1398.9151 liq=3457.41903 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402469` (event `219250`) q='Will AnkiMobile Flashcards be #1 Paid App in the US Apple App Store on February 27?' vol=1096.9925 liq=4102.73741 tmpl=0.80 eq=0.00 qual=0.53 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402470` (event `219250`) q='Will TeamSpeak 3 be #1 Paid App in the US Apple App Store on February 27?' vol=212.616845 liq=3613.97245 tmpl=0.80 eq=0.00 qual=0.46 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1402471` (event `219250`) q='Will TonalEnergy Tuner & Metronome be #1 Paid App in the US Apple App Store on February 27?' vol=896.538 liq=4010.64665 tmpl=0.80 eq=0.00 qual=0.52 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1402472` (event `219250`) q='Will Current Reader be #1 Paid App in the US Apple App Store on February 27?' vol=1923.631 liq=3956.70992 tmpl=0.80 eq=0.00 qual=0.55 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1402473` (event `219250`) q='Will App A be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402474` (event `219250`) q='Will App B be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402475` (event `219250`) q='Will App C be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']
- `1402476` (event `219250`) q='Will App D be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.01 rej=True reject=['reject:appstore_charts'] keep=['quality:ended_penalty']

### reject:religion_prophecy

- `540819` (event `23784`) q='Will Jesus Christ return before GTA VI?' vol=9558476.309409 liq=898585.9202 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']
- `703258` (event `90178`) q='Will Jesus Christ return before 2027?' vol=34302230.08217 liq=4134554.03835 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']

## Kept high relevance (examples)

- `1403678` (event `219797`) q='Trump sued over tariff powers again by March 31?' vol=43544.370691 liq=31208.80182 tmpl=0.00 eq=1.00 qual=0.82 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:macro', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_high']
- `665729` (event `73332`) q='US congress stock trading ban before 2027?' vol=14720.444924 liq=4715.5252 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693776` (event `86397`) q='Will Aristotle self-certify sports event contracts by March 31, 2026?' vol=23929.622966 liq=95.0459 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693777` (event `86397`) q='Will Railbird self-certify sports event contracts by March 31, 2026?' vol=42133.039038 liq=2062.8749 tmpl=0.00 eq=0.80 qual=0.74 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693778` (event `86397`) q='Will ForecastEx self-certify sports event contracts by March 31, 2026?' vol=30761.001938 liq=2868.1414 tmpl=0.00 eq=0.80 qual=0.74 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693779` (event `86397`) q='Will the Chicago Mercantile Exchange self-certify sports event contracts by March 31, 2026?' vol=None liq=None tmpl=0.00 eq=0.80 qual=0.10 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `693780` (event `86397`) q='Will Cboe Futures Exchange self-certify sports event contracts by March 31, 2026?' vol=9225.0 liq=70.2115 tmpl=0.00 eq=0.80 qual=0.58 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `693781` (event `86397`) q='Will Intercontinental Exchange self-certify sports event contracts by March 31, 2026?' vol=23491.180908 liq=99.5063 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693782` (event `86397`) q='Will the Small Exchange self-certify sports event contracts by March 31, 2026?' vol=24824.494914 liq=2294.2321 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693783` (event `86397`) q='Will LedgerX self-certify sports event contracts by March 31, 2026?' vol=2.0 liq=87.8803 tmpl=0.00 eq=0.80 qual=0.27 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `701299` (event `86397`) q='Will The Clearing Company self-certify sports event contracts by March 31, 2026?' vol=520.048671 liq=101.6086 tmpl=0.00 eq=0.80 qual=0.48 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1198966` (event `168384`) q='Von der Leyen out as European Commission President in 2026?' vol=10548.925687 liq=6771.7642 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `1199759` (event `168607`) q='Will Marine Le Pen win her appeal to lift ineligibility ban in 2026?' vol=4933.126072 liq=5923.5649 tmpl=0.00 eq=0.80 qual=0.69 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1228017` (event `176964`) q='SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?' vol=1244.150963 liq=83.89789 tmpl=0.00 eq=0.80 qual=0.51 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `1236477` (event `179563`) q='Will Trump act to ban mail-in voting or voting machines by June 30?' vol=1890.656968 liq=8051.8349 tmpl=0.00 eq=0.80 qual=0.66 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1243055` (event `181500`) q='Jack Smith charged by March 31?' vol=879.509461 liq=155.7149 tmpl=0.00 eq=0.80 qual=0.51 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1300240` (event `193766`) q='Will CA River Plate win on 2026-02-26?' vol=1744.343619 liq=27601.4826 tmpl=0.00 eq=0.80 qual=0.61 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_high', 'quality:ended_penalty']
- `1300242` (event `193766`) q='Will CA Banfield win on 2026-02-26?' vol=861.574593 liq=24466.4749 tmpl=0.00 eq=0.80 qual=0.58 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high', 'quality:ended_penalty']
- `1327734` (event `197715`) q='Will CA Banfield win on 2026-03-02?' vol=None liq=21383.404 tmpl=0.00 eq=0.80 qual=0.39 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1327736` (event `197715`) q='Will CA Aldosivi win on 2026-03-02?' vol=None liq=21459.5245 tmpl=0.00 eq=0.80 qual=0.39 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']

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

- `572473` (event `35908`) vol=97598620.388187 liq=1310266.83742 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Judy Shelton as the next Fed chair?'
- `654412` (event `67284`) vol=74375583.918019 liq=2194390.86734 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?'
- `654415` (event `67284`) vol=63817117.027564 liq=1529587.29894 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?'
- `1198423` (event `114242`) vol=57344276.800799 liq=465253.4514 tmpl=0.0 eq=0.0 qual=0.915 reasons=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty'] q='US strikes Iran by February 28, 2026?'
- `572469` (event `35908`) vol=43672017.575907 liq=238184.4789 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Warsh as the next Fed chair?'
- `1092199` (event `114242`) vol=41754060.055673 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by January 31, 2026?'
- `572481` (event `35908`) vol=38214810.331053 liq=1674649.26731 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Scott Bessent as the next Fed chair?'
- `572470` (event `35908`) vol=31577784.88322 liq=752901.1098 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Hassett as the next Fed chair?'
- `572485` (event `35908`) vol=28819893.256916 liq=804383.7168 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Rick Rieder as the next Fed chair?'
- `997488` (event `118172`) vol=28570331.414415 liq=560806.20923 tmpl=0.0 eq=0.7 qual=1.0 reasons=['relevance:corporate_actions', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump acquire Greenland before 2027?'
- `572478` (event `35908`) vol=27746138.05542 liq=5257012.83037 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Jerome Powell as the next Fed chair?'
- `572471` (event `35908`) vol=24502163.327109 liq=241092.00292 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Christopher Waller as the next Fed chair?'
- `572472` (event `35908`) vol=24458475.328131 liq=2405157.28732 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Bill Pulte as the next Fed chair?'
- `1105752` (event `143443`) vol=23908119.120341 liq=97849.50761 tmpl=0.0 eq=0.0 qual=0.985159888012976 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Frank Donovan be the leader of Venezuela end of 2026?'
- `572494` (event `35908`) vol=23507646.036 liq=3045397.99896 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate himself as the next Fed chair?'
- `572486` (event `35908`) vol=22238603.729402 liq=295714.44991 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Michelle Bowman as the next Fed chair?'
- `654413` (event `67284`) vol=21805489.345923 liq=1376444.99485 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?'
- `654414` (event `67284`) vol=21420185.508298 liq=985900.95712 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will there be no change in Fed interest rates after the March 2026 meeting?'
- `572489` (event `35908`) vol=21310692.069942 liq=3016397.49799 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Janet Yellen as the next Fed chair?'
- `572476` (event `35908`) vol=21107894.068664 liq=3200064.29832 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Arthur Laffer as the next Fed chair?'
- `572492` (event `35908`) vol=20877940.96291 liq=3327084.21241 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Barron Trump as the next Fed chair?'
- `572480` (event `35908`) vol=20404315.286784 liq=417229.02242 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Stephen Miran as the next Fed chair?'
- `572506` (event `35908`) vol=20125050.451264 liq=311586.9518 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate no one before 2027?'
- `561829` (event `31759`) vol=20058905.252137 liq=684224.95164 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Russia x Ukraine ceasefire by March 31, 2026?'
- `984441` (event `114242`) vol=20034529.724812 liq=170048.5821 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='US strikes Iran by March 31, 2026?'
- `1320793` (event `114242`) vol=18810054.309004 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 20, 2026?'
- `516926` (event `16167`) vol=17976157.529867 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='MicroStrategy sells any Bitcoin in 2025?'
- `572484` (event `35908`) vol=17905674.56491 liq=2872389.61924 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate David Zervos as the next Fed chair?'
- `1335520` (event `114242`) vol=17561112.38258 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 9, 2026?'
- `916732` (event `102773`) vol=17534878.726808 liq=264348.9157 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Khamenei out as Supreme Leader of Iran by March 31?'

## Top rejected by volume_usd

- `553861` (event `27830`) vol=47813154.36217 liq=380609.04845 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Indiana Pacers win the 2026 NBA Finals?'
- `559684` (event `30829`) vol=40243093.8429 liq=348917.96037 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Chelsea Clinton win the 2028 Democratic presidential nomination?'
- `566203` (event `33507`) vol=38355328.202948 liq=1822059.94335 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Leeds win the 2025–26 English Premier League?'
- `559687` (event `30829`) vol=35887016.324629 liq=1828045.85605 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Oprah Winfrey win the 2028 Democratic presidential nomination?'
- `703258` (event `90178`) vol=34302230.08217 liq=4134554.03835 tmpl=0.9 eq=0.0 qual=1.0 reasons=['reject:religion_prophecy'] q='Will Jesus Christ return before 2027?'
- `561247` (event `31552`) vol=32551315.844438 liq=1187453.33406 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 US Presidential Election?'
- `559688` (event `30829`) vol=32430717.038741 liq=1463111.49515 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Andrew Yang win the 2028 Democratic presidential nomination?'
- `559683` (event `30829`) vol=32158726.222483 liq=579594.90359 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will George Clooney win the 2028 Democratic presidential nomination?'
- `561251` (event `31552`) vol=31950790.067883 liq=450097.02907 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 US Presidential Election?'
- `553874` (event `27830`) vol=31907501.540182 liq=1046837.07116 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Memphis Grizzlies win the 2026 NBA Finals?'
- `559677` (event `30829`) vol=31138451.440963 liq=1089655.49891 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hillary Clinton win the 2028 Democratic presidential nomination?'
- `559685` (event `30829`) vol=30564132.805933 liq=1832856.43933 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will MrBeast win the 2028 Democratic presidential nomination?'
- `566192` (event `33507`) vol=30340641.717611 liq=1368213.79363 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Tottenham win the 2025–26 English Premier League?'
- `559671` (event `30829`) vol=30063768.541674 liq=1585901.89299 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Zohran Mamdani win the 2028 Democratic presidential nomination?'
- `559679` (event `30829`) vol=29957099.551846 liq=1370096.5308 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Bernie Sanders win the 2028 Democratic presidential nomination?'
- `559681` (event `30829`) vol=28894915.566319 liq=1777388.40173 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 Democratic presidential nomination?'
- `1303355` (event `194107`) vol=28483598.63917 liq=3249901.55063 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:price_target_template'] q='Will Bitcoin reach $150,000 in February?'
- `566174` (event `33506`) vol=28392439.058395 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Slavia Pragu win the 2025–26 Champions League?'
- `561249` (event `31552`) vol=28197957.820201 liq=424947.85737 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Greg Abbott win the 2028 US Presidential Election?'
- `559680` (event `30829`) vol=27761430.975552 liq=1585337.55074 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Phil Murphy win the 2028 Democratic presidential nomination?'
- `559678` (event `30829`) vol=27328081.740393 liq=1193770.09561 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Liz Cheney win the 2028 Democratic presidential nomination?'
- `559666` (event `30829`) vol=26653364.573795 liq=1614756.26464 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 Democratic presidential nomination?'
- `559682` (event `30829`) vol=25482131.158485 liq=1533542.88637 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hunter Biden win the 2028 Democratic presidential nomination?'
- `561995` (event `31875`) vol=25045551.80892 liq=712512.95314 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Mike Pence win the 2028 Republican presidential nomination?'
- `561242` (event `31552`) vol=24497620.202746 liq=691134.79494 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tulsi Gabbard win the 2028 US Presidential Election?'
- `559690` (event `30829`) vol=23744884.531537 liq=1880024.9234 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Kim Kardashian win the 2028 Democratic presidential nomination?'
- `559670` (event `30829`) vol=23192285.544884 liq=826749.19861 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Gina Raimondo win the 2028 Democratic presidential nomination?'
- `559689` (event `30829`) vol=23022832.779776 liq=856332.19879 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Beto O’Rourke win the 2028 Democratic presidential nomination?'
- `561248` (event `31552`) vol=21368419.314414 liq=709934.50331 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Vivek Ramaswamy win the 2028 US Presidential Election?'
- `566167` (event `33506`) vol=21360158.2305 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Olympiakos win the 2025–26 Champions League?'
