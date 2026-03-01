# Hard Filter Audit

## Run metadata

- decided_at_utc: `2026-02-28T15:33:22.506651+00:00`
- filter_version: `hard_filters_v8`
- config_sha256: `6bc7e216020a44917efaabb0fb3155a93019597f530dabb18c0dfe6bf9f470e4`
- evaluated: `52646`
- rejected: `41236` (78.3%)

## Top rejection reasons

- `reject:sports_market`: 24098
- `reject:winner_template`: 13025
- `reject:micro_price_bets`: 2217
- `reject:entertainment_gossip`: 1498
- `reject:price_target_template`: 1052
- `reject:meme_trivia`: 596
- `reject:political_leader_template`: 389
- `reject:appstore_charts`: 65
- `reject:religion_prophecy`: 2

## Samples by rejection reason

### reject:sports_market

- `550694` (event `26313`) q='Will Italy qualify for the 2026 FIFA World Cup?' vol=206614.331792 liq=2402.8431 tmpl=1.00 eq=0.00 qual=0.81 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550695` (event `26313`) q='Will Netherlands qualify for the 2026 FIFA World Cup?' vol=7759.946623 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550696` (event `26313`) q='Will Belgium qualify for the 2026 FIFA World Cup?' vol=16165.628878 liq=None tmpl=1.00 eq=0.00 qual=0.48 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550697` (event `26313`) q='Will Croatia qualify for the 2026 FIFA World Cup?' vol=6400.949231 liq=None tmpl=1.00 eq=0.00 qual=0.44 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550698` (event `26313`) q='Will Colombia qualify for the 2026 FIFA World Cup?' vol=13673.922584 liq=0.0 tmpl=1.00 eq=0.00 qual=0.47 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550699` (event `26313`) q='Will Uruguay qualify for the 2026 FIFA World Cup?' vol=9211.867177 liq=0.0 tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550700` (event `26313`) q='Will Saudi Arabia qualify for the 2026 FIFA World Cup?' vol=10048.89281 liq=None tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550701` (event `26313`) q='Will Australia qualify for the 2026 FIFA World Cup?' vol=67.9616 liq=None tmpl=1.00 eq=0.00 qual=0.27 rej=True reject=['reject:sports_market'] keep=[]
- `550702` (event `26313`) q='Will Oman qualify for the 2026 FIFA World Cup?' vol=7789.699868 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550703` (event `26313`) q='Will Sweden qualify for the 2026 FIFA World Cup?' vol=100598.974439 liq=3558.7327 tmpl=1.00 eq=0.00 qual=0.79 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550704` (event `26313`) q='Will United Arab Emirates qualify for the 2026 FIFA World Cup?' vol=4269.077475 liq=None tmpl=1.00 eq=0.00 qual=0.43 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550705` (event `26313`) q='Will Austria qualify for the 2026 FIFA World Cup?' vol=1754.384306 liq=0.0 tmpl=1.00 eq=0.00 qual=0.39 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']

### reject:winner_template

