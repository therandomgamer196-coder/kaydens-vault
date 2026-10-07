---
tags: [trading, auto-trader, robinhood, notes]
date: 2026-09-30
---
# Trading Bot: Session Notes (2026-09-30)

Part of [[Trading OS]]. The current rules live in [[Auto-trader]].

> [!info] Summary
> The $15 auto-trader in the Agentic Robinhood account (••3001) is live and fully automatic. It runs hourly on weekdays at :50 past the hour, 9:50 AM–3:50 PM ET, and logs everything to the Trading OS page.

## Setup
- **Account:** Agentic (••3001) only. Never touches Main or the Bitcoin Cash holding.
- **Capital:** $15 plus realized P&L. $7.50 per trade, max 2 open, long only.
- **No options, shorting or margin.** Crypto is watch/paper only because the fee is 0.95% each way.
- **Dashboard:** Trading OS artifact (claude.ai), which holds the bot ledger (state, trades, markets, log).

## Strategies
| Market | Strategy | Entry | Stop / Target | Exit |
|---|---|---|---|---|
| USO (oil), GLD (gold) | 4h trend | 20 EMA > 50 EMA and price above the 20 EMA | −1% / +2% | Stop, target, or 20 EMA crosses under the 50 |
| QQQ, SPY | 15m fair value gap | Price pulls back into a live bullish gap from today (9:45 AM–2:50 PM) | 0.1% under the gap / 2R | Stop, target, or the 3:50 PM check |

- Only one of QQQ/SPY open at a time. No re-entering a market on the same day after exiting it.
- **Day-trade guard:** max 2 same-day round trips per 5 business days (the PDT limit is 4).

## Exits (asked "when are you exiting trades")
- Exits only happen at the hourly checks. There are no resting stop orders at Robinhood, so a fast move can fill past the stop.
- FVG trades are always flat by the 3:50 PM check. Trend trades can be held overnight or for days.

## Alerts (added today)
- **Every new trade** gets Robinhood alerts: price below stop, price above target, plus:
  - Trend trades: price below the 1-hour 80 EMA (about the 4h 20 EMA; Robinhood alerts have no 4h bars or EMA crossover).
  - FVG trades: price below the gap bottom ("gap failing").
- Alerts are deleted when the bot sells.
- **Bot push messages:**
  - "**We hit big, sir**" when a trade is ≥ halfway to its target, or sold at a profit.
  - "**We gotta get outta this one, sir**" when a trade is ≥ halfway to its stop, or sold at a loss.
  - Each fires once per trade.

## Watchlist (monitor only, added today)
| Symbol | Reading at 1:22 PM ET |
|---|---|
| NVDA | Uptrend: 20 EMA 222.72 > 50 EMA 217.92, price 230.35 |
| GOOGL | 20 EMA 343.67 < 50 EMA 345.63, but price 350.54 is above both; a bullish cross may be close |
| MSFT | Strong uptrend: 20 EMA 499.50 > 50 EMA 479.27, price 516.78 (stretched 3.5%) |
| PLTR | Uptrend: 20 EMA 180.48 > 50 EMA 168.75, price 188.20 |
| ETH | 2,685 (+0.5% on the day) |
| BTC | 84,084 (paper only; breakout level 85,613) |

The bot pings you when a watchlist stock's 4h 20/50 EMA crosses, or when ETH/BTC moves 5%+ in a day.

## Trades today
| Trade | Entry | Qty | Stop | Target | Status |
|---|---|---|---|---|---|
| USO 4h trend (12:12 PM) | 147.16 | 0.050966 | 145.68 | 150.10 | Open, about 146.72 at 12:50 PM |
| SPY 15m FVG (12:51 PM) | 768.01 | 0.009765 | 766.52 | 770.99 | Open, out by 3:50 PM |

- Bot equity at 12:51 PM: **$14.98**, cash $0, realized P&L $0.

## Open ideas
- [ ] Decide whether any watchlist stock should become tradable (only USO/GLD/QQQ/SPY trade now).
- [ ] Tune the "significant move" threshold (currently halfway to stop/target).

## TradingView charts
Tradable: [USO](https://www.tradingview.com/chart/?symbol=AMEX%3AUSO) · [GLD](https://www.tradingview.com/chart/?symbol=AMEX%3AGLD) · [QQQ](https://www.tradingview.com/chart/?symbol=NASDAQ%3AQQQ) · [SPY](https://www.tradingview.com/chart/?symbol=AMEX%3ASPY)

Watchlist: [NVDA](https://www.tradingview.com/chart/?symbol=NASDAQ%3ANVDA) · [GOOGL](https://www.tradingview.com/chart/?symbol=NASDAQ%3AGOOGL) · [MSFT](https://www.tradingview.com/chart/?symbol=NASDAQ%3AMSFT) · [PLTR](https://www.tradingview.com/chart/?symbol=NASDAQ%3APLTR) · [ETH](https://www.tradingview.com/chart/?symbol=COINBASE%3AETHUSD) · [BTC](https://www.tradingview.com/chart/?symbol=COINBASE%3ABTCUSD)
