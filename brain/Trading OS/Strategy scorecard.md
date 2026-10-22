---
tags: [trading, strategy, moc]
type: moc
created: 2026-10-21
updated: 2026-10-21
summary: Every Z.E.R.O strategy with its mode and live record. The Scribe refreshes each card's live block nightly.
related: ["[[ZERO trading agent]]", "[[Playbook]]"]
---

# Strategy scorecard

Part of [[ZERO trading agent]]. Real-money record since 2026-09-30: 5 closed trades, 1 winner, −$0.24 realized (as of 2026-10-21). Too few trades to judge any strategy yet.

| Strategy | Mode | Live record (2026-10-21) |
|---|---|---|
| [[USO 4h trend]] | real | 4 trades since 2026-09-30: 3 closed (1 win: +$0.45 on 2026-10-16; −$0.15 stop; −$0.04 manual exit), net +$0.26. 1 open since 2026-10-20 (entry 160.14, stop 156.93). |
| [[GLD 4h trend]] | real | 0 trades (GLD has been in a 4h downtrend). |
| [[QQQ 15m FVG]] | real | 0 trades. |
| [[SPY 15m FVG]] | paper | 1 real trade before the switch (2026-09-30, −$0.02). |
| [[Board signals (stocks)]] | real | 1 trade: GOOGL prior-day-low sweep 2026-10-16 → stop 2026-10-21, −$0.49. Note: that trigger came from board data that was 2 weeks stale. |
| [[Crypto board copy]] | real | 0 real trades (the board was stale from Oct 3 to Oct 21, so no board paper trades opened). |
| [[Crypto sweep FVG]] | paper | 3 paper trades (2026-10-02 to 10-04), −$0.31 after fees. |
| [[5m scout setups]] | alerts | 0 real trades. Alert: PLTR RSI(2) dip fired 2026-10-21 1:48 PM (40% of 10 unseen). |
| [[Trinity NQ ES]] | paper | Since 2026-10-15: 1 paper trade (NQ 2026-10-21: +1R at 1R, −1R at 2R/3R). Other sessions had no full setup by noon. |

```dataview
TABLE mode, updated FROM "brain/Trading OS/Strategies" SORT mode ASC
```
