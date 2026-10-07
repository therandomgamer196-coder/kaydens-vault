---
tags: [trading, crypto, monitor]
aliases: [Crypto 24/7 monitor, crypto monitor, crypto scanner]
created: 2026-10-01
updated: 2026-10-01
summary: Hourly 24/7 paper-only scan of 10 popular coins - resting liquidity, sweeps, sweep + FVG setups, fee-aware paper trades and timestamped alerts.
---

# Crypto 24/7 monitor

Part of [[Trading OS]]. A Claude scheduled task, "Crypto 24/7 monitor (paper)", that runs **every hour at :30, around the clock**. It started 2026-10-01 (first run 9:30 PM ET). It watches the most popular coins so Kayden can learn how crypto liquidity behaves, and it paper-trades setups to see whether any would pay after fees.

> [!warning] Paper only
> The Agentic account charges **0.95% to buy and 0.95% to sell** (checked with a Robinhood order preview on 2026-10-01). A trade has to make more than 1.9% just to break even. A 30-day backtest found every 15-minute crypto setup losing after fees, so the monitor never places real orders. Turning real crypto on needs Kayden's explicit OK.

## Coins

BTC, ETH, SOL, XRP, DOGE, ADA, LINK, AVAX, LTC, SUI. Candles come from Coinbase's public API (Robinhood has no crypto chart data); paper fills use Robinhood's live quotes.

## What it looks for (see [[Trading glossary]])

- **Resting liquidity:** the prior UTC day's high and low (PDH/PDL) and untaken 1-hour swing highs and lows. Equal highs or lows are two swing points within 0.1% of each other, at least 6 hours apart.
- **Sweep:** a 1-hour candle wicks through one of those levels and closes back inside. A sell-side sweep (a low taken) is bullish; a buy-side sweep (a high taken) is bearish.
- **Sweep + FVG setup (long):** a bullish 15-minute fair value gap within about 2 hours after a sell-side sweep.
  - Entry: at the gap.
  - Stop: 0.2% under the sweep's wick.
  - Target: the next untaken buy-side level.
  - It only counts as "pays after fees" when it still nets **at least 1.5R and 2%** after both fees.
- **Rank:** mixes an active setup, a recent sell-side sweep, the 4h trend (20 vs 50 EMA), oversold RSI on Tier-1 coins (Kayden's dip rule: RSI under 30), daily range and 24h volume.

## Paper trades

$7.50 each (fee taken out), at most 2 open, one per coin, and no re-opening a coin on the same day. Exits trigger when a 15-minute candle touches the stop or the target. P&L is recorded after fees. Open paper trades get their own profit wheel on the [[Trading OS page]].

## Alerts (each starts with its Eastern time)

- **Pushed to phone:**
  - new setups
  - sweeps of PDH/PDL
  - Tier-1 RSI under 30
  - 24h moves of 5% or more
  - paper opens and closes
- **Logged only (Alert log, not pushed):** sweeps of 1-hour swing highs and lows.
- **Quiet hour:** `[9:30 PM ET] No new crypto alerts, sir. Top-ranked: BTC at 84,821 (4h trend up).`

## First scan (2026-10-01, 7:41 PM ET)

BTC ranked #1 (4h uptrend; RSI 1h 61 / 4h 59; buy-side liquidity at 85,244, sell-side at 83,107). 17 sweeps across the 10 coins in the prior 24 hours. No sweep + FVG setups.

## Where things live

- Its state, paper trades and alerts are in the [[Trading OS page]] database (`crypto/scan`, `crypto_trades`, `alerts`, `log`).
- The scanner script itself is stored inside the scheduled task's prompt.
- The Daily Market Brief reads this scan for its crypto section.
