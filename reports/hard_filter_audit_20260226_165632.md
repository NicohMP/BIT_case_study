# Hard Filter Audit

## Run metadata

- decided_at_utc: `2026-02-26T16:56:32.546961+00:00`
- filter_version: `hard_filters_v8`
- config_sha256: `6bc7e216020a44917efaabb0fb3155a93019597f530dabb18c0dfe6bf9f470e4`
- evaluated: `58391`
- rejected: `46879` (80.3%)

## Top rejection reasons

- `reject:sports_market`: 26417
- `reject:winner_template`: 13091
- `reject:micro_price_bets`: 5011
- `reject:entertainment_gossip`: 1654
- `reject:price_target_template`: 1385
- `reject:meme_trivia`: 759
- `reject:political_leader_template`: 353
- `reject:appstore_charts`: 63
- `reject:religion_prophecy`: 2

## Samples by rejection reason

### reject:sports_market

- `550694` (event `26313`) q='Will Italy qualify for the 2026 FIFA World Cup?' vol=206162.678529 liq=2972.4008 tmpl=1.00 eq=0.00 qual=0.81 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550695` (event `26313`) q='Will Netherlands qualify for the 2026 FIFA World Cup?' vol=7759.946623 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550696` (event `26313`) q='Will Belgium qualify for the 2026 FIFA World Cup?' vol=16165.628878 liq=None tmpl=1.00 eq=0.00 qual=0.48 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550697` (event `26313`) q='Will Croatia qualify for the 2026 FIFA World Cup?' vol=6400.949231 liq=None tmpl=1.00 eq=0.00 qual=0.44 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550698` (event `26313`) q='Will Colombia qualify for the 2026 FIFA World Cup?' vol=13673.922584 liq=0.0 tmpl=1.00 eq=0.00 qual=0.47 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550699` (event `26313`) q='Will Uruguay qualify for the 2026 FIFA World Cup?' vol=9211.867177 liq=0.0 tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550700` (event `26313`) q='Will Saudi Arabia qualify for the 2026 FIFA World Cup?' vol=10048.89281 liq=None tmpl=1.00 eq=0.00 qual=0.46 rej=True reject=['reject:sports_market'] keep=['quality:volume_high']
- `550701` (event `26313`) q='Will Australia qualify for the 2026 FIFA World Cup?' vol=67.9616 liq=None tmpl=1.00 eq=0.00 qual=0.27 rej=True reject=['reject:sports_market'] keep=[]
- `550702` (event `26313`) q='Will Oman qualify for the 2026 FIFA World Cup?' vol=7789.699868 liq=None tmpl=1.00 eq=0.00 qual=0.45 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550703` (event `26313`) q='Will Sweden qualify for the 2026 FIFA World Cup?' vol=99003.074518 liq=5629.0141 tmpl=1.00 eq=0.00 qual=0.80 rej=True reject=['reject:sports_market'] keep=['quality:volume_high', 'quality:liquidity_mid']
- `550704` (event `26313`) q='Will United Arab Emirates qualify for the 2026 FIFA World Cup?' vol=4269.077475 liq=None tmpl=1.00 eq=0.00 qual=0.43 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']
- `550705` (event `26313`) q='Will Austria qualify for the 2026 FIFA World Cup?' vol=1754.384306 liq=0.0 tmpl=1.00 eq=0.00 qual=0.39 rej=True reject=['reject:sports_market'] keep=['quality:volume_mid']

### reject:winner_template

- `553824` (event `27829`) q='Will the Carolina Hurricanes win the 2026 NHL Stanley Cup?' vol=126161.935709 liq=90498.0467 tmpl=1.00 eq=0.00 qual=0.89 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553825` (event `27829`) q='Will the Florida Panthers win the 2026 NHL Stanley Cup?' vol=624373.703352 liq=70621.39649 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553826` (event `27829`) q='Will the Edmonton Oilers win the 2026 NHL Stanley Cup?' vol=284076.416241 liq=46183.0125 tmpl=1.00 eq=0.00 qual=0.91 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553827` (event `27829`) q='Will the Dallas Stars win the 2026 NHL Stanley Cup?' vol=326050.473418 liq=77916.3873 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553828` (event `27829`) q='Will the Colorado Avalanche win the 2026 NHL Stanley Cup?' vol=6526512.719104 liq=90121.73815 tmpl=1.00 eq=0.00 qual=0.98 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553829` (event `27829`) q='Will the Vegas Golden Knights win the 2026 NHL Stanley Cup?' vol=641382.009677 liq=96386.01678 tmpl=1.00 eq=0.00 qual=0.96 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553830` (event `27829`) q='Will the Tampa Bay Lightning win the 2026 NHL Stanley Cup?' vol=166580.278472 liq=68614.31027 tmpl=1.00 eq=0.00 qual=0.90 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553831` (event `27829`) q='Will the Los Angeles Kings win the 2026 NHL Stanley Cup?' vol=6127141.801104 liq=92302.72903 tmpl=1.00 eq=0.00 qual=0.98 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553832` (event `27829`) q='Will the New Jersey Devils win the 2026 NHL Stanley Cup?' vol=317376.285595 liq=80213.67607 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553833` (event `27829`) q='Will the Winnipeg Jets win the 2026 NHL Stanley Cup?' vol=306034.107435 liq=123455.28703 tmpl=1.00 eq=0.00 qual=0.94 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553834` (event `27829`) q='Will the Toronto Maple Leafs win the 2026 NHL Stanley Cup?' vol=569853.377984 liq=90395.2033 tmpl=1.00 eq=0.00 qual=0.95 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `553835` (event `27829`) q='Will the Washington Capitals win the 2026 NHL Stanley Cup?' vol=290230.139484 liq=86349.21607 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:sports_market', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `540817` (event `23784`) q='New Rihanna Album before GTA VI?' vol=640741.94453 liq=65935.9932 tmpl=0.60 eq=0.00 qual=0.95 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `540818` (event `23784`) q='New Playboi Carti Album before GTA VI?' vol=676316.158261 liq=22474.8363 tmpl=0.60 eq=0.00 qual=0.92 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613835` (event `50251`) q='Will One Battle After Another win Best Picture at the 98th Academy Awards?' vol=1353387.338258 liq=111106.0271 tmpl=0.60 eq=0.00 qual=0.99 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613836` (event `50251`) q='Will Hamnet win Best Picture at the 98th Academy Awards?' vol=1686833.69373 liq=74879.48439 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613837` (event `50251`) q='Will Sinners win Best Picture at the 98th Academy Awards?' vol=1173929.351784 liq=55730.51552 tmpl=0.60 eq=0.00 qual=0.97 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613838` (event `50251`) q='Will Sentimental Value win Best Picture at the 98th Academy Awards?' vol=995227.914939 liq=102500.91577 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613839` (event `50251`) q='Will Marty Supreme win Best Picture at the 98th Academy Awards?' vol=1730182.493418 liq=69564.63682 tmpl=0.60 eq=0.00 qual=0.98 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613840` (event `50251`) q='Will Wicked: For Good win Best Picture at the 98th Academy Awards?' vol=655563.816875 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613841` (event `50251`) q='Will Bugonia win Best Picture at the 98th Academy Awards?' vol=1229490.804944 liq=104448.70357 tmpl=0.60 eq=0.00 qual=0.99 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high', 'quality:liquidity_high']
- `613842` (event `50251`) q='Will It Was Just an Accident win Best Picture at the 98th Academy Awards?' vol=767105.915249 liq=None tmpl=0.60 eq=0.00 qual=0.63 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613843` (event `50251`) q='Will Jay Kelly win Best Picture at the 98th Academy Awards?' vol=928426.551636 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']
- `613844` (event `50251`) q='Will A House of Dynamite win Best Picture at the 98th Academy Awards?' vol=1056888.310835 liq=None tmpl=0.60 eq=0.00 qual=0.64 rej=True reject=['reject:entertainment_gossip'] keep=['quality:volume_high']

### reject:price_target_template

- `665324` (event `73105`) q='Will Trump sell over 100k Gold Cards in 2026?' vol=5534.323376 liq=8496.33665 tmpl=0.70 eq=0.00 qual=0.70 rej=True reject=['reject:price_target_template'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `701486` (event `89502`) q='Will Bitcoin reach $200,000 by December 31, 2026?' vol=649810.512359 liq=54311.9917 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701487` (event `89502`) q='Will Bitcoin reach $190,000 by December 31, 2026?' vol=334064.562877 liq=43684.9999 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701488` (event `89502`) q='Will Bitcoin reach $180,000 by December 31, 2026?' vol=312547.876199 liq=46509.9429 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701489` (event `89502`) q='Will Bitcoin reach $170,000 by December 31, 2026?' vol=194414.737251 liq=29611.9653 tmpl=0.70 eq=0.00 qual=0.88 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701490` (event `89502`) q='Will Bitcoin reach $160,000 by December 31, 2026?' vol=298466.019779 liq=54331.2991 tmpl=0.70 eq=0.00 qual=0.91 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701491` (event `89502`) q='Will Bitcoin reach $150,000 by December 31, 2026?' vol=599686.186234 liq=55447.6506 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701492` (event `89502`) q='Will Bitcoin reach $140,000 by December 31, 2026?' vol=551624.917114 liq=64784.6364 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701493` (event `89502`) q='Will Bitcoin reach $130,000 by December 31, 2026?' vol=545703.329592 liq=67150.9841 tmpl=0.70 eq=0.00 qual=0.94 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701494` (event `89502`) q='Will Bitcoin reach $120,000 by December 31, 2026?' vol=419981.621805 liq=42268.8541 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701495` (event `89502`) q='Will Bitcoin reach $110,000 by December 31, 2026?' vol=471453.632913 liq=35640.7901 tmpl=0.70 eq=0.00 qual=0.92 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `701496` (event `89502`) q='Will Bitcoin reach $100,000 by December 31, 2026?' vol=811396.193354 liq=128740.7343 tmpl=0.70 eq=0.00 qual=0.98 rej=True reject=['reject:price_target_template'] keep=['quality:volume_high', 'quality:liquidity_high']

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

