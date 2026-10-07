---
tags: [trading, guide]
aliases: [Setup guide, How my trading setup works]
created: 2026-10-04
updated: 2026-10-04
summary: Plain-English guide to every part of Kayden's trading setup, with each strategy's backtest (Oct 4 2026) and a ranked list of improvement ideas.
---

# Trading setup guide

Part of [[Trading OS]]. Written Oct 4, 2026. Not financial advice: these are past results, not promises.

## The big picture

The setup has four layers:

1. **Eyes:** scanners pull prices from Robinhood, Yahoo and Coinbase.
2. **Brains:** the strategy rules decide whether a setup is there.
3. **Hands:** the $15 auto-trader places small real orders. Everything else is paper.
4. **Memory:** the Trading OS page, its database, your phone pings and this vault.

Every scheduled task wakes up, does one job, writes what it found to the page's database, and pings your phone.

## Your scheduled tasks, one by one

| Task | When (ET) | Real money? | What it does |
|---|---|---|---|
| Auto-trader ($15) | Weekdays, every hour at :50, 9:50 AM to 3:50 PM | **Yes**, Agentic only | Runs the oil/gold trend, QQQ/SPY gap and live board strategies; sets Robinhood alerts; sends callouts |
| Probability board refresh | Every night, 8:20 PM | No | Re-scores 18 markets on 2 years of history; pings when a proven setup fires |
| Trinity paper trader | Weekdays, 4:25 PM | No | Replays the day's NQ/ES 1-minute candles through the Trinity model and logs a paper trade |
| Crypto 24/7 monitor | Every hour | No (paper) | Scans 10 coins for liquidity sweeps and gap setups; paper-trades them after fees |
| Daily Market Brief | Weekdays, about 8 AM | No | Macro, levels and crypto summary |
| Watchlist curator | Daily, 4:58 PM | No | Adds held and flagged symbols to your Robinhood watchlist |
| Weekly edge review | Sundays, 6:52 PM | No | Week in review, fixes, one new money idea |

## The strategies, explained

### 1. Oil/gold trend (USO, GLD): real money

- **Idea:** ride a market that's already trending up.
- **The rule:**
  - On 4-hour candles, the 20-period average (EMA20) must be above the 50-period average (EMA50). That means the trend is up.
  - Price must be above the EMA20.
  - Buy $7.50.
- **Exits:** stop 1% below, target 2% above, or sell if the averages cross down.
- **Backtest, 2 years (Nov 2023 – Oct 2026):**
  - USO: 167 trades, 40% won, +34% total (+0.20% a trade).
  - GLD: 128 trades, 50% won, +64% total (+0.50% a trade).
  - Simply holding did better: USO +96%, GLD +106%.
- **Best variant tested:** stop 2%, target 4%.
  - USO: +0.56% a trade (96 trades).
  - GLD: +1.34% a trade (60 trades).
  - That's about 3 times more per trade, with fewer trades.

### 2. QQQ/SPY 15-minute fair value gap: real money

- **Idea:** after a strong push up, price often dips back into the "gap" it left and bounces.
- **A fair value gap (FVG):** three 15-minute candles where the third candle's low sits above the first candle's high.
- **The rule:**
  - Buy when price is back inside a live gap.
  - Stop just under the gap.
  - Target 2 times the risk (2R).
  - Close out by end of day.
- **Backtest, 59 sessions (Jul 13 – Oct 2):**
  - QQQ: 14 trades, 43% won, +4.6R.
  - SPY: 13 trades, 46% won, −6.8R.
  - Changing the target (1R to 3R) barely mattered. The hourly checks rarely catch the target, so most trades end at the stop or the close.
- **Status:** blocked since Sep 30 by the day-trade guard, which protects you from the pattern-day-trader rule.

### 3. Probability board: real money when a setup triggers live

- **Idea:** only take setups that have won more often than not in that market's own history.
- **Five setups are tested on 18 markets** (2 years of daily candles):
  - uptrend pullback
  - oversold bounce
  - prior-day low sweep
  - 20-day breakout
  - three red days in an uptrend
- **A setup counts as proven only if all of these hold:**
  - won at least 55% of 25+ past signals
  - beat the market's "any day" rate by 3+ points
  - held up in both halves of the history
