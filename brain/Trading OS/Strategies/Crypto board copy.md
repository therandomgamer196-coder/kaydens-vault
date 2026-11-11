---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-11-11
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
As of 2026-11-11 11:41 ET: 0 real trades, 0 wins, net $0.00, no real trade date yet. The ETH oversold board setup (64.5% of 31) fired on 2026-11-11 (paper long opened 8:45 AM ET) and the real copy was skipped at 8:52 and 9:53 AM: the bot account has only $0.13 buying power (minimum $2.00). The ADA oversold setup (70% of 40) was skipped the same way on 2026-11-10. Earlier: the 2026-11-03 ADA buys were denied by the permission check.
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
