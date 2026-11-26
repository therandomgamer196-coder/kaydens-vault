---
tags: [trading, daily-desk]
type: note
created: 2026-11-26
updated: 2026-11-26
summary: No real trades (bot account ••3001 unfunded, $0.13 buying power; stock market closed for Thanksgiving). ADA, BONK and ETH paper board longs and the Lab CLS dip still open; Lab paper-bought MU on the holiday (no holiday check). Lab champions 12→10→8; forward record still 22 trades at −5.95%/trade. Research (idea only): slow crypto trend rules fail after fees on unseen data; hourly stop checks erase the RSI(2) dip edge; beehiiv bans fully AI-run newsletters. Lab vault pushes still refused; 3D brain builder still missing.
related: ["[[ZERO trading agent]]", "[[Trading OS change log]]", "[[Daily desk 2026-11-25]]"]
---

# Daily desk 2026-11-26

Part of [[ZERO trading agent]]. Written by the Scribe every 3 hours, newest first. Previous desk: [[Daily desk 2026-11-25]].

## 11:41 ET

Covers 8:42 to 11:41 AM ET. Thanksgiving: US stock market closed today.

**Real trades:** none. The real crypto trader ran at 8:53, 9:53 and 10:53 AM: no board setup inside its 75-minute window (the ADA, BONK and ETH setups from 2026-11-24 are too old), 0 real crypto trades open, bot account ••3001 effectively unfunded ($0.13 buying power). Stock auto-trader took holiday snapshots only (9:51, 10:51 AM). 0 real 5m trades open.

**Open paper positions:**
- Crypto monitor board longs ($7.50 each, 10-day max), all from 2026-11-24: ADA, BONK and ETH oversold bounces. None closed.
- Lab: CLS RSI(2) dip at 182.65, last 191.95 (about +5.1%). **New:** MU RSI(3) < 35 dip bought at 601.25 at 9:30 AM (stop 549.66, target 876.38, 5-day max). The market was closed, so this entry used a stale price (see research and problems below).

**Crypto scan:** 8:45 AM: SOL top-ranked (4h mixed); SOL +6.2%, XRP +6.5%, PEPE +6.0% in 24h. 9:46 AM: no new sweeps or setups. 10:45 AM: LTC swept its 1h swing high 43.828 (wick 43.896) and DOGE swept its equal 1h highs 0.05716 (wick 0.05724), both closed back below (buy-side liquidity taken, bearish short-term). No setups, no board hits.

**Probability board:** no change since the 8:20 PM refresh on 11/25; no market has "Decent odds now".

**5m scout:** ran at 8:48, 9:48 and 10:49 AM. 48 markets, 3 proven setups (RKLB ORB, AMD and PINS 5m RSI(2) dip), none firing. 3 Robinhood alerts unchanged. Auto is OFF (alerts only).

**Lab (paper):** gens 2824, 2830 and 2836. Champions passing out-of-sample **10 → 9 → 8**; 71 markets tested. 2 paper trades open (CLS, MU), 1 opened, none closed. Forward record unchanged: **22 trades, −5.95%/trade**. 5 flaws flagged, no proposals.

