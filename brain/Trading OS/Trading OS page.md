---
tags: [trading, dashboard]
aliases: [Trading OS dashboard, trading dashboard]
created: 2026-09-30
updated: 2026-10-01
summary: The Trading OS claude.ai page - look, every panel, the database collections it reads, and how to update it without losing changes.
---

# Trading OS page

Part of [[Trading OS]]. A claude.ai artifact: https://claude.ai/artifact/QQnc8KJpphMajt9zfY4BLQ. Live data comes from Kayden's Robinhood connection and refreshes every minute while the page is open. The first time it asks, allow Robinhood for the page.

## Look

A neon-green circuit board on near-black, based on the FXNX "Trading Operating System" images Kayden shared (2026-09-30). A chart module is wired through a glowing central **sync chip** to **Data Flow** (left) and **Execution** (right). Pick a symbol anywhere and the traces light up and sync all three.

## Panels, top to bottom

| Panel | Shows |
|---|---|
| Top bar | ET clock, market session, Agentic / Main account switch |
| Account strip | total, cash, buying power, stocks, crypto, open P&L, auto-trader equity |
| Open trades | one card per position with a **profit wheel** that fills from stop toward target, green in profit, red under water; paper crypto trades are tagged "Paper" |
| Chart | 5m / 15m / 1h / 1D candles; resistance and support (last 30 candles), live FVG zones, prior close, bot entry/stop/target; tap the chart to set entry, stop or target |
| Data flow: Markets | indexes, ETFs, watchlist and crypto with sparklines; each row shows its strategy note with an "as of" time, plus its latest alert and when it fired |
| Data flow: Feed | bot checks, crypto scans, alerts, orders and session times, each with time and day |
| Data flow: Alerts | Robinhood price and indicator alerts, with when each was set |
| Execution | stock ticket (limit or market, shares from risk %), NQ/MNQ contract sizing, readiness ring (rules + 6-item checklist), Robinhood pre-trade preview (never places orders), copy order |
| Crypto 24/7 | 10 coins ranked: 4h trend, RSI, day range, volume, liquidity above and below, sweeps with times, setups; plus "How to read this board" |
| Research | the latest research report from the database |
| Auto-trader | bot equity, realized P&L, day-trade count, last check, recent checks |
| Alert log | every alert with its time; filter All / Stocks / Crypto |
| Recent orders, Rules | Agentic account orders; the auto-trader rules |

## Database (the artifact's own store)

| Path | Written by | Holds |
|---|---|---|
| `bot/state` | [[Auto-trader]] | mode, cash, equity, realized P&L, day_trades, note |
| `trades/<SYM-time>` | [[Auto-trader]] | live bot trades |
| `markets/<USO…PLTR>` | [[Auto-trader]] | readings, with `updated_at` |
| `crypto/scan` | [[Crypto 24-7 monitor\|Crypto 24/7 monitor]] | latest scan + keys of alerts already sent |
| `crypto_trades/<SYM-time>` | [[Crypto 24-7 monitor\|Crypto 24/7 monitor]] | paper trades |
| `alerts/<S…, C…, R…>` | every task | every alert: `t`, `time`, `src`, `level`, `text` |
| `log/<…>` | every task | one line per run (`src: crypto` for crypto runs) |
| `research/<id>` | research tasks | title, summary, markdown body, stats |

## Connections

Robinhood tools the page uses: accounts, portfolio, positions, quotes (stocks, crypto, indexes), orders, alerts, historicals and `review_equity_order` (preview only). The page never places an order.

## Updating it safely

1. Other sessions publish this page too. Read the live version first and merge onto it. A publish built on an old copy is refused.
2. Keep a timestamp on every alert row.
3. Test before publishing: syntax-check the script, then render it once headless at desktop and phone width with mocked data. Then publish to the same URL.
4. Add an entry to [[Trading OS change log]].