- **Proven right now:**
  - GOOGL prior-day low sweep: 60.6% of 104 past signals.
  - ADA oversold bounce: 70.5% of 44, paper only because it's crypto.
- The bot buys these live, in the moment, within the $15 limits.

### 4. Trinity model (NQ/ES futures): paper

- **Steps:**
  1. An overnight 1-hour candle closes through a 1-hour gap. That sets the bias.
  2. Price tags a 1-hour gap without closing past its middle.
  3. NQ and ES disagree on making a new low or high (SMT).
  4. A 1-minute gap flips. That's the entry.
- **Backtest on 1-minute candles, 19 sessions:** 6 trades, 3 won.
  - 2R target: +2.4R (+$63 on 1 micro).
  - ES did better than NQ.
- **Status:** far too few trades to trust yet. It's paper-traded every day.

### 5. Crypto 24/7 sweeps: paper

- **Idea:** after price "sweeps" an old high or low and snaps back, it often runs to the other side.
- **Research:**
  - 138 trades lost an average of −3.12R after the 0.95% fee each way.
  - BTC-confirmed alt sweeps reached the other side 52.8% of the time (36 cases) vs 16.1% without confirmation.
- **Status:** stays on paper until there's a lower-fee venue.

### 6. NQ sweep vs break (your manual trading)

- After a **sweep** of the overnight high or low, price reached the opposite extreme 41.5% of the time (241 cases).
- After a **break**, it did so only 14.3% of the time (244 cases).
- Use this as a bias filter at the open. See [[Liquidity sweep plan]].

## Ideas to improve profit and effectiveness

**Evidence-backed** (real-money changes need your OK):

1. **Widen the oil/gold brackets to stop 2% / target 4%.** It earned about 3 times more per trade in the 2-year test.
2. **Move SPY gap trades to paper.** −6.8R over 13 trades, and QQQ is the only positive gap market.
3. **Unblock QQQ gaps.**
   - Avoid same-day manual exits.
   - Or switch the Agentic account to a cash account, where the pattern-day-trader rule doesn't apply.
4. **Use real stop orders at Robinhood** instead of hourly checks, if they're allowed on fractional shares. Stops would then hit at the right price, not up to an hour late.
5. **Size is the profit lever.** At $7.50 a trade, a win is cents. Every $1,000 per trade adds about $0.50–$5 per trade in expectation, depending on the strategy. Only raise it after the live results match the backtests.
6. **Fix the crypto monitor:**
   - Paper entries come in hours late. Only enter while price is still in the gap.
   - Run it every 3 hours overnight to save usage.

**System and effectiveness:**

7. **Add a circuit breaker:** pause the bot after 2 losses in a day, or a −$1 day.
8. **Weekly scorecard:** live vs backtest for every strategy, so weak ones get cut fast.
9. **Run the Daily Brief on Eastern time.** It's on UTC now, so it will show up at 7 AM after Nov 1.
10. **Point the Oct 16 pattern review at the Trading OS ledger.**
11. **Slow the page's polling after hours** to cut wasted Robinhood calls.
12. **Combine signals:** only take Trinity or gap trades in the direction of the sweep/break bias.
13. **Secure the laptop:** full virus scan, and remove the game-unlocker tools. Your trading accounts are logged in on it.
14. **Better data later:** Yahoo's free data is delayed and keeps only 30 days of 1-minute candles. A broker data feed would allow longer, cleaner tests.
15. **Run Coin check** on any new coin before it gets near a list.

## Applied 2026-10-04

Kayden approved all 15 ideas. Status:

| Status | Ideas |
|---|---|
| **Done** | 1 wider trend brackets · 2 SPY FVG to paper · 5 circuit breaker · 7–8 stricter crypto entries and new schedule · 9 weekly scorecard · 10 Trinity sweep/aligned tags · 11 brief at 7:52 · 12 Oct 16 review repointed · 13 off-hours polling (page v9) · 14 Hydra and LuaTools removed, full scan started |
| **Kayden** | 3 switch Agentic to a cash account in the Robinhood app |
| **Not possible** | 4 real stops on fractional shares (market orders only) |
| **Later** | 6 bigger size once live results match the backtests · 15 paid data feed |

Details: [[Trading OS change log]].
