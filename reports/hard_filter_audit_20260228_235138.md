# Hard Filter Audit

## Run metadata

- decided_at_utc: `2026-02-28T23:51:38.720334+00:00`
- filter_version: `hard_filters_v8`
- config_sha256: `6bc7e216020a44917efaabb0fb3155a93019597f530dabb18c0dfe6bf9f470e4`
- evaluated: `55447`
- rejected: `43541` (78.5%)

## Top rejection reasons

- `reject:sports_market`: 25716
- `reject:winner_template`: 13026
- `reject:micro_price_bets`: 2797
- `reject:entertainment_gossip`: 1498
- `reject:price_target_template`: 1142
- `reject:meme_trivia`: 613
- `reject:political_leader_template`: 389
- `reject:appstore_charts`: 65
- `reject:religion_prophecy`: 2

## Samples by rejection reason

### reject:sports_market

- `550694` (event `26313`) q='Will Italy qualify for the 2026 FIFA World Cup?' vol=206700.993137 liq=2772.2826 tmpl=1.00 eq=0.00 qual=0.81 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550695` (event `26313`) q='Will Netherlands qualify for the 2026 FIFA World Cup?' vol=7759.946623 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550696` (event `26313`) q='Will Belgium qualify for the 2026 FIFA World Cup?' vol=16165.628878 liq=None tmpl=1.00 eq=0.00 qual=0.48 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550697` (event `26313`) q='Will Croatia qualify for the 2026 FIFA World Cup?' vol=6400.949231 liq=None tmpl=1.00 eq=0.00 qual=0.44 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550698` (event `26313`) q='Will Colombia qualify for the 2026 FIFA World Cup?' vol=13673.922584 liq=0.0 tmpl=1.00 eq=0.00 qual=0.47 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550699` (event `26313`) q='Will Uruguay qualify for the 2026 FIFA World Cup?' vol=9211.867177 liq=0.0 tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550700` (event `26313`) q='Will Saudi Arabia qualify for the 2026 FIFA World Cup?' vol=10048.89281 liq=None tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550701` (event `26313`) q='Will Australia qualify for the 2026 FIFA World Cup?' vol=67.9616 liq=None tmpl=1.00 eq=0.00 qual=0.27 rej=True reject=['reject:sports_market'] keep=[]
- `550702` (event `26313`) q='Will Oman qualify for the 2026 FIFA World Cup?' vol=7789.699868 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550703` (event `26313`) q='Will Sweden qualify for the 2026 FIFA World Cup?' vol=100609.824439 liq=4589.9977 tmpl=1.00 eq=0.00 qual=0.80 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550704` (event `26313`) q='Will United Arab Emirates qualify for the 2026 FIFA World Cup?' vol=4269.077475 liq=None tmpl=1.00 eq=0.00 qual=0.43 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550705` (event `26313`) q='Will Austria qualify for the 2026 FIFA World Cup?' vol=1754.384306 liq=0.0 tmpl=1.00 eq=0.00 qual=0.39 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']

### reject:winner_template

