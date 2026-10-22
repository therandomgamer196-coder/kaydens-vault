---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-10-21
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
As of 2026-10-21: 4 trades since 2026-09-30: 3 closed (1 win: +$0.45 on 2026-10-16; −$0.15 stop; −$0.04 manual exit), net +$0.26. 1 open since 2026-10-20 (entry 160.14, stop 156.93).
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