- `553824` (event `27829`) q='Will the Carolina Hurricanes win the 2026 NHL Stanley Cup?' vol=131779.343431 liq=97519.6216 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553825` (event `27829`) q='Will the Florida Panthers win the 2026 NHL Stanley Cup?' vol=634465.36699 liq=73471.61584 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553826` (event `27829`) q='Will the Edmonton Oilers win the 2026 NHL Stanley Cup?' vol=288376.643563 liq=45569.4662 tmpl=1.00 eq=0.00 qual=0.91 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553827` (event `27829`) q='Will the Dallas Stars win the 2026 NHL Stanley Cup?' vol=353756.951253 liq=75138.68568 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553828` (event `27829`) q='Will the Colorado Avalanche win the 2026 NHL Stanley Cup?' vol=6970172.941487 liq=106585.26953 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553829` (event `27829`) q='Will the Vegas Golden Knights win the 2026 NHL Stanley Cup?' vol=650836.203051 liq=108440.86334 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553830` (event `27829`) q='Will the Tampa Bay Lightning win the 2026 NHL Stanley Cup?' vol=173330.983479 liq=76182.94144 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553831` (event `27829`) q='Will the Los Angeles Kings win the 2026 NHL Stanley Cup?' vol=6135570.296577 liq=101645.25329 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553832` (event `27829`) q='Will the New Jersey Devils win the 2026 NHL Stanley Cup?' vol=321686.492595 liq=83222.36592 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553833` (event `27829`) q='Will the Winnipeg Jets win the 2026 NHL Stanley Cup?' vol=319152.494944 liq=120209.15648 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553834` (event `27829`) q='Will the Toronto Maple Leafs win the 2026 NHL Stanley Cup?' vol=575429.987685 liq=98220.29331 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553835` (event `27829`) q='Will the Washington Capitals win the 2026 NHL Stanley Cup?' vol=292486.476315 liq=93792.38665 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `540817` (event `23784`) q='New Rihanna Album before GTA VI?' vol=641636.383532 liq=24570.7294 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `540818` (event `23784`) q='New Playboi Carti Album before GTA VI?' vol=676817.547688 liq=18069.2709 tmpl=0.60 eq=0.00 qual=0.91 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613835` (event `50251`) q='Will One Battle After Another win Best Picture at the 98th Academy Awards?' vol=1402588.607696 liq=55094.2279 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613836` (event `50251`) q='Will Hamnet win Best Picture at the 98th Academy Awards?' vol=1740213.925131 liq=61101.68774 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613837` (event `50251`) q='Will Sinners win Best Picture at the 98th Academy Awards?' vol=1202088.078233 liq=52305.13385 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613838` (event `50251`) q='Will Sentimental Value win Best Picture at the 98th Academy Awards?' vol=1051854.145064 liq=107300.37535 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613839` (event `50251`) q='Will Marty Supreme win Best Picture at the 98th Academy Awards?' vol=1824009.662734 liq=45285.42034 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613840` (event `50251`) q='Will Wicked: For Good win Best Picture at the 98th Academy Awards?' vol=655563.816875 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613841` (event `50251`) q='Will Bugonia win Best Picture at the 98th Academy Awards?' vol=1369165.093833 liq=111522.88155 tmpl=0.60 eq=0.00 qual=0.99 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613842` (event `50251`) q='Will It Was Just an Accident win Best Picture at the 98th Academy Awards?' vol=767105.915249 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613843` (event `50251`) q='Will Jay Kelly win Best Picture at the 98th Academy Awards?' vol=928426.551636 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613844` (event `50251`) q='Will A House of Dynamite win Best Picture at the 98th Academy Awards?' vol=1056888.310835 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']

### reject:price_target_template

- `665324` (event `73105`) q='Will Trump sell over 100k Gold Cards in 2026?' vol=5582.894803 liq=8417.26572 tmpl=0.70 eq=0.00 qual=0.70 rej=True reject=['reject:price_target_template'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `701486` (event `89502`) q='Will Bitcoin reach $200,000 by December 31, 2026?' vol=658600.156709 liq=55324.4301 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701487` (event `89502`) q='Will Bitcoin reach $190,000 by December 31, 2026?' vol=340206.787633 liq=45785.4799 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701488` (event `89502`) q='Will Bitcoin reach $180,000 by December 31, 2026?' vol=316498.700481 liq=36335.1292 tmpl=0.70 eq=0.00 qual=0.90 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701489` (event `89502`) q='Will Bitcoin reach $170,000 by December 31, 2026?' vol=196654.862964 liq=30681.4975 tmpl=0.70 eq=0.00 qual=0.88 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701490` (event `89502`) q='Will Bitcoin reach $160,000 by December 31, 2026?' vol=300216.499779 liq=52487.1793 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701491` (event `89502`) q='Will Bitcoin reach $150,000 by December 31, 2026?' vol=602087.854239 liq=56299.6718 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701492` (event `89502`) q='Will Bitcoin reach $140,000 by December 31, 2026?' vol=557330.293614 liq=57299.5267 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701493` (event `89502`) q='Will Bitcoin reach $130,000 by December 31, 2026?' vol=555534.615741 liq=61580.3353 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701494` (event `89502`) q='Will Bitcoin reach $120,000 by December 31, 2026?' vol=424041.29893 liq=34243.7114 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701495` (event `89502`) q='Will Bitcoin reach $110,000 by December 31, 2026?' vol=476348.425439 liq=34227.9451 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701496` (event `89502`) q='Will Bitcoin reach $100,000 by December 31, 2026?' vol=825292.661875 liq=96039.9336 tmpl=0.70 eq=0.00 qual=0.97 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:meme_trivia

- `1255799` (event `184873`) q='Will Elon Musk post 0-19 tweets in March 2026?' vol=113238.92932 liq=26276.80419 tmpl=0.60 eq=0.00 qual=0.85 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255801` (event `184873`) q='Will Elon Musk post 20-39 tweets in March 2026?' vol=44001.832625 liq=22895.26263 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255803` (event `184873`) q='Will Elon Musk post 40-59 tweets in March 2026?' vol=68943.039552 liq=24550.79725 tmpl=0.60 eq=0.00 qual=0.83 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255805` (event `184873`) q='Will Elon Musk post 60-79 tweets in March 2026?' vol=47825.973416 liq=20961.14589 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255808` (event `184873`) q='Will Elon Musk post 80-99 tweets in March 2026?' vol=53657.029166 liq=21338.4738 tmpl=0.60 eq=0.00 qual=0.82 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255810` (event `184873`) q='Will Elon Musk post 100-119 tweets in March 2026?' vol=32116.913332 liq=27068.50451 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255812` (event `184873`) q='Will Elon Musk post 120-139 tweets in March 2026?' vol=38761.8515 liq=23670.73321 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255814` (event `184873`) q='Will Elon Musk post 140-159 tweets in March 2026?' vol=29313.948166 liq=24269.13439 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255816` (event `184873`) q='Will Elon Musk post 160-179 tweets in March 2026?' vol=27017.936499 liq=23157.79099 tmpl=0.60 eq=0.00 qual=0.79 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255819` (event `184873`) q='Will Elon Musk post 180-199 tweets in March 2026?' vol=29707.407904 liq=25548.02133 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255821` (event `184873`) q='Will Elon Musk post 200-219 tweets in March 2026?' vol=30655.487999 liq=20927.68446 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255824` (event `184873`) q='Will Elon Musk post 220-239 tweets in March 2026?' vol=21266.226415 liq=16094.65152 tmpl=0.60 eq=0.00 qual=0.77 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:political_leader_template

