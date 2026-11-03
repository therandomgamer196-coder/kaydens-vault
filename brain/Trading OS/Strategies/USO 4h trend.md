---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-11-03
summary: Buy USO when the 4-hour 20 EMA is above the 50 EMA and the ask is above the 20 EMA. Stop −2%, first target +2%
related: ["[[Strategy scorecard]]", "[[ZERO trading agent]]"]
---

# USO 4h trend

**Mode:** real · Part of [[Strategy scorecard]] · Rules in [[ZERO trading agent]]

## Rule
Buy USO when the 4-hour 20 EMA is above the 50 EMA and the ask is above the 20 EMA. Stop −2%, first target +2% (sell half, stop to breakeven), trail the rest.

## Backtest
+0.56% per trade over 96 trades in 2 years (2026-10-04, stop −2% / target +4%).

## Live record
<!-- live:start -->
As of 2026-11-03 14:45 ET: 6 real trades since 2026-09-30, all closed. 3 won: +$0.45 (2026-10-16), +$0.63 (2026-10-23, runner sold by hand) and +$0.08 (2026-10-29, trailing stop). 3 lost: −$0.04 (manual exit), −$0.15 (stop) and −$0.20 (2026-11-03, stop hit at 157.11 after a $4.84 buy at 164.02 on 2026-10-29). Net +$0.78 after costs (stocks have no commission). 0 open. Last trade 2026-11-03.
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
