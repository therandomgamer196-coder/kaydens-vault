---
tags: [trading, index]
aliases: [Trading OS, trading desk, Robinhood trading OS]
created: 2026-09-30
updated: 2026-10-21
summary: Kayden's trading desk - live Robinhood dashboard, $15 real-money auto-trader, 24/7 crypto liquidity monitor and the research loop.
---

# Trading OS

Kayden's trading desk. It has four parts:
- a live Robinhood dashboard on claude.ai
- a $15 auto-trader that trades real money in the Agentic account
- a 24/7 crypto liquidity monitor (paper only)
- a research loop that tests setups before any rule changes

> [!important] Read before changing anything
> Read this folder first. Every alert carries its Eastern time, like "[10:50 AM ET]". Real-money rules only change with Kayden's OK, one change at a time, logged in [[Trading OS change log]].

## Open it

| What | Link |
|---|---|
| Trading OS page | https://claude.ai/artifact/QQnc8KJpphMajt9zfY4BLQ |
| Jarvis Console (Trading OS card + top-bar link) | https://claude.ai/artifact/EZUPMFpGmNqWZ9dDBEH6zE |
| First paper test ($15 Paper Desk) | https://claude.ai/artifact/93XKW9X4EkUSDXE1CL2muM |

## Notes

> [!info] Current setup (2026-10-21)
> The $15 bot became **Z.E.R.O** on 2026-10-15/16. Start with [[ZERO trading agent]] (system map and rules), [[Strategy scorecard]], [[Pending scheduled-task changes]] and [[Handoff to Claude]]. Coding agents: [[VS Code agent brief]].

- [[Trading OS page]]: layout, every panel, the database it reads, how to update it safely
- [[Auto-trader]]: the real-money $15 bot (rules, schedule, alerts, authorization)
- [[Crypto 24-7 monitor|Crypto 24/7 monitor]]: hourly liquidity scan of 10 coins, paper trades, fee math
- [[Liquidity sweep plan]]: the optimization plan, test results so far, open decisions
- [[Trading glossary]]: plain-English meanings of FVG, sweep, liquidity, R, EMA, RSI, PDT
- [[Trading OS change log]]: dated record of every change
- [[Optimization review 2026-10-02]]: what limits output, ranked fixes, and the decisions waiting on Kayden
- [[Trading setup guide]]: plain-English guide to every strategy and task, the Oct 4 backtests, and improvement ideas
- **Claude Code project:** `C:\Users\NCG\Documents\Trading OS`. Its `CLAUDE.md` holds the full context and rules.
- [[Trading bot session notes 2026-09-30]]: the auto-trader's first day
- [[Bitcoin trading agent plan]]: earlier draft plan for a dedicated BTC bot (Freqtrade)

## Scheduled tasks

| Task | When (ET) | What it does | Real money? |
|---|---|---|---|
| Trading OS auto-trader ($15) | weekdays at :50, 9:50 AM–3:50 PM | Live: USO/GLD 4h trend (−2%/+4%), QQQ FVG and real-time Probability board entries. Paper: SPY FVG. Daily circuit breaker. | Yes, Agentic account only |
| Crypto 24/7 monitor (paper) | :44 past 2 AM, 5 AM and 7 AM–11 PM | scans 10 coins, flags sweeps, paper-trades setups that still clear the fee | No |
| Daily Market Brief | weekdays 7:52 AM | macro + technical brief; crypto section reads the monitor's scan | No |
| Trinity paper trader (NQ/ES, 1-minute) | weekdays 4:25 PM | runs the Trinity engine on the day's 1-minute data, logs paper trades | No |
| Probability board refresh | nightly 8:20 PM | re-tests every setup's odds per market | No |
| Watchlist curator | daily 4:58 PM | keeps the watchlist current | No |
| Weekly edge & opportunity review | Sundays 6:52 PM | scorecard of live results vs backtest benchmarks | No |
| Liquidity sweep market research | one time, Oct 1 (done) | deep sweep study, saved to the page's Research panel | No |
| 30-Day Trading Pattern Review | one time, Oct 16, 9 AM | honest review from the Trading OS ledger and Robinhood history | No |

All of them push to Kayden's phone and start every line with the Eastern time.

## October goal (set 2026-10-01, 10:20 PM ET)

**$1,000 from trading by Oct 31.** There's a progress bar at the top of the [[Trading OS page]]. It counts closed-trade profit since Oct 1 in both Robinhood accounts, plus outside trades (like NQ futures) added on the page.
- About **$48 per trading day** is needed (21 trading days left after Oct 1).
- The $15 bot alone can't reach it: a 2R win on a $7.50 QQQ trade is about $0.02.
- The best candidate is NQ/MNQ at the open. In the last 50 sessions, the median first 15m FVG stop was 28.5 pts ($57 per MNQ) and the median 9:30–11:00 range was 236 pts.

## Key facts

- **Accounts:** Main (the default account, read-only to Claude) and Agentic (••3001, the only account the bot trades). The Bitcoin Cash in Agentic is never touched.
- **Crypto fee in Agentic:** 0.95% each way (1.9% round trip). That's why crypto is paper only.
- **Risk rules:** hard stop on every trade; 1–2% of equity max per setup.
- **Claude skill:** "kayden-trading-desk" (proposed 2026-10-01) gives Claude the same rules in any session.
- **Related:** [[About Kayden]], [[Jarvis Brain]], and the NQ research platform (Python, 5 phases) on the HP Victus.