- `553824` (event `27829`) q='Will the Carolina Hurricanes win the 2026 NHL Stanley Cup?' vol=133160.936316 liq=101157.0378 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553825` (event `27829`) q='Will the Florida Panthers win the 2026 NHL Stanley Cup?' vol=634892.151628 liq=75319.32895 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553826` (event `27829`) q='Will the Edmonton Oilers win the 2026 NHL Stanley Cup?' vol=291712.33579 liq=44582.3742 tmpl=1.00 eq=0.00 qual=0.91 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553827` (event `27829`) q='Will the Dallas Stars win the 2026 NHL Stanley Cup?' vol=355252.271492 liq=73922.90341 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553828` (event `27829`) q='Will the Colorado Avalanche win the 2026 NHL Stanley Cup?' vol=7066408.703418 liq=104649.25375 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553829` (event `27829`) q='Will the Vegas Golden Knights win the 2026 NHL Stanley Cup?' vol=652016.57753 liq=107896.15691 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553830` (event `27829`) q='Will the Tampa Bay Lightning win the 2026 NHL Stanley Cup?' vol=173725.835431 liq=71941.93036 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553831` (event `27829`) q='Will the Los Angeles Kings win the 2026 NHL Stanley Cup?' vol=6136208.624221 liq=102721.5928 tmpl=1.00 eq=0.00 qual=0.99 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553832` (event `27829`) q='Will the New Jersey Devils win the 2026 NHL Stanley Cup?' vol=322434.465595 liq=86374.94695 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553833` (event `27829`) q='Will the Winnipeg Jets win the 2026 NHL Stanley Cup?' vol=319508.072194 liq=120084.88584 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553834` (event `27829`) q='Will the Toronto Maple Leafs win the 2026 NHL Stanley Cup?' vol=575787.400151 liq=99004.03793 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553835` (event `27829`) q='Will the Washington Capitals win the 2026 NHL Stanley Cup?' vol=293507.782376 liq=93268.85507 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `540817` (event `23784`) q='New Rihanna Album before GTA VI?' vol=641705.393532 liq=27423.1518 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `540818` (event `23784`) q='New Playboi Carti Album before GTA VI?' vol=677002.176258 liq=19451.4348 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613835` (event `50251`) q='Will One Battle After Another win Best Picture at the 98th Academy Awards?' vol=1428120.253022 liq=39135.6741 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613836` (event `50251`) q='Will Hamnet win Best Picture at the 98th Academy Awards?' vol=1755949.586891 liq=57647.57441 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613837` (event `50251`) q='Will Sinners win Best Picture at the 98th Academy Awards?' vol=1207884.339433 liq=48916.99105 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613838` (event `50251`) q='Will Sentimental Value win Best Picture at the 98th Academy Awards?' vol=1054541.204511 liq=113876.6633 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613839` (event `50251`) q='Will Marty Supreme win Best Picture at the 98th Academy Awards?' vol=1831654.311816 liq=44869.71789 tmpl=0.60 eq=0.00 qual=0.96 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613840` (event `50251`) q='Will Wicked: For Good win Best Picture at the 98th Academy Awards?' vol=655563.816875 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613841` (event `50251`) q='Will Bugonia win Best Picture at the 98th Academy Awards?' vol=1373512.381699 liq=128893.13929 tmpl=0.60 eq=0.00 qual=0.99 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613842` (event `50251`) q='Will It Was Just an Accident win Best Picture at the 98th Academy Awards?' vol=767105.915249 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613843` (event `50251`) q='Will Jay Kelly win Best Picture at the 98th Academy Awards?' vol=928426.551636 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613844` (event `50251`) q='Will A House of Dynamite win Best Picture at the 98th Academy Awards?' vol=1056888.310835 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']

### reject:price_target_template

- `665324` (event `73105`) q='Will Trump sell over 100k Gold Cards in 2026?' vol=5582.894803 liq=7780.24721 tmpl=0.70 eq=0.00 qual=0.70 rej=True reject=['reject:price_target_template'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `701486` (event `89502`) q='Will Bitcoin reach $200,000 by December 31, 2026?' vol=658933.490041 liq=54295.0325 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701487` (event `89502`) q='Will Bitcoin reach $190,000 by December 31, 2026?' vol=340349.644774 liq=40689.9066 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701488` (event `89502`) q='Will Bitcoin reach $180,000 by December 31, 2026?' vol=316498.700481 liq=35327.726 tmpl=0.70 eq=0.00 qual=0.90 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701489` (event `89502`) q='Will Bitcoin reach $170,000 by December 31, 2026?' vol=196654.862964 liq=29527.473 tmpl=0.70 eq=0.00 qual=0.88 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701490` (event `89502`) q='Will Bitcoin reach $160,000 by December 31, 2026?' vol=300266.499779 liq=50404.8204 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701491` (event `89502`) q='Will Bitcoin reach $150,000 by December 31, 2026?' vol=612548.174239 liq=45266.1301 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701492` (event `89502`) q='Will Bitcoin reach $140,000 by December 31, 2026?' vol=558301.558072 liq=59196.9724 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701493` (event `89502`) q='Will Bitcoin reach $130,000 by December 31, 2026?' vol=559777.255683 liq=58758.5512 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701494` (event `89502`) q='Will Bitcoin reach $120,000 by December 31, 2026?' vol=424668.417874 liq=34214.4756 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701495` (event `89502`) q='Will Bitcoin reach $110,000 by December 31, 2026?' vol=476567.543899 liq=34160.1481 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701496` (event `89502`) q='Will Bitcoin reach $100,000 by December 31, 2026?' vol=832525.561575 liq=98660.4342 tmpl=0.70 eq=0.00 qual=0.97 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:meme_trivia

- `1255799` (event `184873`) q='Will Elon Musk post 0-19 tweets in March 2026?' vol=113238.92932 liq=26261.10918 tmpl=0.60 eq=0.00 qual=0.85 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255801` (event `184873`) q='Will Elon Musk post 20-39 tweets in March 2026?' vol=44001.832625 liq=22946.78431 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255803` (event `184873`) q='Will Elon Musk post 40-59 tweets in March 2026?' vol=68943.039552 liq=24570.94393 tmpl=0.60 eq=0.00 qual=0.83 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255805` (event `184873`) q='Will Elon Musk post 60-79 tweets in March 2026?' vol=47825.973416 liq=20966.38754 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255808` (event `184873`) q='Will Elon Musk post 80-99 tweets in March 2026?' vol=53657.029166 liq=21388.88048 tmpl=0.60 eq=0.00 qual=0.82 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255810` (event `184873`) q='Will Elon Musk post 100-119 tweets in March 2026?' vol=32116.913332 liq=27109.07619 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255812` (event `184873`) q='Will Elon Musk post 120-139 tweets in March 2026?' vol=38761.8515 liq=25002.66051 tmpl=0.60 eq=0.00 qual=0.81 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255814` (event `184873`) q='Will Elon Musk post 140-159 tweets in March 2026?' vol=29313.948166 liq=24282.56107 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255816` (event `184873`) q='Will Elon Musk post 160-179 tweets in March 2026?' vol=27017.936499 liq=23166.61907 tmpl=0.60 eq=0.00 qual=0.79 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255819` (event `184873`) q='Will Elon Musk post 180-199 tweets in March 2026?' vol=29707.407904 liq=25603.84841 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255821` (event `184873`) q='Will Elon Musk post 200-219 tweets in March 2026?' vol=31738.447999 liq=20131.80844 tmpl=0.60 eq=0.00 qual=0.80 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']
- `1255824` (event `184873`) q='Will Elon Musk post 220-239 tweets in March 2026?' vol=21340.686415 liq=16223.30042 tmpl=0.60 eq=0.00 qual=0.77 rej=True reject=['reject:meme_trivia'] keep=['quality:volume_high', 'quality:liquidity_high']

### reject:political_leader_template

- `562793` (event `32224`) q='Will the Democratic Party control the Senate after the 2026 Midterm elections?' vol=239085.34867 liq=110827.7638 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562794` (event `32224`) q='Will the Republican Party control the Senate after the 2026 Midterm elections?' vol=361803.019471 liq=85560.1237 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562795` (event `32224`) q='Will Party A control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562796` (event `32224`) q='Will Party B control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562797` (event `32224`) q='Will Party C control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562798` (event `32224`) q='Will Party D control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562799` (event `32224`) q='Will Party E control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562800` (event `32224`) q='Will Party F control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562801` (event `32224`) q='Will another party control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562802` (event `32225`) q='Will the Democratic Party control the House after the 2026 Midterm elections?' vol=1799175.659025 liq=183233.7632 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562803` (event `32225`) q='Will the Republican Party control the House after the 2026 Midterm elections?' vol=1687598.051507 liq=185782.001 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562804` (event `32225`) q='Will Party A control the House after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.01 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:ended_penalty']