- `562793` (event `32224`) q='Will the Democratic Party control the Senate after the 2026 Midterm elections?' vol=239080.47867 liq=109714.4882 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562794` (event `32224`) q='Will the Republican Party control the Senate after the 2026 Midterm elections?' vol=361171.052807 liq=86370.0426 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562795` (event `32224`) q='Will Party A control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562796` (event `32224`) q='Will Party B control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562797` (event `32224`) q='Will Party C control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562798` (event `32224`) q='Will Party D control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562799` (event `32224`) q='Will Party E control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562800` (event `32224`) q='Will Party F control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562801` (event `32224`) q='Will another party control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562802` (event `32225`) q='Will the Democratic Party control the House after the 2026 Midterm elections?' vol=1769333.642987 liq=222589.607 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562803` (event `32225`) q='Will the Republican Party control the House after the 2026 Midterm elections?' vol=1678361.219632 liq=203662.1173 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562804` (event `32225`) q='Will Party A control the House after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.01 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:ended_penalty']

### reject:appstore_charts

- `1402598` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 22?' vol=35098.372531 liq=None tmpl=0.80 eq=0.00 qual=0.43 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402599` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 24?' vol=15056.440058 liq=None tmpl=0.80 eq=0.00 qual=0.39 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402600` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 26?' vol=16396.910339 liq=None tmpl=0.80 eq=0.00 qual=0.40 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402601` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 28?' vol=10035.826406 liq=315.3895 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1449762` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by March 15?' vol=1865.502857 liq=13990.7246 tmpl=0.80 eq=0.00 qual=0.59 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_high', 'quality:ended_penalty']
- `1449763` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by March 31?' vol=180.466874 liq=2088.1677 tmpl=0.80 eq=0.00 qual=0.44 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1455928` (event `234983`) q='Will Shadowrocket be #1 Paid App in the US Apple App Store on March 6?' vol=1163.762951 liq=1207.8835 tmpl=0.80 eq=0.00 qual=0.58 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1455929` (event `234983`) q='Will HotSchedules be #1 Paid App in the US Apple App Store on March 6?' vol=448.220254 liq=852.8534 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=[]
- `1455930` (event `234983`) q='Will SkyView be #1 Paid App in the US Apple App Store on March 6?' vol=479.4821 liq=1430.64857 tmpl=0.80 eq=0.00 qual=0.55 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1455931` (event `234983`) q='Will Procreate Pocket be #1 Paid App in the US Apple App Store on March 6?' vol=463.08525 liq=793.63795 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=[]
- `1455932` (event `234983`) q='Will AnkiMobile Flashcards be #1 Paid App in the US Apple App Store on March 6?' vol=712.662125 liq=1600.12495 tmpl=0.80 eq=0.00 qual=0.57 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1455933` (event `234983`) q='Will Paprika Recipe Manager 3 be #1 Paid App in the US Apple App Store on March 6?' vol=632.86875 liq=1321.00488 tmpl=0.80 eq=0.00 qual=0.56 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']

