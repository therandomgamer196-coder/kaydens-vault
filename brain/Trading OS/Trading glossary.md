---
tags: [trading, glossary]
aliases: [trading terms, trading definitions]
created: 2026-10-01
updated: 2026-10-01
status: evergreen
summary: Plain-English definitions of the trading terms used across the Trading OS.
---

# Trading glossary

Plain-English meanings of the words used across [[Trading OS]].

## Price structure

- **Candle:** one bar of price for a time window (5m, 15m, 1h, 4h, 1D) showing its open, high, low and close. Green closed above its open; red closed below it.
- **Swing high / swing low:** a candle whose high (or low) is the highest (or lowest) of the candles on each side of it. The monitor uses 3 candles each side on the 1-hour chart.
- **PDH / PDL:** prior day's high and low. For crypto that's the UTC day; for stocks, the prior regular session.
- **Support / resistance:** a price area where buying (support) or selling (resistance) has held before. On the Trading OS chart it's the lowest low and highest high of the last 30 candles.

## Liquidity

- **Liquidity:** resting orders waiting at a price. Big players need it to fill large orders.
- **Buy-side liquidity:** sits **above** old highs: stop-losses from shorts, plus breakout buy orders. Price often runs up to take it.
- **Sell-side liquidity:** sits **below** old lows: stop-losses from longs. Price often dips to take it.
- **Equal highs / equal lows:** two swing points within about 0.1% of each other. Stops pile up there, so they're bigger targets.
- **Liquidity sweep:** price wicks through a liquidity level and then **closes back on the other side**. The orders got taken but the move past the level failed. A sell-side sweep can mark a low; a buy-side sweep can mark a high.
- **Break:** price **closes** beyond the level. The move is continuing, not failing.
- **Displacement:** a strong, fast candle in one direction, often right after a sweep. It usually leaves a fair value gap behind.

## Fair value gaps

- **Fair value gap (FVG):** a three-candle pattern where price moved so fast it left a gap. **Bullish FVG:** candle 3's low is above candle 1's high (candle 2 is the big green push). **Bearish FVG:** candle 3's high is below candle 1's low.
- **Live / unfilled gap:** no later candle has closed back through the gap. The bot buys pullbacks into live bullish gaps.

## Indicators

- **EMA (exponential moving average):** an average price that weights recent candles more. "4h 20 EMA above the 50 EMA" means the short-term trend on 4-hour candles is above the longer one, so it's an uptrend.
- **RSI (relative strength index):** 0–100 momentum gauge. Under 30 is oversold, over 70 is overbought. Kayden's crypto dip rule: buy Tier-1 alts only when RSI is actually under 30.
- **ATR / day range:** the average size of a candle's range. The crypto board shows the 14-day average daily range as a % of price.

## Risk and results

- **R:** one unit of risk, the distance from entry to stop. A 2R target is twice that distance above entry. "+4.6R" means the trades made 4.6 times the risk of one trade, in total.
- **Win rate / expectancy:** % of trades that made money / the average R per trade.
- **Fees:** the Agentic account's crypto fee is 0.95% per side, so a trade needs more than 1.9% just to break even.
- **PDT (pattern day trader):** 4 or more same-day round trips in 5 business days on a margin account under $25k gets restricted. The bot caps itself at 2.
- **Paper trade:** a simulated trade with virtual money, used to test a rule without risk.

## Futures (NQ)

- **NQ / MNQ:** Nasdaq-100 futures. NQ = $20 per point, MNQ (micro) = $2 per point.
- **Globex / overnight session:** futures trading from 6 PM to 9:30 AM ET. Its high and low are liquidity levels at the open.
- **8:30 data:** major US economic reports come out at 8:30 AM ET and often cause the first sweep of the day.
