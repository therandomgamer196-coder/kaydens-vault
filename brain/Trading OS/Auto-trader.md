---
tags: [trading, auto-trader, robinhood]
aliases: [auto-trader, $15 bot, trading bot]
created: 2026-09-30
updated: 2026-10-01
summary: The $15 real-money Robinhood bot - authorization, schedule, strategies, day-trade guard, alerts and callout formats.
---

# Auto-trader

Part of [[Trading OS]]. A Claude scheduled task, "Trading OS auto-trader ($15)", that trades **real money** in the Robinhood **Agentic** account (••3001). Its first day is in [[Trading bot session notes 2026-09-30]].

> [!warning] Authorization
> Kayden chose fully automatic trading on 2026-09-30: no per-trade confirmation, Agentic account only. It never touches the Main account or the Bitcoin Cash holding, never trades crypto, and never uses options, shorting or margin. Changing any of this needs Kayden's explicit OK.

## Schedule

Weekdays at :50 past the hour, **9:50 AM to 3:50 PM ET** (7 checks a day). Each check reads the ledger in the [[Trading OS page]] database, handles exits, then entries, then writes everything back in one batch.

## Money rules

- Capital: $15 plus realized P&L. **$7.50 per trade**, at most 2 open, long only.
- Only one of QQQ/SPY open at a time. No re-entering a market on the same day after exiting it.
- **Day-trade guard:** at most 2 same-day round trips in any 5 business days (pattern-day-trader protection; the limit is 4).

## Strategies

| Market | Strategy | Entry | Stop / target | Exit |
|---|---|---|---|---|
| USO (oil), GLD (gold) | 4h trend | 4h 20 EMA above the 50 EMA and the ask above the 20 EMA | −1% / +2% | stop, target, or the 20 EMA crossing under the 50 |
| QQQ, SPY | 15m fair value gap | price inside a live bullish 15m gap from today, 9:45 AM–2:50 PM | 0.1% under the gap / 2R | stop, target, or flat at the 3:50 PM check |

- A bullish FVG is candles A, B, C where C's low is above A's high, B closed green, and the gap is at least 0.05%. See [[Trading glossary]].
- Exits happen only at the hourly checks. There are no resting stop orders, so a fast move can fill past the stop.

## Watchlist (monitor only)

NVDA, GOOGL, MSFT, PLTR: the 4h 20/50 EMA reading goes to the Markets panel, and a fresh cross sends a watch line. Crypto moved to the [[Crypto 24-7 monitor|Crypto 24/7 monitor]] on 2026-10-01.

## Alerts

- Every new trade gets Robinhood alerts at the stop and the target, plus:
  - trend trades: the 1-hour 80 EMA
  - FVG trades: the gap bottom
- Those alerts are deleted when the bot sells.
- Push messages (each starts with its time):
  - `[10:50 AM ET] We hit big, sir: USO up +$0.14 (+1.9%) from 146.97.` (at least halfway to target, or sold at a profit)
  - `[2:50 PM ET] We gotta get outta this one, sir: …` (at least halfway to the stop, or sold at a loss)
  - `[1:50 PM ET] Watch: GOOGL 4h 20 EMA just crossed above the 50 (bullish).`
  - `[3:50 PM ET] No trades this check, sir.` plus bot equity and the nearest setup
- Every line is also saved to the `alerts` collection, so the [[Trading OS page]] shows it in the Markets rows, the Feed and the Alert log.

## Open decisions

- SPY's 15m FVG trades lost over the last 60 days (−6.8R over 13 trades). Move SPY to paper only and keep QQQ? See [[Liquidity sweep plan]].
- Should any watchlist stock become tradable?