### reject:appstore_charts

- `1402598` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 22?' vol=35098.372531 liq=None tmpl=0.80 eq=0.00 qual=0.43 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402599` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 24?' vol=15056.440058 liq=None tmpl=0.80 eq=0.00 qual=0.39 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402600` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 26?' vol=16396.910339 liq=None tmpl=0.80 eq=0.00 qual=0.40 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:ended_penalty']
- `1402601` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by February 28?' vol=15478.578043 liq=1445.78569 tmpl=0.80 eq=0.00 qual=0.61 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_high', 'quality:liquidity_mid', 'quality:ended_penalty']
- `1449762` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by March 15?' vol=2343.036264 liq=14181.48123 tmpl=0.80 eq=0.00 qual=0.60 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_high', 'quality:ended_penalty']
- `1449763` (event `219309`) q='Will ChatGPT be out as the #1 Free App in the US Apple Store by March 31?' vol=340.456874 liq=1562.67815 tmpl=0.80 eq=0.00 qual=0.46 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid', 'quality:ended_penalty']
- `1455928` (event `234983`) q='Will Shadowrocket be #1 Paid App in the US Apple App Store on March 6?' vol=1163.762951 liq=1198.5823 tmpl=0.80 eq=0.00 qual=0.58 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1455929` (event `234983`) q='Will HotSchedules be #1 Paid App in the US Apple App Store on March 6?' vol=453.220254 liq=847.3044 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=[]
- `1455930` (event `234983`) q='Will SkyView be #1 Paid App in the US Apple App Store on March 6?' vol=479.4821 liq=1522.41765 tmpl=0.80 eq=0.00 qual=0.56 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1455931` (event `234983`) q='Will Procreate Pocket be #1 Paid App in the US Apple App Store on March 6?' vol=481.02525 liq=869.89688 tmpl=0.80 eq=0.00 qual=0.54 rej=True reject=['reject:appstore_charts'] keep=[]
- `1455932` (event `234983`) q='Will AnkiMobile Flashcards be #1 Paid App in the US Apple App Store on March 6?' vol=922.655791 liq=1417.14249 tmpl=0.80 eq=0.00 qual=0.58 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1455933` (event `234983`) q='Will Paprika Recipe Manager 3 be #1 Paid App in the US Apple App Store on March 6?' vol=632.86875 liq=1114.81099 tmpl=0.80 eq=0.00 qual=0.56 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']

