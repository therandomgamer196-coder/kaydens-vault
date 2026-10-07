---
tags: [trading, plan, research]
aliases: [sweep plan, liquidity sweeps plan]
created: 2026-10-01
updated: 2026-10-01
status: growing
summary: Plan to catch higher-quality liquidity sweeps - backtest results so far, the 3-step plan, open decisions and the background research study.
---

# Liquidity sweep plan

Part of [[Trading OS]]. Kayden asked (2026-10-01) for a plan to get better liquidity sweeps into our setup, and to study the most popular coins' charts to understand how the market works. Terms are in [[Trading glossary]].

## Backtest results so far (2026-10-01)

> [!note] Small samples
> These are first reads, not proof. Each idea needs at least 30 trades before it changes a real-money rule.

**QQQ / SPY, 15-minute, 59 sessions (Jul 10 – Oct 1)**

| Test | QQQ | SPY |
|---|---|---|
| Current FVG rule, hourly checks (how the bot runs) | 14 trades, 43% win, **+4.6R** | 13 trades, 46% win, **−6.8R** |
| FVG only after a sell-side sweep, hourly checks | 4 trades, 0% win, −3.0R | 3 trades, −2.3R |
| Resting limit at the gap + bracket exits | 37 trades, +3.2R | 27 trades, −6.3R |
| Sweep filter + limit/bracket | 12 trades, +0.2R | 8 trades, −2.0R |

The sweep filter (prior-day low, pre-market low or an intraday swing low) **did not improve** the current setup. QQQ's plain FVG rule has been positive; SPY's has lost money.

**Crypto, 15-minute, 30 days (BTC, ETH, SOL)**

| Test | BTC | ETH | SOL |
|---|---|---|---|
| FVG only, 2R, before fees | 52 trades, +12.1R | 81 trades, −4.6R | 81 trades, −6.6R |
| Sweep + FVG, 2R, before fees | 14 trades, −5.4R | 16 trades, −0.1R | 23 trades, 48% win, **+6.9R** |
| Same, **after 0.95% per side** | every variant loses | every variant loses | every variant loses |

Why it loses: typical risk per trade was only 0.4–1.3%, so the 1.9% round-trip fee is bigger than the whole stop. The follow-up research (below) also tested swing-size targets of 4% or more, and those lost too. Cheaper execution (a venue with ~0.1% fees) is the only clear fix.

## The plan

1. **Measure (running now):** the [[Crypto 24-7 monitor|Crypto 24/7 monitor]] logs every sweep and paper-trades sweep + FVG setups with fees. The background research study finished at 8:48 PM on 2026-10-01 (results below).
2. **Decide with evidence:** after the research and at least 30 trades per idea, compare each idea against the current rules.
3. **Change one rule at a time,** only with Kayden's OK for anything that touches real money. Log the date in [[Trading OS change log]], then compare the 20 trades before and after.

## Open decisions

- [ ] Move SPY 15m FVG entries to paper only and keep QQQ (SPY −6.8R over 13 trades).
- [x] NQ at the open: test "sweep → displacement → 5m FVG". Tested 2026-10-01: it didn't beat plain FVGs. Sweep vs break works better as a bias filter (see results below).
- [x] Crypto swing setups (target 4%+, 4h uptrend): tested 2026-10-01. None clear the fees, so crypto stays paper only.
- [ ] Use sweep vs break as a bias filter in Kayden's own NQ open playbook.
- [ ] Tag "BTC-confirmed" alt sweeps in the crypto monitor.
- [ ] Test Robinhood's market-maker routing cost against the 0.95% fee.

## Research results (finished 2026-10-01, 8:48 PM ET)

From the one-time "Liquidity sweep market research" task. The full report is in the Research panel on the [[Trading OS page]] (database `research/sweep-study-20261001`).

> [!summary] TL;DR
> - **A sweep is information, not an entry.** After a sweep, price reaches the opposite side 2–3x more often than after a break.
>   - NQ overnight high/low, 2 years: 41.5% (n=241) vs 14.3% (n=244).
>   - Crypto prior-day high/low: 25.9% (n=214) vs 14.4% (n=187).
> - **Crypto swing trades can't beat the 1.9% round-trip fee.** 138 trades: −0.17R gross, −3.12R net per trade. No variant was positive even before fees.
> - **BTC confirmation matters on alts.** When BTC swept the same prior-day level within 2h, the alt reached the opposite level 52.8% of the time (n=36), vs 16.1% without (n=139).
> - **The 5m sweep → FVG model didn't beat plain FVGs** on NQ (−1.77R over 15 vs −0.80R over 35) or QQQ (−1.73R over 12 vs −3.66R over 43). Samples are tiny (49–59 sessions).

