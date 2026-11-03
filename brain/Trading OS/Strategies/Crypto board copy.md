---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-11-03
summary: The real crypto trader copies paper BOARD trades opened by the crypto monitor in the last 75 minutes. First-ta
related: ["[[Strategy scorecard]]", "[[ZERO trading agent]]"]
---

# Crypto board copy

**Mode:** real · Part of [[Strategy scorecard]] · Rules in [[ZERO trading agent]]

## Rule
The real crypto trader copies paper BOARD trades opened by the crypto monitor in the last 75 minutes. First-target gain must be ≥ 3% after the 1.9% round-trip fee.

## Backtest
Board 2026-10-21 (after fees): PEPE oversold 78.9% of 38, BONK oversold 75.0% of 40, ADA oversold 70.0% of 40. Rare and clustered in crashes; ~90 combos tested, so some may be luck.

## Live record
<!-- live:start -->
As of 2026-11-03 14:45 ET: 0 real trades. The ADA oversold board setup (70% of 40) fired on 2026-11-03, but both $4.77 buy attempts (12:53 PM and 1:54 PM ET) were denied by the session permission check, so nothing was bought. Net $0.00.
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