**Research (all idea only)**
- U20261126T1430 (9:30 AM), **the Lab has no market-holiday check.** It paper-bought MU on Thanksgiving because the entry gate checks only weekday and clock time. On 25 names over 3 years, holiday gaps averaged +0.06% with a mean absolute size of 1.35% (n = 750), similar to normal overnight gaps, so it adds noise rather than bias. Fix: add the NYSE holiday calendar. Sources: [NYSE hours and calendars](https://www.nyse.com/markets/hours-calendars), [NYSE 2026–2028 holiday calendar (Business Wire)](https://www.businesswire.com/news/home/20251223981478/en/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar).
- U20261126T1531 (10:31 AM), **position sizing can't rescue a thin edge.** The RSI(2) dip setup makes about +0.035R/trade at every volatility level (49 names, unseen Nov 2023–Nov 2026, n = 2,906). Equal-dollar sizing +4.7% with a −56% drawdown; 1%-risk sizing −24.7%; edge-gated half-Kelly sat out 96% of trades (−17% drawdown). 5 sizing rules tested. Sources: [Harvey et al. 2018 (Duke PDF)](https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf), [Alpha Architect](https://alphaarchitect.com/volatility-targeting-improves-risk-adjusted-returns/).
- U20261126T1632 (11:32 AM), **Black Friday half-day is too thin to trade.** Tomorrow NYSE closes at 1:00 PM ET. On 25 names (2002–2025, n = 470) volume runs ~40% of normal and range ~61%; +0.41%/day average but median +0.03%, 50.6% win, t = 1.02, and 3 of 24 years made 92% of the gain. 5 measures tested. Sources: [E*TRADE (Nov 2024)](https://us.etrade.com/knowledge/library/perspectives/daily-insights/thanksgiving-seasonal), [Bloomberg (Nov 2022)](https://www.bloomberg.com/news/articles/2022-11-25/stock-market-has-a-black-friday-tradition-low-trading-volume).

**Problems seen**
1. **Bot account unfunded** ($0.13 buying power), so no real trades are possible.
2. **Lab vault pushes still denied (403)** at 9:30, 10:31 and 11:34 AM (add_repo not available in that task). Its research and Ideas updates stay in the page database only.
3. **Lab traded on a market holiday** (MU paper buy at a stale price). Paper only, but it pollutes the forward record; engine needs an NYSE holiday check.
4. **3D brain not rebuilt:** `graphify-out/build_brain_data.py` is still missing from the vault (only `build_brain_map.py` is there).
5. **Daily Market Brief:** today's 7:52 AM run is still marked pending almost 4 hours later.
6. No rule or task-setting changes: config/rules matches the snapshot, and no task was edited in this window.

## 08:41 ET

Covers 5:42 to 8:41 AM ET. Thanksgiving: US stock market closed today.

**Real trades:** none. The real crypto trader ran at 5:53, 6:53 and 7:52 AM: no board setup inside its 75-minute window (the ADA, BONK and ETH setups from 2026-11-24 are too old), 0 real crypto trades open, bot account ••3001 effectively unfunded ($0.44 value, $0.13 buying power). Stock auto-trader idle (holiday). 0 real 5m trades open.

**Open paper positions:**
- Crypto monitor board longs ($7.50 each, 10-day max), all from 9:46 PM 2026-11-24: ADA, BONK and ETH oversold bounces. None closed.
- Lab: CLS RSI(2) dip at 182.65, last 191.95 (about +5.1%), 2-day max.

**Crypto scan:** 5:45 AM: BTC top-ranked, PENGU +5.8% in 24h. 7:45 AM: SOL top-ranked (4h mixed); SOL and SUI swept their 1h swing lows (70.43, 0.6645) and closed back above; both formed sweep + FVG setups but lose after the 0.95% fee each way (SOL −0.08R, SUI −0.35R), so skipped. SUI +6.2%, ADA +6.8%, DOGE +6.1% in 24h. No board hits.

**Probability board:** no change since the 8:20 PM refresh on 11/25; no market has "Decent odds now".

**5m scout:** ran at 5:48, 6:49 and 7:48 AM. 48 markets, 3 proven setups (RKLB ORB, AMD and PINS 5m RSI(2) dip), none firing. 3 Robinhood alerts unchanged. Auto is OFF (alerts only).

**Lab (paper):** gens 2806, 2812 and 2818. Champions passing out-of-sample **12 → 11 → 10**; 71 markets tested. 1 paper trade open (CLS), none opened or closed. Forward record unchanged: **22 trades, 22.7% winners, −5.95%/trade (−$9.82)**. 5 flaws flagged, no proposals.

**Research (all idea only)**
- U20261126T1132 (6:32 AM), **slow crypto trend rules don't survive the fee on unseen data.** 8 MA/breakout variants on 10 coins made big gains in 2016–2023 but −10.3% to +5.5%/trade on Nov 2023–Nov 2026; the best (50-day breakout) had t = 1.4 and its top 5 trades were 128% of the profit. Fails gates 3 and 5. Sources: [Annals of OR](https://link.springer.com/article/10.1007/s10479-019-03357-1), [Rink 2023](https://link.springer.com/content/pdf/10.1007/s11408-023-00433-2.pdf), [arXiv 2602.11708](https://arxiv.org/pdf/2602.11708).
- U20261126T1231 (7:31 AM), **hourly stop checks erase the RSI(2) dip edge.** On 30 stocks/ETFs (n = 4,462, Sep 2022–Nov 2026) a resting stop gives +0.054R/trade; an estimated hourly-check fill gives −0.022R/trade. Robinhood bracket orders are whole-share only. 2 exit models. Sources: [Robinhood fractional shares](https://robinhood.com/us/en/support/articles/fractional-shares), [Robinhood stop order](https://robinhood.com/us/en/support/articles/stop-order), [BrokerChooser](https://brokerchooser.com/invest-long-term/risk-management/stop-loss-order-robinhood).
- U20261126T1331 (8:31 AM), **a beehiiv newsletter can be agent-drafted, not agent-run.** Estimates: $50–150/mo in ads at 1,000 subscribers vs ~$49/mo plan; beehiiv's Jul 2026 rules ban fully AI-built newsletters. Sources: [Sirency](https://www.sirency.com/blog/beehiiv-ad-network-and-boosts), [Roo](https://roo.beehiiv.com/p/how-to-make-money-on-beehiiv).

**Problems seen**
1. **Bot account unfunded** ($0.13 buying power), so no real trades are possible.
2. **Lab vault pushes still denied (403)** at 6:34, 7:31 and 8:31 AM (add_repo not available in that task). Its research stays in the page database only.
3. **3D brain not rebuilt:** `graphify-out/build_brain_data.py` is still missing from the vault (only `build_brain_map.py` is there). Watchdog (7:45 AM) flagged the 3D brain as stale since 2026-10-22.
4. **Daily Market Brief:** watchdog flagged the 11/25 run as abandoned; today's 7:52 AM run was still pending at 8:41 AM.
5. No rule or task-setting changes: config/rules matches the snapshot, and no task was edited in this window.

## 05:41 ET

Covers 2:42 AM to 5:41 AM ET.

**Real trades:** none. The real crypto trader ran at 2:53, 3:52 and 4:52 AM: no board setup inside its 75-minute window, 0 real crypto trades open, bot account ••3001 effectively unfunded ($0.13 buying power). Stock auto-trader idle (market closed overnight; today is Thanksgiving). 0 real 5m trades open.

**Open paper positions** (unchanged, none opened or closed):
- Crypto monitor board longs ($7.50 each, 10-day max) from 9:46 PM 2026-11-24: ADA oversold at 0.14194 (stop 0.130382, target 0.153498), BONK oversold at 0.00000207 (stop 0.00000185315, target 0.00000228685), ETH oversold at 1653.28 (stop 1556.87, target 1749.69).
- Lab: CLS RSI(2) dip at 182.65, last 191.95 (about +5.1%), 2-day max.

**Crypto scan (2:45 AM):** BTC top-ranked (4h mixed); 24h up moves: WIF +9.0%, LTC +8.0%, LINK +5.3%, BONK +5.3%. No setups. All 4 meme coins passed the coin check.

**Probability board:** no change since the 8:20 PM refresh (Nov 25 bars); no market has "Decent odds now".

**5m scout:** ran at 2:48, 3:48 and 4:47 AM. 48 markets, 3 proven setups (RKLB, AMD, PINS), none firing. 3 Robinhood alerts unchanged. Auto is OFF (alerts only).

**Lab (paper):** gens 2788, 2794 and 2800. Champions passing out-of-sample rose from 7 to **8**, **9**, then **12**; markets tested 70 → 72. 1 paper trade open (CLS). Forward record unchanged: **22 trades, 22.7% winners, −5.95%/trade (−$9.82)**. 5 flaws flagged, no proposals.

**Research (all idea only)**
- U20261126T0832 (3:32 AM), **tax-loss reversal is small and unreliable on big stocks.** Buying the worst 20% YTD names on Dec 20 and selling Jan 10 made +2.53%/trade vs +2.21% for all names and +1.33% SPY (11 seasons, 258 picks, 60.5% win, after 0.10% cost), but per-season excess was only +0.43% (t≈0.65) and it lagged in 2023–24. 3 variants. Sources: [Applied Finance Letters](https://ojs.aut.ac.nz/applied-finance-letters/article/download/615/164), [Alpha Architect](https://alphaarchitect.com/2015/12/tis-the-season-for-strange-effects-in-the-stock-market/).
- U20261126T0931 (4:31 AM), **the 52-week-high screen is worse than buying any day.** On 87 big stocks, buying within 2% of the 1-year high (above SMA200) made +0.66% per 10 days on unseen data (Nov 2023–Nov 2026, n=10,391) vs +0.84% for every day, and lost −0.82%/trade since September. 6 variants. Sources: [George & Hwang](https://www.bauer.uh.edu/tgeorge/papers/gh5-paper.pdf), [Yu (AUT)](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/56468/657406-H-Yu-Nearness-to-the-52-week-high-and-low-prices,-past-returns,-and-average-stock-returns.pdf).
- U20261126T1031 (5:31 AM), **overnight drift is real but too thin to trade.** On 52 Lab stocks/ETFs, close-to-open made +0.113%/night gross vs +0.034% open-to-close (unseen Nov 2024–Nov 2026, n≈25.7k), but a 0.10% round trip leaves +0.013% (t=0.49); SPY/QQQ/IWM go negative, and it lost −0.12%/night since September. 6 variants. Sources: [Alpha Architect](https://alphaarchitect.com/trading-costs-wipe-out-the-overnight-return-anomaly/), [arXiv 2507.04481](https://arxiv.org/html/2507.04481v1).

**Problems seen**
1. **Bot account unfunded** ($0.13 buying power), so no real trades are possible.
2. **Lab vault pushes still denied (403)** at 3:33, 4:33 and 5:33 AM (add_repo not available in that task). Its research and ideas stay in the page database only.
3. **3D brain not rebuilt:** `graphify-out/build_brain_data.py` is still missing from the vault. The watchdog (3:46 AM) flagged Jarvis Brain 3D data as stale since 2026-10-22.
4. **Daily Market Brief:** its 11/25 7:53 AM run was abandoned (watchdog, 3:46 AM); next run 7:52 AM ET today.

## 02:41 ET

Covers 11:42 PM (Nov 25) to 2:41 AM ET.

**Real trades:** none. The real crypto trader ran at 11:52 PM, 12:52 and 1:52 AM: no board setup inside its 75-minute window (the ADA, BONK and ETH setups from 2026-11-24 are too old), 0 real crypto trades open, bot account ••3001 effectively unfunded ($0.44 value, $0.13 buying power). Stock auto-trader idle overnight. 0 real 5m trades open.

**Open paper positions:**
- Crypto monitor board longs ($7.50 each, 10-day max), all from 9:46 PM 2026-11-24: ADA oversold at 0.14194 (stop 0.130382, target 0.153498; 68.3% of 41), BONK oversold at 0.00000207 (stop 0.00000185315, target 0.00000228685; 75% of 40), ETH oversold at 1653.28 (stop 1556.87, target 1749.69; 64.5% of 31). None closed.
- Lab: CLS RSI(2) dip at 182.65, last 191.95 (about +5.1%), 2-day max.

**Crypto scan:** no runs in this window (the monitor skips midnight to 2 AM ET); last scan 11:45 PM: BTC top-ranked (4h mixed), no sweeps, no setups.

**Probability board:** no change since the 8:20 PM refresh; no market has "Decent odds now".

**5m scout:** ran at 11:47 PM, 12:49 and 1:47 AM. 48 markets, 3 proven setups (RKLB, AMD, PINS), none firing. RKLB breakout alert nudged 43.83 → 43.82 → 43.83. 3 Robinhood alerts active. Auto is OFF (alerts only).

**Lab (paper):** gens 2770, 2776 and 2782. Champions passing out-of-sample fell from 10 to **3**, then back to **6** and **7**; markets tested dropped 92 → 82 → 75. 1 paper trade open (CLS), none opened or closed. Forward record unchanged: **22 trades, 22.7% winners, −5.95%/trade (−$9.82)**. 5 flaws flagged, no proposals.

**Research (all idea only)**
- U20261126T0531 (12:31 AM), **Etsy digital downloads can't run hands-off.** A $10 file nets about $8.60 after fees ($7.10 with Offsite Ads, estimates), but Etsy's Oct 22, 2026 AI update bans bot-made listings and AI-written guides. Sources: [Checkout Page](https://checkoutpage.com/blog/etsy-fees), [Digital Commerce 360](https://www.digitalcommerce360.com/2026/10/26/etsy-ai-policy/amp/), [Value Added Resource](https://www.valueaddedresource.net/etsy-bans-ai-patterns/).
- U20261126T0632 (1:32 AM), **the Lab's champion bar barely filters luck.** 3,000 random rules pass it 0.33% of the time on real data vs 0.30% on shuffled no-edge data (17 markets); the out-of-sample window is reused every generation (~178k evaluations, estimate). Best champion's unseen t = 1.14, below the no-edge max of 3.9. Sources: [Bailey & López de Prado (SSRN 2460551)](https://papers.ssrn.com/abstract=2460551), [SSRN 2326253](https://papers.ssrn.com/abstract=2326253).
- U20261126T0732 (2:32 AM), **correlated entries caused ~92% of Lab paper losses.** 12 of 22 trades came on 2 days (Oct 27, Nov 3), 8 in one bitcoin-miner/AI-datacenter cluster. A 60-day correlation cap (skip if corr ≥ 0.6 to a pick already taken) cut backtest drawdown from −$88.7 to −$59.3 (n=1,972, Sep 2024–Nov 2026); a flat 3-per-day cap hurt. 4 variants. Sources: [Longin & Solnik 2001](https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:2:p:649-676), [CryptoSlate](https://cryptoslate.com/high-betas-low-correlations-miners-break-from-bitcoin-patterns/).

**Problems seen**
1. **Bot account unfunded** ($0.13 buying power), so no real trades are possible.
2. **Lab vault pushes still denied (403)** at 12:33, 1:32 and 2:34 AM (add_repo not available in that task). Its research and ideas stay in the page database only.
3. **3D brain not rebuilt:** `graphify-out/build_brain_data.py` is still missing from the vault (the Scribe's add_repo tool was also unavailable this run, though cloning worked).
4. Watchdog (11:45 PM) flagged the stale 3D brain and the abandoned Daily Market Brief from 2026-11-25.
5. No rule or task-setting changes: config/rules matches the snapshot, and no task was edited in this window.
