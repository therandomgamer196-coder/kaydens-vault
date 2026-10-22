# Z.E.R.O / Trading OS: instructions for coding agents (VS Code)

You are helping Kayden build **Z.E.R.O**, his automated trading setup, from VS Code on his Windows laptop (HP Victus, RTX 4050 6 GB, i5). Claude (on claude.ai) runs the live system. You work on code, research and notes alongside it. Read this whole file before doing anything.

## Talk to Kayden like this
- Call him "sir". Start every alert or status line with Eastern time in brackets, e.g. `[10:50 AM ET]`.
- Plain English, short. Give honest numbers: sample size (n), results after fees, and say when a result could be luck.
- End anything about trades with "Not financial advice."

## The goal
Reach $1,000 from trading, then $10,000, with no deadline, ideally $5+ profit per trade. Only use strategies with evidence. Never risk more to chase the goal.

## How the system works
- **Live system (Claude only):** scheduled tasks on claude.ai trade Robinhood and write to the Trading OS page database (https://claude.ai/artifact/QQnc8KJpphMajt9zfY4BLQ). **You can't reach Robinhood, the page database or the scheduled tasks.** Hand that work to Claude (see Handoff).
- **The brain:** this repo is Kayden's Obsidian vault (`brain/`). On the laptop it is `C:\Users\NCG\OneDrive\Desktop\Kaydens Vault\`. It syncs to GitHub `therandomgamer196-coder/kaydens-vault` (branch `main`). Cloud agents pull and push it too, so always pull before you edit and push soon after.
- **Code:** `trading-os-code/` holds copies of every engine script (exported 2026-10-21). The live versions are stored in the page database. Claude uploads your changes after review. The laptop also has `C:\Users\NCG\Documents\Trading OS\code\` (the page HTML and older scripts, plus its own `CLAUDE.md`).

Read these notes first:
1. `brain/Trading OS/ZERO trading agent.md`: system map, every agent, schedules, rules
2. `brain/Trading OS/Strategy scorecard.md` and `brain/Trading OS/Strategies/`: each strategy, backtest, live record
3. `brain/Trading OS/Pending scheduled-task changes.md`: what is approved but not applied yet
4. `brain/Trading OS/Trading OS change log.md`: newest first
5. `brain/Trading OS/Lab/Playbook.md` and `Lab/Ideas.md`: promotion gates and ideas
6. `brain/Trading OS/Trading setup guide.md` and `Trading glossary.md`: background

## Scripts in `trading-os-code/`
| File | Live database doc | What it does | Run |
|---|---|---|---|
| `edge_scan.py` | edge_code/scan_py | Probability board: ~22 markets, 2 years daily bars, which setups win | `python edge_scan.py out.json` |
| `crypto_scan.py` | crypto_code/scan_py | hourly crypto liquidity and board-hit scan | `python crypto_scan.py open.json edge_dir > scan.json` |
| `coincheck.py` | crypto_code/coincheck_py | meme coin rug and holder-concentration check | `python coincheck.py > cc.json` |
| `fvg.py` | bot_code/fvg_py | QQQ/SPY 15-minute fair-value-gap finder | `python fvg.py` |
| `m5_engine.py` | m5_code/engine_py | 5-minute setup search (70/30 train/unseen split) | `python m5_engine.py out.json` |
| `lab_engine.py` | lab_code/engine_py (v1.5) | Ultron's evolving paper strategies | `python lab_engine.py --state s.json --open o.json --ctx ctx --out out --gens 1` |
| `trinity_engine.py` | trinity_code/engine_py | Trinity NQ/ES 1-minute paper model | `python trinity_engine.py today out.json .` |

They use free public data (Yahoo chart API, Coinbase Exchange API, RugCheck, GoPlus). Python 3, standard library only, so keep it that way.

## Hard rules (never break them)
1. **No real orders from you, ever.** Only Claude's scheduled tasks trade, and only in the one Robinhood account the bot is allowed to use (now ••3001). Never put account numbers, API keys, passwords or tokens in code or notes.
2. **Real-money rule changes need Kayden's explicit OK.** That covers sizes, limits, symbols, strategies and the switch from paper to real. Write the proposal into the Handoff and let Kayden decide. Paper-side and research work is fine.
3. **Current real-money rules** (source of truth: database `config/rules`):
   - Long only, spot only. No options, shorts or margin.
   - $25-$30 per position, at most 50% of the account in one position. At $500+ switch to 2% risk per trade.
   - At most 2 open stock trades and 2 open real crypto trades, one per symbol.
   - Circuit breaker: no new entries after −8% of capital in a day or 2 losing trades.
   - Pattern-day-trader guard on margin accounts under $25k.
   - Crypto costs 0.95% each way (1.9% round trip). Real crypto only copies Probability-board paper trades.
   - Meme coins need a daily coin check of OK.
   - SPY 15m FVG, crypto sweep, Lab strategies and Trinity are paper only.
4. **Promotion gates.** A strategy reaches the Playbook and real money only after all of these:
   - a cited source;
   - a backtest on 2+ years with costs;
   - an out-of-sample pass;
   - 30+ forward paper trades, positive after costs;
   - no single lucky cluster of dates;
   - Kayden's OK.
   Social media, forums and videos are idea sources only.
5. **Testing.** Test every change with real data. Use fake open trades to test exits. Never show tiny prices in e-notation (meme coins are under $0.01, so keep 6 significant figures). Keep a `.bak` copy of the file you change.
6. **Vault safety.**
   - Never read, edit or commit anything in `.obsidian/`. `.obsidian/plugins/obsidian-local-rest-api/data.json` holds a key. It should be untracked and rotated; only Kayden does that, on the laptop.
   - Don't move or rename notes outside Obsidian, because that breaks `[[wikilinks]]`.
   - Never delete notes.
7. JARVIS voice assistant stays disabled. No broad searches of the home folder; use exact paths.

## How to work
1. `git pull`. Read the notes above.
2. Make the change in `trading-os-code/` (or a new script there), test it locally, and keep it small.
3. Note what you did in the brain, using Obsidian markdown: YAML frontmatter (`tags`, `type`, `created`, `updated`, `summary`), `[[wikilinks]]`, ISO dates, newest first.
   - Add a dated section to `brain/Trading OS/Trading OS change log.md` if behavior changed.
   - Add one line to `brain/Work log.md`: `- YYYY-MM-DD HH:MM ET: VS Code: <what> [[Note]]`.
   - Update the matching `Strategies/<name>.md` or `Lab/Ideas.md`.
4. Hand off anything Claude must do (upload a script, change a task, anything touching Robinhood) by adding an item to `brain/Trading OS/Handoff to Claude.md`: date, what, which file, how you tested it, and whether it changes real-money behavior.
5. Commit with a clear message, pull with rebase, and push.

## Open work you can pick up (2026-10-21)
- **Local models:** set up Ollama with a 7-8B model (Q4 fits 6 GB VRAM) and an Obsidian plugin (e.g. Smart Connections) so local models can search the brain. Use them for summaries and search, not trade decisions. Free disk space on C: first (it was ~5-6% free).
- **Lab research helpers:** scripts that pull public research (arXiv, blogs with numbers) into `Lab/Ideas.md` as "idea only".
- **Backtest harness:** one shared, cost-aware backtest module the board, Lab and 5m engine can all use. It must report n, win %, expectancy after costs, out-of-sample results and the number of variants tested.
- **Watcher prototype:** a script that checks prices every 5 minutes for proven setups and writes "setup firing" to a file. Claude will decide later how it hands off to the trader. Testing only, no orders.
- **Fix the laptop vault sync** (last pushed 2026-10-07) and **Hermes** (`hermes pm repair`).
- Make the scripts timezone-safe (some use deprecated `utcfromtimestamp`).

## Handoff to Claude
`brain/Trading OS/Handoff to Claude.md`. Claude reads it and applies or uploads items, then marks them done.
</content>
</invoke>