### reject:religion_prophecy

- `540819` (event `23784`) q='Will Jesus Christ return before GTA VI?' vol=9588221.756877 liq=1142198.4063 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']
- `703258` (event `90178`) q='Will Jesus Christ return before 2027?' vol=35095239.247901 liq=3630316.00322 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']

## Kept high relevance (examples)

- `1403678` (event `219797`) q='Trump sued over tariff powers again by March 31?' vol=51559.965691 liq=19645.29829 tmpl=0.00 eq=1.00 qual=0.81 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:macro', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_high']
- `665729` (event `73332`) q='US congress stock trading ban before 2027?' vol=14742.444924 liq=2745.6636 tmpl=0.00 eq=0.80 qual=0.71 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693776` (event `86397`) q='Will Aristotle self-certify sports event contracts by March 31, 2026?' vol=27581.702966 liq=2794.6551 tmpl=0.00 eq=0.80 qual=0.73 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693777` (event `86397`) q='Will Railbird self-certify sports event contracts by March 31, 2026?' vol=42133.039038 liq=190.2706 tmpl=0.00 eq=0.80 qual=0.67 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693778` (event `86397`) q='Will ForecastEx self-certify sports event contracts by March 31, 2026?' vol=31597.708642 liq=982.9463 tmpl=0.00 eq=0.80 qual=0.71 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693779` (event `86397`) q='Will the Chicago Mercantile Exchange self-certify sports event contracts by March 31, 2026?' vol=None liq=None tmpl=0.00 eq=0.80 qual=0.10 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `693780` (event `86397`) q='Will Cboe Futures Exchange self-certify sports event contracts by March 31, 2026?' vol=9225.0 liq=77.0195 tmpl=0.00 eq=0.80 qual=0.59 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `693781` (event `86397`) q='Will Intercontinental Exchange self-certify sports event contracts by March 31, 2026?' vol=23491.180908 liq=103.0889 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693782` (event `86397`) q='Will the Small Exchange self-certify sports event contracts by March 31, 2026?' vol=26703.494914 liq=111.3495 tmpl=0.00 eq=0.80 qual=0.64 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693783` (event `86397`) q='Will LedgerX self-certify sports event contracts by March 31, 2026?' vol=2.0 liq=72.9653 tmpl=0.00 eq=0.80 qual=0.27 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `701299` (event `86397`) q='Will The Clearing Company self-certify sports event contracts by March 31, 2026?' vol=520.048671 liq=71.51289 tmpl=0.00 eq=0.80 qual=0.47 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1198966` (event `168384`) q='Von der Leyen out as European Commission President in 2026?' vol=10548.925687 liq=5732.6534 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `1199759` (event `168607`) q='Will Marine Le Pen win her appeal to lift ineligibility ban in 2026?' vol=4940.266072 liq=3803.9511 tmpl=0.00 eq=0.80 qual=0.67 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1228017` (event `176964`) q='SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?' vol=1244.150963 liq=72.59974 tmpl=0.00 eq=0.80 qual=0.51 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `1236477` (event `179563`) q='Will Trump act to ban mail-in voting or voting machines by June 30?' vol=1896.364109 liq=6727.3021 tmpl=0.00 eq=0.80 qual=0.65 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1243055` (event `181500`) q='Jack Smith charged by March 31?' vol=879.509461 liq=101.5677 tmpl=0.00 eq=0.80 qual=0.50 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1327734` (event `197715`) q='Will CA Banfield win on 2026-03-02?' vol=None liq=67863.6141 tmpl=0.00 eq=0.80 qual=0.42 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1327736` (event `197715`) q='Will CA Aldosivi win on 2026-03-02?' vol=None liq=68555.7433 tmpl=0.00 eq=0.80 qual=0.42 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1352764` (event `201497`) q='Will CA Barracas Central win on 2026-03-06?' vol=None liq=97.2469 tmpl=0.00 eq=0.80 qual=0.23 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1352768` (event `201497`) q='Will CA Banfield win on 2026-03-06?' vol=None liq=95.9945 tmpl=0.00 eq=0.80 qual=0.23 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']

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

- `572473` (event `35908`) vol=98818470.052209 liq=1103651.10538 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Judy Shelton as the next Fed chair?'
- `654412` (event `67284`) vol=76514318.306683 liq=1554382.41939 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?'
- `654415` (event `67284`) vol=65502807.291602 liq=1846936.36642 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?'
- `572469` (event `35908`) vol=43943770.293565 liq=220849.09518 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Warsh as the next Fed chair?'
- `572481` (event `35908`) vol=38304312.621053 liq=1595529.61243 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Scott Bessent as the next Fed chair?'
- `572470` (event `35908`) vol=31802228.507365 liq=763530.86789 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Hassett as the next Fed chair?'
- `572485` (event `35908`) vol=29027126.071576 liq=695553.47925 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Rick Rieder as the next Fed chair?'
- `997488` (event `118172`) vol=28766283.765283 liq=383370.44358 tmpl=0.0 eq=0.7 qual=1.0 reasons=['relevance:corporate_actions', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump acquire Greenland before 2027?'
- `572478` (event `35908`) vol=27748141.69542 liq=627897.31487 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Jerome Powell as the next Fed chair?'
- `572471` (event `35908`) vol=24729587.179171 liq=211067.73788 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Christopher Waller as the next Fed chair?'
- `572472` (event `35908`) vol=24500475.328131 liq=2362163.14526 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Bill Pulte as the next Fed chair?'
- `1105754` (event `143443`) vol=24288530.127163 liq=140940.85617 tmpl=0.0 eq=0.0 qual=0.995802995904472 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Richard Grenell be the leader of Venezuela end of 2026?'
- `1105752` (event `143443`) vol=23941740.501341 liq=100888.99053 tmpl=0.0 eq=0.0 qual=0.986052091653186 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Frank Donovan be the leader of Venezuela end of 2026?'
- `1180303` (event `162818`) vol=23592208.888984 liq=175689.28144 tmpl=0.0 eq=0.0 qual=0.915 reasons=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty'] q='Khamenei out as Supreme Leader of Iran by February 28?'
- `572494` (event `35908`) vol=23508646.036 liq=3043350.2834 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate himself as the next Fed chair?'
- `654413` (event `67284`) vol=23284685.647289 liq=516229.36651 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?'
- `572486` (event `35908`) vol=22903812.5779 liq=421253.98385 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Michelle Bowman as the next Fed chair?'
- `654414` (event `67284`) vol=22807877.502316 liq=472005.70581 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will there be no change in Fed interest rates after the March 2026 meeting?'
- `916732` (event `102773`) vol=22807757.101663 liq=301317.2473 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Khamenei out as Supreme Leader of Iran by March 31?'
- `572489` (event `35908`) vol=21311692.069942 liq=3016438.6614 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Janet Yellen as the next Fed chair?'
- `572476` (event `35908`) vol=21108894.068664 liq=3199049.24379 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Arthur Laffer as the next Fed chair?'
- `572492` (event `35908`) vol=20878940.96291 liq=3327083.65511 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Barron Trump as the next Fed chair?'
- `572480` (event `35908`) vol=20684559.982137 liq=269013.99994 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Stephen Miran as the next Fed chair?'
- `561829` (event `31759`) vol=20495331.495942 liq=383457.24374 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Russia x Ukraine ceasefire by March 31, 2026?'
- `572506` (event `35908`) vol=20405771.107681 liq=219313.72511 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate no one before 2027?'
- `516926` (event `16167`) vol=17976157.529867 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='MicroStrategy sells any Bitcoin in 2025?'
- `572484` (event `35908`) vol=17906674.56491 liq=2871516.92222 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate David Zervos as the next Fed chair?'
- `572479` (event `35908`) vol=12626617.884833 liq=3051539.9915 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Ron Paul as the next Fed chair?'
- `703257` (event `90177`) vol=11620352.227947 liq=1512388.6523 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will the US confirm that aliens exist before 2027?'
- `572488` (event `35908`) vol=10797098.951725 liq=2896265.59327 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Philip Jefferson as the next Fed chair?'

## Top rejected by volume_usd

- `553861` (event `27830`) vol=47827622.59217 liq=384742.7111 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Indiana Pacers win the 2026 NBA Finals?'
- `559684` (event `30829`) vol=40293492.528514 liq=329013.12645 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Chelsea Clinton win the 2028 Democratic presidential nomination?'
- `566203` (event `33507`) vol=38357203.212948 liq=2038642.29792 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Leeds win the 2025–26 English Premier League?'
- `559687` (event `30829`) vol=36062948.267405 liq=1698675.10142 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Oprah Winfrey win the 2028 Democratic presidential nomination?'
- `703258` (event `90178`) vol=35095239.247901 liq=3630316.00322 tmpl=0.9 eq=0.0 qual=1.0 reasons=['reject:religion_prophecy'] q='Will Jesus Christ return before 2027?'
- `561247` (event `31552`) vol=32699856.84821 liq=1109351.90418 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 US Presidential Election?'
- `559688` (event `30829`) vol=32532093.132512 liq=1401431.12081 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Andrew Yang win the 2028 Democratic presidential nomination?'
- `559683` (event `30829`) vol=32214830.794093 liq=557013.36876 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will George Clooney win the 2028 Democratic presidential nomination?'
- `561251` (event `31552`) vol=32076593.446274 liq=472370.44606 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 US Presidential Election?'
- `553874` (event `27830`) vol=32040695.398182 liq=995886.65959 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Memphis Grizzlies win the 2026 NBA Finals?'
- `559677` (event `30829`) vol=31290474.421765 liq=1008039.6853 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hillary Clinton win the 2028 Democratic presidential nomination?'
- `559685` (event `30829`) vol=30634728.896817 liq=1790167.61398 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will MrBeast win the 2028 Democratic presidential nomination?'
- `566192` (event `33507`) vol=30341659.247611 liq=1597539.45849 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Tottenham win the 2025–26 English Premier League?'
- `559671` (event `30829`) vol=30208873.871283 liq=1503369.30245 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Zohran Mamdani win the 2028 Democratic presidential nomination?'
- `559679` (event `30829`) vol=30156312.158956 liq=1432922.42802 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Bernie Sanders win the 2028 Democratic presidential nomination?'
- `559681` (event `30829`) vol=28968009.575536 liq=1707490.36907 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 Democratic presidential nomination?'
- `1303355` (event `194107`) vol=28635512.18917 liq=3123594.74186 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:price_target_template'] q='Will Bitcoin reach $150,000 in February?'
- `566174` (event `33506`) vol=28392439.058395 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Slavia Pragu win the 2025–26 Champions League?'
- `561249` (event `31552`) vol=28212200.011976 liq=397911.00812 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Greg Abbott win the 2028 US Presidential Election?'
- `559680` (event `30829`) vol=27797042.421909 liq=1602011.61048 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Phil Murphy win the 2028 Democratic presidential nomination?'
- `559678` (event `30829`) vol=27398381.765938 liq=1165611.70332 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Liz Cheney win the 2028 Democratic presidential nomination?'
- `559666` (event `30829`) vol=26818021.350128 liq=1638568.47032 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 Democratic presidential nomination?'
- `559682` (event `30829`) vol=25534279.244034 liq=1499948.20348 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hunter Biden win the 2028 Democratic presidential nomination?'
- `561995` (event `31875`) vol=25087761.026794 liq=697650.65152 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Mike Pence win the 2028 Republican presidential nomination?'
- `561242` (event `31552`) vol=24548316.777034 liq=647143.32809 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tulsi Gabbard win the 2028 US Presidential Election?'
- `559690` (event `30829`) vol=23798338.156966 liq=1851620.01511 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Kim Kardashian win the 2028 Democratic presidential nomination?'
- `1423580` (event `226986`) vol=23721086.33 liq=20319.68993 tmpl=0.6 eq=0.0 qual=0.939315683252285 reasons=['reject:meme_trivia'] q='Will Elon Musk post 0-19 tweets from February 27 to March 6, 2026?'
- `559670` (event `30829`) vol=23267500.388767 liq=792225.32692 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Gina Raimondo win the 2028 Democratic presidential nomination?'
- `559689` (event `30829`) vol=23100399.85928 liq=845300.58284 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Beto O’Rourke win the 2028 Democratic presidential nomination?'
- `561248` (event `31552`) vol=22322548.429074 liq=418923.47685 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Vivek Ramaswamy win the 2028 US Presidential Election?'