- `562793` (event `32224`) q='Will the Democratic Party control the Senate after the 2026 Midterm elections?' vol=237142.957452 liq=113505.4649 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562794` (event `32224`) q='Will the Republican Party control the Senate after the 2026 Midterm elections?' vol=358767.31281 liq=88656.0499 tmpl=1.00 eq=0.00 qual=0.93 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562795` (event `32224`) q='Will Party A control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562796` (event `32224`) q='Will Party B control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562797` (event `32224`) q='Will Party C control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562798` (event `32224`) q='Will Party D control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562799` (event `32224`) q='Will Party E control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562800` (event `32224`) q='Will Party F control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562801` (event `32224`) q='Will another party control the Senate after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.10 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=[]
- `562802` (event `32225`) q='Will the Democratic Party control the House after the 2026 Midterm elections?' vol=1746772.171337 liq=229126.3792 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562803` (event `32225`) q='Will the Republican Party control the House after the 2026 Midterm elections?' vol=1633253.117063 liq=224835.4887 tmpl=1.00 eq=0.00 qual=1.00 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:volume_high', 'quality:liquidity_high']
- `562804` (event `32225`) q='Will Party A control the House after the 2026 Midterm elections?' vol=0.0 liq=0.0 tmpl=1.00 eq=0.00 qual=0.01 rej=True reject=['reject:political_leader_template', 'reject:winner_template'] keep=['quality:ended_penalty']

### reject:appstore_charts

- `1402465` (event `219250`) q='Will Shadowrocket be #1 Paid App in the US Apple App Store on February 27?' vol=6138.7775 liq=1413.6506 tmpl=0.80 eq=0.00 qual=0.65 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402466` (event `219250`) q='Will HotSchedules be #1 Paid App in the US Apple App Store on February 27?' vol=3619.645543 liq=1485.7091 tmpl=0.80 eq=0.00 qual=0.63 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402467` (event `219250`) q='Will SkyView be #1 Paid App in the US Apple App Store on February 27?' vol=5375.911505 liq=1966.01108 tmpl=0.80 eq=0.00 qual=0.66 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402468` (event `219250`) q='Will Procreate Pocket be #1 Paid App in the US Apple App Store on February 27?' vol=1366.2491 liq=1309.01445 tmpl=0.80 eq=0.00 qual=0.59 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402469` (event `219250`) q='Will AnkiMobile Flashcards be #1 Paid App in the US Apple App Store on February 27?' vol=1096.9925 liq=1856.13216 tmpl=0.80 eq=0.00 qual=0.59 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402470` (event `219250`) q='Will TeamSpeak 3 be #1 Paid App in the US Apple App Store on February 27?' vol=212.616845 liq=1620.76651 tmpl=0.80 eq=0.00 qual=0.53 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1402471` (event `219250`) q='Will TonalEnergy Tuner & Metronome be #1 Paid App in the US Apple App Store on February 27?' vol=896.538 liq=2077.17446 tmpl=0.80 eq=0.00 qual=0.59 rej=True reject=['reject:appstore_charts'] keep=['quality:liquidity_mid']
- `1402472` (event `219250`) q='Will Current Reader be #1 Paid App in the US Apple App Store on February 27?' vol=1696.908 liq=2383.6085 tmpl=0.80 eq=0.00 qual=0.62 rej=True reject=['reject:appstore_charts'] keep=['quality:volume_mid', 'quality:liquidity_mid']
- `1402473` (event `219250`) q='Will App A be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.10 rej=True reject=['reject:appstore_charts'] keep=[]
- `1402474` (event `219250`) q='Will App B be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.10 rej=True reject=['reject:appstore_charts'] keep=[]
- `1402475` (event `219250`) q='Will App C be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.10 rej=True reject=['reject:appstore_charts'] keep=[]
- `1402476` (event `219250`) q='Will App D be #1 Paid App in the US Apple App Store on February 27?' vol=0.0 liq=0.0 tmpl=0.80 eq=0.00 qual=0.10 rej=True reject=['reject:appstore_charts'] keep=[]

### reject:religion_prophecy

- `540819` (event `23784`) q='Will Jesus Christ return before GTA VI?' vol=9545629.422815 liq=1682714.3602 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']
- `703258` (event `90178`) q='Will Jesus Christ return before 2027?' vol=33861270.850422 liq=4543329.24785 tmpl=0.90 eq=0.00 qual=1.00 rej=True reject=['reject:religion_prophecy'] keep=['quality:volume_high', 'quality:liquidity_high']

## Kept high relevance (examples)

- `1403678` (event `219797`) q='Trump sued over tariff powers again by March 31?' vol=39163.242728 liq=16379.27223 tmpl=0.00 eq=1.00 qual=0.80 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:macro', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_high']
- `665729` (event `73332`) q='US congress stock trading ban before 2027?' vol=14576.888027 liq=4029.4821 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693776` (event `86397`) q='Will Aristotle self-certify sports event contracts by March 31, 2026?' vol=22932.0 liq=145.3481 tmpl=0.00 eq=0.80 qual=0.64 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693777` (event `86397`) q='Will Railbird self-certify sports event contracts by March 31, 2026?' vol=39629.396809 liq=1885.0488 tmpl=0.00 eq=0.80 qual=0.74 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693778` (event `86397`) q='Will ForecastEx self-certify sports event contracts by March 31, 2026?' vol=26568.213168 liq=2342.9695 tmpl=0.00 eq=0.80 qual=0.73 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693779` (event `86397`) q='Will the Chicago Mercantile Exchange self-certify sports event contracts by March 31, 2026?' vol=None liq=None tmpl=0.00 eq=0.80 qual=0.10 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `693780` (event `86397`) q='Will Cboe Futures Exchange self-certify sports event contracts by March 31, 2026?' vol=9225.0 liq=74.53 tmpl=0.00 eq=0.80 qual=0.58 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `693781` (event `86397`) q='Will Intercontinental Exchange self-certify sports event contracts by March 31, 2026?' vol=23372.180908 liq=115.6182 tmpl=0.00 eq=0.80 qual=0.63 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high']
- `693782` (event `86397`) q='Will the Small Exchange self-certify sports event contracts by March 31, 2026?' vol=23569.8 liq=2352.5478 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `693783` (event `86397`) q='Will LedgerX self-certify sports event contracts by March 31, 2026?' vol=2.0 liq=122.3389 tmpl=0.00 eq=0.80 qual=0.28 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `701299` (event `86397`) q='Will The Clearing Company self-certify sports event contracts by March 31, 2026?' vol=512.546 liq=144.93242 tmpl=0.00 eq=0.80 qual=0.49 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1198966` (event `168384`) q='Von der Leyen out as European Commission President in 2026?' vol=10287.953741 liq=6962.071 tmpl=0.00 eq=0.80 qual=0.72 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_high', 'quality:liquidity_mid']
- `1199759` (event `168607`) q='Will Marine Le Pen win her appeal to lift ineligibility ban in 2026?' vol=4909.17138 liq=4458.5615 tmpl=0.00 eq=0.80 qual=0.68 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1228017` (event `176964`) q='SCOTUS lets Trump fire FTC commissioners in Trump v. Slaughter?' vol=1244.150963 liq=173.35515 tmpl=0.00 eq=0.80 qual=0.53 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid']
- `1236477` (event `179563`) q='Will Trump act to ban mail-in voting or voting machines by June 30?' vol=1851.410594 liq=3882.6792 tmpl=0.00 eq=0.80 qual=0.64 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_mid']
- `1243055` (event `181500`) q='Jack Smith charged by March 31?' vol=879.509461 liq=245.9248 tmpl=0.00 eq=0.80 qual=0.53 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']
- `1300240` (event `193766`) q='Will CA River Plate win on 2026-02-26?' vol=1744.343619 liq=27601.4826 tmpl=0.00 eq=0.80 qual=0.69 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:volume_mid', 'quality:liquidity_high']
- `1300242` (event `193766`) q='Will CA Banfield win on 2026-02-26?' vol=861.574593 liq=24466.4749 tmpl=0.00 eq=0.80 qual=0.66 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_high']
- `1327734` (event `197715`) q='Will CA Banfield win on 2026-03-02?' vol=None liq=1020.4447 tmpl=0.00 eq=0.80 qual=0.30 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal', 'quality:liquidity_mid']
- `1327736` (event `197715`) q='Will CA Aldosivi win on 2026-03-02?' vol=None liq=982.758 tmpl=0.00 eq=0.80 qual=0.30 rej=False reject=[] keep=['override:policy_or_macro_context', 'relevance:regulation_legal']

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

- `572473` (event `35908`) vol=96420304.477184 liq=1410750.27563 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Judy Shelton as the next Fed chair?'
- `654412` (event `67284`) vol=71890690.024027 liq=2082576.20185 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 50+ bps after the March 2026 meeting?'
- `654415` (event `67284`) vol=60710500.896238 liq=2207182.57071 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed increase interest rates by 25+ bps after the March 2026 meeting?'
- `1198423` (event `114242`) vol=47829399.485234 liq=722247.1323 tmpl=0.0 eq=0.0 qual=0.915 reasons=['quality:volume_high', 'quality:liquidity_high', 'quality:ended_penalty'] q='US strikes Iran by February 28, 2026?'
- `572469` (event `35908`) vol=43383548.836196 liq=355378.69658 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Warsh as the next Fed chair?'
- `1092199` (event `114242`) vol=41754060.055673 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by January 31, 2026?'
- `572481` (event `35908`) vol=37979521.661053 liq=1892971.62037 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Scott Bessent as the next Fed chair?'
- `572470` (event `35908`) vol=31120711.685667 liq=752878.61086 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Kevin Hassett as the next Fed chair?'
- `997488` (event `118172`) vol=28493983.740449 liq=582884.74057 tmpl=0.0 eq=0.7 qual=1.0 reasons=['relevance:corporate_actions', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump acquire Greenland before 2027?'
- `572485` (event `35908`) vol=28352404.884892 liq=1097873.1674 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Rick Rieder as the next Fed chair?'
- `572478` (event `35908`) vol=27743754.32542 liq=5246504.4398 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Jerome Powell as the next Fed chair?'
- `572472` (event `35908`) vol=24458475.328131 liq=2398254.56171 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Bill Pulte as the next Fed chair?'
- `572471` (event `35908`) vol=24330198.868945 liq=314102.35497 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Christopher Waller as the next Fed chair?'
- `1105752` (event `143443`) vol=23876389.911566 liq=95827.43866 tmpl=0.0 eq=0.0 qual=0.984550847586518 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Will Frank Donovan be the leader of Venezuela end of 2026?'
- `572494` (event `35908`) vol=23505646.036 liq=3062107.38084 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate himself as the next Fed chair?'
- `572486` (event `35908`) vol=22179842.32907 liq=298644.91394 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Michelle Bowman as the next Fed chair?'
- `572489` (event `35908`) vol=21309692.069942 liq=3010521.95931 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Janet Yellen as the next Fed chair?'
- `654413` (event `67284`) vol=21179082.297842 liq=1535201.6913 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will the Fed decrease interest rates by 25 bps after the March 2026 meeting?'
- `572476` (event `35908`) vol=21107894.068664 liq=3191728.49182 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Arthur Laffer as the next Fed chair?'
- `572492` (event `35908`) vol=20876940.96291 liq=3322673.89679 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Barron Trump as the next Fed chair?'
- `654414` (event `67284`) vol=20741806.939949 liq=995051.59764 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will there be no change in Fed interest rates after the March 2026 meeting?'
- `572480` (event `35908`) vol=20184631.011031 liq=428631.43766 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate Stephen Miran as the next Fed chair?'
- `572506` (event `35908`) vol=20016450.684349 liq=326486.92825 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate no one before 2027?'
- `561829` (event `31759`) vol=19932480.570843 liq=640181.89065 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='Russia x Ukraine ceasefire by March 31, 2026?'
- `1320793` (event `114242`) vol=18810054.309004 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 20, 2026?'
- `984441` (event `114242`) vol=18275410.253858 liq=425214.1295 tmpl=0.0 eq=0.0 qual=1.0 reasons=['quality:volume_high', 'quality:liquidity_high'] q='US strikes Iran by March 31, 2026?'
- `516926` (event `16167`) vol=17976157.529867 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='MicroStrategy sells any Bitcoin in 2025?'
- `572484` (event `35908`) vol=17904674.56491 liq=2851278.61139 tmpl=0.0 eq=0.6 qual=1.0 reasons=['override:policy_or_macro_context', 'relevance:macro', 'quality:volume_high', 'quality:liquidity_high'] q='Will Trump nominate David Zervos as the next Fed chair?'
- `1335520` (event `114242`) vol=17561112.38258 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 9, 2026?'
- `1386659` (event `114242`) vol=16942273.879883 liq=None tmpl=0.0 eq=0.0 qual=0.565 reasons=['quality:volume_high', 'quality:ended_penalty'] q='US strikes Iran by February 24, 2026?'

## Top rejected by volume_usd

- `553861` (event `27830`) vol=47604798.41217 liq=574712.45533 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Indiana Pacers win the 2026 NBA Finals?'
- `559684` (event `30829`) vol=40043626.321025 liq=522210.67354 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Chelsea Clinton win the 2028 Democratic presidential nomination?'
- `566203` (event `33507`) vol=38355176.992948 liq=1778293.83624 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Leeds win the 2025–26 English Premier League?'
- `559687` (event `30829`) vol=35799931.433907 liq=1869185.61365 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Oprah Winfrey win the 2028 Democratic presidential nomination?'
- `703258` (event `90178`) vol=33861270.850422 liq=4543329.24785 tmpl=0.9 eq=0.0 qual=1.0 reasons=['reject:religion_prophecy'] q='Will Jesus Christ return before 2027?'
- `559688` (event `30829`) vol=32355231.570859 liq=1491127.64476 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Andrew Yang win the 2028 Democratic presidential nomination?'
- `561247` (event `31552`) vol=31919716.040518 liq=1230594.08482 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 US Presidential Election?'
- `561251` (event `31552`) vol=31892248.614778 liq=462411.07605 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 US Presidential Election?'
- `553874` (event `27830`) vol=31853613.712182 liq=1062359.51473 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market', 'reject:winner_template'] q='Will the Memphis Grizzlies win the 2026 NBA Finals?'
- `559683` (event `30829`) vol=31598506.209372 liq=714982.42361 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will George Clooney win the 2028 Democratic presidential nomination?'
- `559677` (event `30829`) vol=30771141.62138 liq=1132131.7303 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hillary Clinton win the 2028 Democratic presidential nomination?'
- `559685` (event `30829`) vol=30535199.114493 liq=1841068.38832 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will MrBeast win the 2028 Democratic presidential nomination?'
- `566192` (event `33507`) vol=30335577.717611 liq=1304989.22432 tmpl=1.0 eq=0.0 qual=1.0 reasons=['reject:sports_market'] q='Will Tottenham win the 2025–26 English Premier League?'
- `559671` (event `30829`) vol=30013296.206881 liq=1608227.44575 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Zohran Mamdani win the 2028 Democratic presidential nomination?'
- `559679` (event `30829`) vol=29899698.940763 liq=1378094.44318 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Bernie Sanders win the 2028 Democratic presidential nomination?'
- `559681` (event `30829`) vol=28754868.267211 liq=1839973.25864 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will LeBron James win the 2028 Democratic presidential nomination?'
- `566174` (event `33506`) vol=28392439.058395 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Slavia Pragu win the 2025–26 Champions League?'
- `1303355` (event `194107`) vol=28287977.13917 liq=3467411.61987 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:price_target_template'] q='Will Bitcoin reach $150,000 in February?'
- `561249` (event `31552`) vol=28188312.853092 liq=432646.95447 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Greg Abbott win the 2028 US Presidential Election?'
- `559680` (event `30829`) vol=27719822.618163 liq=1587766.06583 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Phil Murphy win the 2028 Democratic presidential nomination?'
- `559678` (event `30829`) vol=27288333.489289 liq=1209307.42361 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Liz Cheney win the 2028 Democratic presidential nomination?'
- `559666` (event `30829`) vol=26614585.227434 liq=1635721.32575 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tim Walz win the 2028 Democratic presidential nomination?'
- `559682` (event `30829`) vol=25427602.851377 liq=1558340.38655 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Hunter Biden win the 2028 Democratic presidential nomination?'
- `561995` (event `31875`) vol=24983611.198316 liq=729995.26758 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Mike Pence win the 2028 Republican presidential nomination?'
- `561242` (event `31552`) vol=24455908.340107 liq=693252.52863 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Tulsi Gabbard win the 2028 US Presidential Election?'
- `559690` (event `30829`) vol=23707782.508815 liq=1888248.38446 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Kim Kardashian win the 2028 Democratic presidential nomination?'
- `559670` (event `30829`) vol=23135939.001335 liq=847329.73903 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Gina Raimondo win the 2028 Democratic presidential nomination?'
- `559689` (event `30829`) vol=22951879.856557 liq=873980.1117 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Beto O’Rourke win the 2028 Democratic presidential nomination?'
- `566167` (event `33506`) vol=21360158.2305 liq=None tmpl=1.0 eq=0.0 qual=0.65 reasons=['reject:sports_market'] q='Will Olympiakos win the 2025–26 Champions League?'
- `561248` (event `31552`) vol=21352979.783625 liq=723624.83284 tmpl=0.7 eq=0.0 qual=1.0 reasons=['reject:winner_template'] q='Will Vivek Ramaswamy win the 2028 US Presidential Election?'
