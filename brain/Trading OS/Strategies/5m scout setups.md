---
tags: [trading, strategy]
type: strategy
mode: alerts
created: 2026-10-21
updated: 2026-10-27
summary: The 5-minute engine finds setups that win on unseen data (70/30 split). Auto trading is OFF, so it only create
related: ["[[Strategy scorecard]]", "[[ZERO trading agent]]"]
---

# 5m scout setups

**Mode:** alerts · Part of [[Strategy scorecard]] · Rules in [[ZERO trading agent]]

## Rule
The 5-minute engine finds setups that win on unseen data (70/30 split). Auto trading is OFF, so it only creates Robinhood alerts.

## Backtest
2026-10-21: 4 proven of 47 markets, unseen samples small (n ≈ 8-10).

## Live record
<!-- live:start -->
As of 2026-10-27 17:42 ET: 0 real trades (Auto OFF). 4 proven setups at 4:48 PM, none firing; 4 managed Robinhood alerts (MXL price crosses 5m EMA21 added).
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
