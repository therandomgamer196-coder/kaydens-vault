---
tags: [trading, bitcoin, plan]
date: 2026-09-30
---
# Bitcoin Trading Agent: Plan (draft, will change)

> [!info] Goal
> Dedicated system that backtests Bitcoin strategies, watches 5-minute candles 24/7 and alerts me with times to enter or exit a trade.

## Plan so far
1. Claude writes candidate BTC strategies (EMA trend, breakout, mean reversion) as **Freqtrade** code.
2. Backtest on 2-3+ years of 5-minute data, using walk-forward / out-of-sample testing to avoid overfitting.
3. Claude reads results, prunes weak strategies, refines survivors.
4. Run survivors in Freqtrade **dry-run** on an always-on VPS (Hetzner or DigitalOcean, about $5/month) for 2-4 weeks.
5. Alerts to my phone via a **Telegram bot**: enter/exit with stop and target.
6. Only after dry-run decide on real money (I place trades, or the bot with small size).

## Options
| Job | Options |
|---|---|
| 5-min candle data | Binance, Coinbase, Kraken, Bybit public APIs via CCXT (free) |
| Backtesting | Freqtrade, vectorbt, backtesting.py, Jesse |
| Always-on hosting | Hetzner / DigitalOcean VPS, Railway, Fly.io, Oracle free tier |
| Alerts | Telegram (easiest), ntfy.sh, Pushover, Discord webhook |
| No-code | 3Commas, Cryptohopper, TradingView Pine alerts (mostly paid) |

## Notes
- Claude scheduled tasks can't run every 5 minutes; a rule-based engine watches, Claude does research and review.
- Backtests often fail live (overfitting, fees, slippage). Signals are not financial advice.
- Pricing/limits were from memory; check before committing.
- Not started yet.
