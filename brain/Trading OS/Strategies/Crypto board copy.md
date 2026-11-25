---
tags: [trading, strategy]
type: strategy
mode: real
created: 2026-10-21
updated: 2026-11-24
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
As of 2026-11-24 23:41 ET: 0 real trades, 0 wins, net $0.00, no real trade date yet. On 2026-11-24 the BONK (75% of 40), ADA (68.3% of 41) and ETH (64.5% of 31) oversold board setups fired (paper longs opened 9:46 PM ET); the real copies were skipped at 9:53 and 10:53 PM because the bot account is unfunded ($0.13 buying power, $2.00 minimum). Paper board record: 3 closed, 0 wins, −$1.78 after fees (last closes 2026-11-21, ADA −$0.66 and ETH −$0.49, stops hit); n=3, too few to judge.
<!-- live:end -->

## Notes
- Samples this small can be luck. Judge it after 20-30 live trades.
