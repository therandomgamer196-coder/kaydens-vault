---
tags: [trading, daily-desk]
type: note
created: 2026-11-26
updated: 2026-11-26
summary: No real trades (bot account ••3001 unfunded, $0.13 buying power). ADA, BONK and ETH paper board longs and the Lab CLS dip still open. Lab champions rose 7→12; forward record still 22 trades at −5.95%/trade. Research (idea only): tax-loss reversal, 52-week-high screen and overnight drift all fail after costs; earlier, correlated entries caused ~92% of Lab losses. Lab vault pushes still refused; 3D brain builder still missing.
related: ["[[ZERO trading agent]]", "[[Trading OS change log]]", "[[Daily desk 2026-11-25]]"]
---

# Daily desk 2026-11-26

Part of [[ZERO trading agent]]. Written by the Scribe every 3 hours, newest first. Previous desk: [[Daily desk 2026-11-25]].

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
