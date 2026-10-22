---
tags: [trading, zero, moc]
type: moc
aliases: [Z.E.R.O, ZERO, ZERO system map, Trading OS system map]
created: 2026-10-21
updated: 2026-10-21
status: evergreen
summary: How Z.E.R.O works today - every agent, its schedule, what it may write, the rules it follows, and where the code lives. Read this first.
related: ["[[Trading OS]]", "[[Trading OS change log]]", "[[Pending scheduled-task changes]]", "[[VS Code agent brief]]"]
---

# Z.E.R.O trading agent: system map

Z.E.R.O is Kayden's 24/7 trading workforce. Goal: $1,000 from trading, then $10,000, no deadline, ideally $5+ per trade. It replaced the $15 / $7.50 setup on 2026-10-15 and 2026-10-16. Part of [[Trading OS]].

> [!important] Rules live in one place
> The page database doc `config/rules` (created 2026-10-21) is the single source of truth for accounts, sizing, limits, real-money strategies and the kill switch. Real-money rules change only with Kayden's OK and get logged in [[Trading OS change log]].

## Where things live
| What | Where |
|---|---|
| Trading OS page | https://claude.ai/artifact/QQnc8KJpphMajt9zfY4BLQ |
| Page database | the same artifact (ArtifactData; Claude only) |
| Engine code (copies) | `trading-os-code/` at the vault repo root; the live copies are in the database `*_code` docs |
| Brain | this vault, GitHub `therandomgamer196-coder/kaydens-vault` (main) |
| Broker | Robinhood. Only the account where the bot is allowed (now ••3001, limited margin). Z.E.R.O cash account planned. |

## The agents (scheduled tasks on claude.ai)
| Agent | Schedule (ET) | Money | Writes |
|---|---|---|---|
| Z.E.R.O auto-trader `trig_01LbEQv2FbVhFdv4fCUEjaNf` | :50, 9-15, Mon-Fri | **real** stocks | bot/state, trades, markets, alerts S*, log |
| Z.E.R.O crypto `trig_01D9UWzCtfrkTtoe25FBM15b` | :52 hourly, 24/7 | **real** crypto, copies board paper trades only | real_crypto, alerts CR*, log CR* |
| Z.E.R.O 5-minute scout `trig_01SddJ9YWtjxtkcaYaLv57Rj` | :47 hourly | alerts only (Auto OFF) | m5/state, real_m5, alerts M*, log M* |
| Crypto 24/7 monitor `trig_01VgDK5USXHFg9dktAsx5TPC` | :44 at 2, 5, 7-23 | paper | crypto/scan, crypto/coincheck, crypto_trades, alerts C*, log C* |
| Probability board `trig_017H77DyWdsTDnAeYcwEzVu7` | 8:20 PM nightly | info | edge, alerts E* (**disabled since Oct 7; re-enable pending**) |
| Lab / Ultron `trig_01RFK6XbWVmLfUCXKU19QeEy` | :29 hourly | paper | lab, lab_trades, lab_chat, research, alerts L*, log L*, vault Lab/ |
| Trinity paper `trig_01VPy7mpgFQBXSTUsfZgktT1` | 4:25 PM Mon-Fri | paper | trinity_trades, alerts T*, log T* |
| Cloud Jarvis `trig_01NqYA4V8JFr4aboze1Km4Ki` | every 4h | none | vault Jarvis Notes/ |
| Watchdog, Scribe | planned | none | see [[Pending scheduled-task changes]] |

Disabled: Weekly edge review, Watchlist curator, Punch In syncs, Weekly laptop health check.

## Rules every agent follows
- Address Kayden as "sir". Every alert line starts with Eastern time, like `[10:50 AM ET]`.
- Real money only in the account with `agentic_allowed=true`. Look it up every run and show only the last 4 digits. Never touch any other account or any holding that isn't in a bot ledger.
- Long only, spot only. No options, shorts or margin.
- Sizing (2026-10-16): $25-$30 per position, at most 50% of the account in one position, never more than buying power. At $500+ switch to 2% risk per trade.
- Circuit breaker: no new entries after −8% of capital in a day or 2 losing trades.
- Pattern-day-trader guard on margin accounts under $25k: never the 4th day trade in 5 business days.
- Crypto costs 0.95% each way (1.9% round trip). Real crypto only copies Probability-board paper trades (approved "Trade crypto", 2026-10-16).
- Meme coins (PEPE, BONK, WIF, PENGU) trade only while the daily coin check says OK.
- Each agent writes only its own database docs and pins `if_version`.
- Paper only until promoted: SPY 15m FVG, crypto sweep, Lab strategies, Trinity. Promotion gates are in [[Playbook]].
- Never put account numbers, API keys or passwords in notes. Never touch `.obsidian/`.

## Strategy notes
See [[Strategy scorecard]] and each card in `Strategies/`.

## Known issues (2026-10-21)
- The vault's `.obsidian/plugins/obsidian-local-rest-api/data.json` (holds the Local REST API key) is tracked in git. Fix it on the laptop: rotate the key in the plugin, then `git rm --cached` that file and add it to `.gitignore`. A cloud agent must not do this, because a remote delete would remove the laptop's copy on the next pull.
- The laptop's own vault sync last pushed 2026-10-07. Check the sync job on the laptop.
</content>
</invoke>
