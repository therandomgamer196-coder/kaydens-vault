---
tags: [trading, daily-desk]
type: note
created: 2026-10-28
updated: 2026-10-28
summary: Quiet overnight; no real trades; USO 4h trend still open at 163.23; account $9.61; no board, crypto or 5m setups; Lab gens 1168-1180 with no new paper trades (forward 10 trades, −1.08%/trade); research found long-only VWAP cross loses, unusual-volume screen is the one stable Finviz-style edge, Numerai Signals as a free scorer; Lab brain push and 3D brain builder still failing.
related: ["[[ZERO trading agent]]", "[[Trading OS change log]]", "[[Daily desk 2026-10-27]]"]
---

# Daily desk 2026-10-28

Part of [[ZERO trading agent]]. Written by the Scribe every 3 hours, newest first.

## 02:42 ET

**Real trades (bot account ••3001)**
- No buys or sells since 11:42 PM (market closed). Open: **USO 0.029406 sh @ 163.23** (4h trend), last checked 3:50 PM Oct 27 at bid 163.34 (about +$0.00), stop 159.97, first target 166.49.
- Account $9.61, buying power $4.36. Circuit breaker: 0 losses. Realized bot P&L since start: +$0.39 on $15 start cash.
- Real crypto (11:53 PM, 12:52, 1:53 AM): no board setup, 0 open, $4.36 crypto buying power, no orders. Real 5m: none (Auto OFF).

**Board**: Probability board (8:21 PM refresh, bar date Tue Oct 27) has no decent setups; nothing fired.

**Paper crypto (11:45 PM)**: no setups after fees, no board hits, 0 paper trades open. PDH sweeps that closed back below (buy-side liquidity taken): **ETH 2,360.92** (wick 2,366.37), **SOL 101.74** (wick 101.88), **ADA 0.20693** (wick 0.20784); info sweep AVAX 1h high 9.0440. PENGU +5.5% in 24h. BTC top-ranked, 4h mixed. Next scan 2:44 AM.

**5-minute scout (11:48 PM to 1:48 AM)**: 48 markets, 3 proven setups (SOFI, USO, MSTR), none firing; 3 Robinhood alerts unchanged (SOFI below 14.4, USO above 166.38, MSTR above 142). Auto OFF.

**Lab (Ultron)**: generations 1168, 1174 and 1180; 4 to 5 champions pass out-of-sample (down from 7-11); 4 paper trades open (AAOI, AEHR, CIFR ×2), none opened or closed; 77-80 markets tested. Forward record still **10 trades, 50% winners, −1.08% per trade**. No proposals.

**Research** (idea only)
- [U20261028T0029] **Long-only VWAP cross loses after costs.** The famous QQQ VWAP result (Zarattini & Aziz 2023) is long/short on 1-minute bars. The long half on 5-minute bars (60 days, 14 Lab stocks plus QQQ/SPY, 0.05% each way): 2,746 trades, 18.1% winners, −0.129%/trade; only PLTR was net positive, and 5 days made all of that. Whipsaws about 3 times a day. 2 variants; 60 days is far short of the 2-year gate. Don't build a VWAP-cross trigger. Source: [Bear Bull Traders](https://bearbulltraders.com/?p=2606339).
- [U20261028T0133] **Finviz-style screens on Yahoo data.** Finviz blocks automated reads and the Lab's Finviz feed returned 0 names, so the Lab rebuilt 4 screens on 51 stocks (Oct 2022–Oct 2026, next-open entry, 0.2% round trip). Only **unusual volume (2x+ average)** held in both halves: +0.96% excess per 5-day hold (n=2,085), +1.17% out-of-sample (n=910), but RGTI, MXL and IBRX supplied 53% of it and none clear t > 3. 52-week highs and oversold-in-uptrend showed no edge. 8 variants plus 2 splits; survivor universe.
- [U20261028T0230] **Numerai Signals (income idea).** Staking earns or burns up to 3.5% of stake per round, with a churn penalty; no median return is published, so a $100 stake is roughly −$30 to +$30 a year (estimate) plus NMR price risk. The real value is free unstaked submissions as an independent out-of-sample score on the Lab's rankings. Kayden would need to check eligibility in the terms. Sources: [Signals submissions](https://docs.numer.ai/numerai-signals/submissions), [Signals staking](https://docs.numer.ai/numerai-signals/staking), [Numerai forum](https://forum.numer.ai/t/644-8-1-year-return-how/6343).

**Problems seen**
- Brain sync: the Lab's 12:33, 1:34 and 2:30 AM runs got a 403 on push again (add_repo isn't offered to that task). Its research notes and Ideas lines live only in the page database; the research is summarized above.
- 3D brain: not rebuilt. `graphify-out/build_brain_data.py` is still missing from the vault (only `build_brain_map.py` exists), so Jarvis Brain 3D stays at its 2026-10-22 build. The watchdog flagged it again at 12:46 AM. Open item in [[Handoff to Claude]].
- Daily Market Brief last failed on the usage limit (Oct 27 8:00 AM); next try 7:52 AM today.
- No Trading OS rule, config or scheduled-task changes in the last 3 hours.

Not financial advice.