### How crypto liquidity behaves (90 days; BTC, ETH, SOL, XRP, DOGE)

- 53.7% of first touches of a level were sweeps (1,217 touches).
- Sweeps are shallow: median 0.18% past the level, 75th percentile 0.31%. 46.5% went past 0.2%, so stops belong **under the sweep wick**, not at the level.
- After a sweep, the median move in your favour (1.39%) and against you (1.41%) over 24h are nearly equal. A sweep doesn't predict direction by itself; it tells you where price may travel next.
- Sweep share by session (ET): Asia 57.6%, London 56.0%, New York 52.4%, late 4–8 PM 40.6%. The quiet late session mostly produces real breaks.

| Level swept | Sweeps | Reach opposite in 24h | in 48h | Median depth |
|---|---|---|---|---|
| Asia high/low | 313 | 56.2% | 69.2% | 0.15% |
| Prior-day high/low | 214 | 25.9% | 42.7% | 0.21% |
| Equal highs/lows | 127 | 26.2% | 38.7% | 0.19% |

### NQ at the open

- **2 years of NQ 1h data (577 sessions):** after the first 9–11 AM touch of the overnight high or low, a sweep sent price to the opposite overnight extreme by 4 PM **41.5%** of the time (n=241). A break did so **14.3%** of the time (n=244).
- **5m, 49 sessions, 8:30–11:00 AM:** 80 sweeps vs 43 breaks. 62% of first touches came between 9:30 and 9:45, and the 8:30 news candle was the other cluster.

| Market | Model | Trades | Win % | Total R |
|---|---|---|---|---|
| NQ | Sweep → 5m FVG, 2R | 15 | 26.7 | −1.77 |
| NQ | Sweep → 5m FVG, opposite liquidity | 11 | 27.3 | +0.06 |
| NQ | FVG only 5m, 2R | 35 | 37.1 | −0.80 |
| QQQ | Sweep → 5m FVG, 2R | 12 | 33.3 | −1.73 |
| QQQ | Sweep → 5m FVG, opposite liquidity | 9 | 22.2 | +1.05 |
| QQQ | FVG only 5m, 2R | 43 | 34.9 | −3.66 |

### Recommended changes (ranked by evidence)

1. **Sweep-vs-break bias filter for the NQ/QQQ open.**
   - After a **break** of the overnight high or low, skip FVGs that fade it and only take FVGs in the break's direction.
   - After a **sweep**, favour FVGs pointing toward the opposite overnight extreme and target that extreme. (41.5% vs 14.3%, n≈240 each.)
2. **Keep crypto paper only.** Fees cost about 2.9R per trade at 0.84% average risk, and the median target sits only 1.6% away. A low-fee venue (~0.1%) would help more than any filter.
3. **Crypto monitor: tag "BTC-confirmed" alt sweeps** (BTC swept the same prior-day level in the same hour or up to 2h before) and rank them higher. (52.8% vs 16.1%.)
4. **Stops under the sweep wick, not at the level.**
5. **Watch only:** shorts after buy-side sweeps at the open looked better than longs (NQ +1.58R over 6 vs −3.35R over 9; QQQ +3.27R over 4 vs −5.00R over 8). That's too few trades for a rule.

### What NOT to change

- Don't make "must follow a sweep" an entry requirement on the $15 auto-trader. It cut trades about 70% with no reliable gain.
- Don't switch the auto-trader from 15m to 5m FVGs.
- Don't add a 4h trend filter to crypto sweep longs. It made results worse (−0.291R over 83 vs +0.019R over 55).
- Don't require crypto targets of 4% or more. Only 10 setups qualified, and none won.

> [!warning] Caveats
> Yahoo only serves 60 days of 5m data, so every 5m model has 9–43 trades. Only the 2-year NQ 1h check and the crypto event counts are real samples. Look-ahead was avoided: sweeps count only after the confirming close, and only levels known at entry are used.
