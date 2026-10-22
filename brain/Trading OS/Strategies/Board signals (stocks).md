---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-10-21
summary: When the nightly Probability board marks a stock signal decent (n ≥ 25, win ≥ 55%, +3 pts vs baseline, both ha
related: ["[[Strategy scorecard]]", "[[ZERO trading agent]]"]
---

# Board signals (stocks)

**Mode:** real · Part of [[Strategy scorecard]] · Rules in [[ZERO trading agent]]

## Rule
When the nightly Probability board marks a stock signal decent (n ≥ 25, win ≥ 55%, +3 pts vs baseline, both halves ≥ 52%, positive expectancy) and it triggers live, buy with stop and first target at ±1 daily ATR.

## Backtest
Per signal on the board. 2026-10-21: GOOGL prior-day-low sweep 58.8% of 102; MSFT prior-day-low sweep 61.3% of 93 (fired 10-21); MSFT breakout 65.5% of 55.

## Live record
<!-- live:start -->
As of 2026-10-21: 1 trade: GOOGL prior-day-low sweep 2026-10-16 → stop 2026-10-21, −$0.49. Note: that trigger came from board data that was 2 weeks stale.
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