### reject:religion_prophecy

- `540819` (event `23784`) q='Will Jesus Christ return before GTA VI?' vol=9597346.096994 liq=828993.2701 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']
- `703258` (event `90178`) q='Will Jesus Christ return before 2027?' vol=35531171.697761 liq=2884241.74632 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']

## Kept high relevance (examples)

- `1403678` (event `219797`) q='Trump sued over tariff powers again by March 31?' vol=54097.003691 liq=17167.58925 tmpl=0.00 eq=1.00 qual=0.81 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:macro', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_high']
- `665729` (event `73332`) q='US congress stock trading ban before 2027?' vol=14742.444924 liq=3045.739 tmpl=0.00 eq=0.80 qual=0.71 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693776` (event `86397`) q='Will Aristotle self-certify sports event contracts by March 31, 2026?' vol=29278.977499 liq=2619.6433 tmpl=0.00 eq=0.80 qual=0.73 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693777` (event `86397`) q='Will Railbird self-certify sports event contracts by March 31, 2026?' vol=42133.039038 liq=1427.7629 tmpl=0.00 eq=0.80 qual=0.73 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693778` (event `86397`) q='Will ForecastEx self-certify sports event contracts by March 31, 2026?' vol=32786.028642 liq=996.83 tmpl=0.00 eq=0.80 qual=0.71 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693779` (event `86397`) q='Will the Chicago Mercantile Exchange self-certify sports event contracts by March 31, 2026?' vol=None liq=None tmpl=0.00 eq=0.80 qual=0.10 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `693780` (event `86397`) q='Will Cboe Futures Exchange self-certify sports event contracts by March 31, 2026?' vol=9225.0 liq=81.0196 tmpl=0.00 eq=0.80 qual=0.59 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `693781` (event `86397`) q='Will Intercontinental Exchange self-certify sports event contracts by March 31, 2026?' vol=23491.180908 liq=118.1372 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693782` (event `86397`) q='Will the Small Exchange self-certify sports event contracts by March 31, 2026?' vol=26705.184914 liq=101.7212 tmpl=0.00 eq=0.80 qual=0.64 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693783` (event `86397`) q='Will LedgerX self-certify sports event contracts by March 31, 2026?' vol=2.0 liq=74.0071 tmpl=0.00 eq=0.80 qual=0.27 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `701299` (event `86397`) q='Will The Clearing Company self-certify sports event contracts by March 31, 2026?' vol=520.048671 liq=76.303 tmpl=0.00 eq=0.80 qual=0.47 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1198966` (event `168384`) q='Von der Leyen out as European Commission President in 2026?' vol=10569.045687 liq=6363.9279 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `1199759` (event `168607`) q='Will Marine Le Pen win her appeal to lift ineligibility ban in 2026?' vol=4963.522737 liq=3653.4877 tmpl=0.00 eq=0.80 qual=0.67 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1228017` (event `176964`) q='SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?' vol=1244.150963 liq=63.97305 tmpl=0.00 eq=0.80 qual=0.50 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `1236477` (event `179563`) q='Will Trump act to ban mail-in voting or voting machines by June 30?' vol=1899.214109 liq=5765.1001 tmpl=0.00 eq=0.80 qual=0.65 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1243055` (event `181500`) q='Jack Smith charged by March 31?' vol=879.509461 liq=105.2638 tmpl=0.00 eq=0.80 qual=0.50 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1327734` (event `197715`) q='Will CA Banfield win on 2026-03-02?' vol=None liq=69718.7947 tmpl=0.00 eq=0.80 qual=0.43 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1327736` (event `197715`) q='Will CA Aldosivi win on 2026-03-02?' vol=None liq=70604.7333 tmpl=0.00 eq=0.80 qual=0.43 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1352764` (event `201497`) q='Will CA Barracas Central win on 2026-03-06?' vol=None liq=107.7734 tmpl=0.00 eq=0.80 qual=0.24 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1352768` (event `201497`) q='Will CA Banfield win on 2026-03-06?' vol=None liq=98.1899 tmpl=0.00 eq=0.80 qual=0.23 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']

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

- `572473` (event `35908`) vol=100965565.603344 liq=700796.71252 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Judy Shelton as the next Fed chair?'
- `654412` (event `67284`) vol=76967747.425662 liq=1494224.43879 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?'
- `654415` (event `67284`) vol=65651484.751596 liq=1807652.37986 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?'
- `1180303` (event `162818`) vol=57040222.662635 liq=471609.139 tmpl=0.0 eq=0.0 qual=0.915 reasons=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty'] q='Khamenei out as Supreme Leader of Iran by February 28?'
- `572469` (event `35908`) vol=44414627.462841 liq=200892.6919 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Warsh as the next Fed chair?'
- `572481` (event `35908`) vol=38542322.771053 liq=1364396.67065 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Scott Bessent as the next Fed chair?'
- `916732` (event `102773`) vol=36568139.265626 liq=502794.34848 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Khamenei out as Supreme Leader of Iran by March 31?'
- `572470` (event `35908`) vol=31960569.507863 liq=709855.3806 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Hassett as the next Fed chair?'
- `572485` (event `35908`) vol=29174804.788901 liq=739173.66157 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Rick Rieder as the next Fed chair?'
- `997488` (event `118172`) vol=28825759.97237 liq=311215.94296 tmpl=0.0 eq=0.7 qual=1.0 reasons=['relevance:corporate_actions', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump acquire Greenland before 2027?'
- `572478` (event `35908`) vol=27798141.69542 liq=571604.39806 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Jerome Powell as the next Fed chair?'
- `572471` (event `35908`) vol=24979801.464497 liq=258481.86732 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Christopher Waller as the next Fed chair?'
- `1105754` (event `143443`) vol=24692949.117163 liq=134257.50178 tmpl=0.0 eq=0.0 qual=0.994386068201472 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Richard Grenell be the leader of Venezuela end of 2026?'
- `572472` (event `35908`) vol=24500475.328131 liq=2340783.56551 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Bill Pulte as the next Fed chair?'
- `1105752` (event `143443`) vol=23950318.135341 liq=104123.42074 tmpl=0.0 eq=0.0 qual=0.986972469643029 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Frank Donovan be the leader of Venezuela end of 2026?'
- `572494` (event `35908`) vol=23508646.036 liq=2997993.09996 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate himself as the next Fed chair?'
- `654413` (event `67284`) vol=23440296.814054 liq=530761.9246 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?'
- `654414` (event `67284`) vol=23269783.959722 liq=379173.61425 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will there be no change in Fed interest rates after the March 2026 meeting?'
- `572486` (event `35908`) vol=23188103.781262 liq=246127.10401 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Michelle Bowman as the next Fed chair?'
- `572489` (event `35908`) vol=21311692.069942 liq=3016286.86578 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Janet Yellen as the next Fed chair?'
- `572476` (event `35908`) vol=21108894.068664 liq=3199860.19411 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Arthur Laffer as the next Fed chair?'
- `572492` (event `35908`) vol=20879940.96291 liq=3303002.94776 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Barron Trump as the next Fed chair?'
- `572480` (event `35908`) vol=20741151.355347 liq=302915.88044 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Stephen Miran as the next Fed chair?'
- `561829` (event `31759`) vol=20710600.992214 liq=305354.34041 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Russia x Ukraine ceasefire by March 31, 2026?'
- `572506` (event `35908`) vol=20509531.279025 liq=170042.81054 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate no one before 2027?'
- `516926` (event `16167`) vol=17976157.529867 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='MicroStrategy sells any Bitcoin in 2025?'
- `572484` (event `35908`) vol=17908344.56491 liq=2870684.7206 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate David Zervos as the next Fed chair?'
- `572479` (event `35908`) vol=12626617.884833 liq=3052426.4899 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Ron Paul as the next Fed chair?'
- `703257` (event `90177`) vol=11915610.837206 liq=1164824.7972 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will the US confirm that aliens exist before 2027?'
- `572488` (event `35908`) vol=10797098.951725 liq=2896113.58781 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Philip Jefferson as the next Fed chair?'

## Top rejected by volume_usd

- `553861` (event `27830`) vol=47827627.59217 liq=385537.22786 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Indiana Pacers win the 2026 NBA Finals?'
- `559684` (event `30829`) vol=40299577.460736 liq=337905.48439 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Chelsea Clinton win the 2028 Democratic presidential nomination?'
- `566203` (event `33507`) vol=38357203.212948 liq=2039852.53212 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Leeds win the 2025–26 English Premier League?'
- `559687` (event `30829`) vol=36078660.46328 liq=1674451.71513 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Oprah Winfrey win the 2028 Democratic presidential nomination?'
- `703258` (event `90178`) vol=35531171.697761 liq=2884241.74632 tmpl=0.9 eq=0.0 qual=1.0 reasons=['reject:religion_prophecy'] q='Will Jesus Christ return before 2027?'
- `561247` (event `31552`) vol=32701612.91196 liq=1108193.15647 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 US Presidential Election?'
- `559688` (event `30829`) vol=32535693.035289 liq=1393867.69595 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Andrew Yang win the 2028 Democratic presidential nomination?'
- `559683` (event `30829`) vol=32227440.404093 liq=550001.96306 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will George Clooney win the 2028 Democratic presidential nomination?'
- `561251` (event `31552`) vol=32096319.016274 liq=460363.63165 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 US Presidential Election?'
- `553874` (event `27830`) vol=32070952.801182 liq=988332.18419 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Memphis Grizzlies win the 2026 NBA Finals?'
- `559677` (event `30829`) vol=31293336.663112 liq=1001126.43597 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hillary Clinton win the 2028 Democratic presidential nomination?'
- `559685` (event `30829`) vol=30679797.696261 liq=1759547.09449 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will MrBeast win the 2028 Democratic presidential nomination?'
- `566192` (event `33507`) vol=30341659.247611 liq=1592807.68055 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Tottenham win the 2025–26 English Premier League?'
- `559679` (event `30829`) vol=30219308.751442 liq=1426264.95033 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Bernie Sanders win the 2028 Democratic presidential nomination?'
- `559671` (event `30829`) vol=30212566.999641 liq=1494582.60846 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Zohran Mamdani win the 2028 Democratic presidential nomination?'
- `559681` (event `30829`) vol=28971167.320535 liq=1703941.40164 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 Democratic presidential nomination?'
- `1303355` (event `194107`) vol=28661522.82917 liq=3121157.68353 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:price_target_template'] q='Will Bitcoin reach $150,000 in February?'
- `566174` (event `33506`) vol=28392439.058395 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Slavia Pragu win the 2025–26 Champions League?'
- `561249` (event `31552`) vol=28213012.231976 liq=385476.765 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Greg Abbott win the 2028 US Presidential Election?'
- `559680` (event `30829`) vol=27803792.129287 liq=1596620.41826 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Phil Murphy win the 2028 Democratic presidential nomination?'
- `559678` (event `30829`) vol=27402692.601271 liq=1157233.56158 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Liz Cheney win the 2028 Democratic presidential nomination?'
- `559666` (event `30829`) vol=26948253.94878 liq=1603540.87582 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 Democratic presidential nomination?'
- `559682` (event `30829`) vol=25542048.395033 liq=1492630.60695 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hunter Biden win the 2028 Democratic presidential nomination?'
- `561995` (event `31875`) vol=25480969.653327 liq=835529.59044 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Mike Pence win the 2028 Republican presidential nomination?'
- `561242` (event `31552`) vol=24550642.605377 liq=454108.57677 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tulsi Gabbard win the 2028 US Presidential Election?'
- `1423580` (event `226986`) vol=23830003.14533 liq=22335.91513 tmpl=0.6 eq=0.0 qual=0.942074882627526 reasons=['reject:meme_trivia'] q='Will Elon Musk post 0-19 tweets from February 27 to March 6, 2026?'
- `559690` (event `30829`) vol=23803469.545216 liq=1842722.5821 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Kim Kardashian win the 2028 Democratic presidential nomination?'
- `559670` (event `30829`) vol=23271080.518767 liq=787620.71844 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Gina Raimondo win the 2028 Democratic presidential nomination?'
- `559689` (event `30829`) vol=23126357.82928 liq=829051.2753 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Beto O’Rourke win the 2028 Democratic presidential nomination?'
- `561248` (event `31552`) vol=22339841.346761 liq=406728.90256 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Vivek Ramaswamy win the 2028 US Presidential Election?'
