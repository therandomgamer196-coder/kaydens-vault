---
tags: [jarvis, plan, roadmap]
aliases: [Jarvis agent plan, Autonomy plan]
status: planned
created: 2026-09-22
---

# Autonomous agent plan

**Goal:** say "Hey Jarvis, make the shift colour blue" or "show eight rows in Up next" and have the dashboard change within seconds. Jarvis works **fully on this laptop** with no Claude, OpenAI or other cloud AI, and uses this vault as his long-term memory.

> [!summary] Verdict
> **It's possible on the HP Victus, with one design rule:** Jarvis changes the dashboard through a small set of **typed, validated settings tools**. He doesn't rewrite the page's code. A local 7–8B model is good at choosing an action from a menu and filling in its values. It isn't reliable at editing an 82 KB, 1,788-line HTML file. New panels and layout rewrites stay "Jarvis drafts, Kayden approves" (Phase 7).

## Where things stand today (2026-09-22)

| Piece | Today | Gap for autonomy |
|---|---|---|
| Brain / model | `llama3.2` (3B) via Ollama `/api/generate`, called through a PowerShell subprocess; OpenAI listed as fallback (`JARVIS_LLM_PROVIDERS=ollama,openai`) | No tool calling; 3B too weak for reliable actions; the fallback is a cloud AI |
| Commands | `handle_command()` in `jarvis_bridge.py`: `open …`, time, close/stop; everything else goes to chat | No way to change anything on the dashboard |
| Memory | Prompt contains only the dashboard context snapshot | **Jarvis never reads this vault**. The vault is memory for Claude Code today, not for Jarvis |
| Dashboard | Settings are hard-coded in `punch-in-wallpaper.html` (see [[Dashboard UI and parameters]]); reloads when `punch-in-version.js` changes (≤ 2 min) | No config file to write to; no instant reload |
| Data | [[Dashboard sync]] is a **Claude** scheduled task at 7 AM | A third-party AI still produces the data |
| Speech out | Edge neural TTS sends the text to Microsoft's speech service. This is a speech service, not an AI | Optional: Piper TTS for fully offline speech |
| Known bug | Stuck `speaking:true` → room chatter is taken as commands ([[Maintenance]]) | **Must be fixed first.** An agent that can change things must not act on background talk |

## Target architecture

```
"Hey Jarvis …" → wake word → faster-whisper → router
   ├─ fast path (existing): open calendar, time, close …
   ├─ agent path (new): dashboard / remember / recall intents
   │     Ollama /api/chat + tools   ←  memory: vault search + Graphify neighbours + Safety rules
   │        └─ tool call → dashboard_control.py (validate → back up → write config → log)
   │                          └─ bridge pushes new config → page applies it live (≈1 s)
   │     "Change shift colour to blue — confirm?"  →  "confirm"  →  applied
   └─ chat path: everything else, answered by the same local model
```

### 1. Split settings out of the page

Move every tunable into **`punch-in-config.js`** (`window.PUNCH_IN_CONFIG = {...}`) next to the page. That covers `MAX_ROWS`, the four colours, pay rates and the keywords that match them, refresh intervals, weather location, panel order and visibility, and labels. Add a JSON Schema listing every allowed key, type and range. The page reads the config at load and falls back to built-in defaults for anything missing or invalid, so a bad write can never blank the wallpaper.

### 2. Dashboard control layer (plain Python, no AI)

Add `Jarvis\dashboard_control.py`. The model can only reach it through these tools:

| Tool | Example | Guard |
|---|---|---|
| `get_dashboard_config()` | "what colour are bills?" | read-only |
| `set_setting(key, value)` | `schedule.maxRows = 8` | key must be in the schema; value type and range checked |
| `set_color(role, hex)` | `shift → #3b82f6` | role ∈ shift / bill / pay / personal; valid hex; contrast check |
| `set_panel(name, visible, position)` | hide Robinhood | name ∈ known panels |
| `undo_last_change()` | "undo that" | restores the last backup |
| `remember(fact)` / `recall(query)` | "remember my Greenfield rate is $21" | writes only to `brain/Memory/Jarvis memory.md` |

Every write does four things: back up (keep the last 20), write the config for **every** `punchin*.dash` folder, push the change live, and append an entry to [[Dashboard change log]]. Jarvis gets **no** file paths, no shell and no HTML editing (this extends [[Safety rules]]).

### 3. Agent loop

- Switch the Ollama call from a PowerShell subprocess to a direct HTTP call to `/api/chat` with `tools=[…]`. Drop the `openai` provider (`JARVIS_LLM_PROVIDERS=ollama`).
- **Model:** a tool-calling 7–8B model at 4-bit uses about 5 GB and fits the RTX 4050's 6 GB. Examples are Qwen 2.5 7B Instruct and Llama 3.1 8B, or whichever 7–8B tool-calling model on Ollama is best when this gets built. Keep `llama3.2` for quick chat. Load only one model at a time (`OLLAMA_MAX_LOADED_MODELS=1`).
- **Pick the model with a test set:** write 30 real phrases, each with the tool call it should produce. Choose the model with the best accuracy that still answers in about 3 s. Keep the test set in `Jarvis\tests`.
- **Confirmation:** every write is read back ("Set Up next to 8 rows — confirm?") and applied only after "confirm". This also blocks prompt injection: an email subject on the dashboard that says "hide the inbox" can't change anything without Kayden's voice.

### 4. Vault as memory

- **Read:** at the start of each agent turn, search `brain/` and pass the top 3–5 matching sections to the model. The search matches keywords plus local embeddings from Ollama `nomic-embed-text` (about 270 MB, rebuilt nightly). Always include [[Safety rules]] and the relevant part of [[Punch In Dashboard]]. The Graphify graph (`graphify-out/graph.json`, see [[Brain Map/Brain Map|Brain Map]]) adds the linked notes, e.g. a question about sync also pulls in the data schema.
- **Write:** only append, and only to three places: `brain/Memory/Jarvis memory.md` (facts Kayden asks him to remember), [[Dashboard change log]] and [[Work log]]. Changing [[About Kayden]] needs a spoken confirmation. Use plain file writes, or the **Obsidian Local REST API** plugin that's already installed. Keep its API key in an environment variable and never in the vault.
- **Never stored:** audio, credentials or email bodies, same as [[Voice and privacy]].
- Rebuilding the Graphify map still needs Claude Code or a Gemini key for the semantic step. The local embedding index covers Jarvis's day-to-day recall without it.

### 5. Live apply

The page already polls the bridge for the orb status. Add `configVersion` to `/status`. When it changes, the page fetches `GET /dashboard-config` and applies the new CSS variables and constants without reloading, so changes show in about a second. The `punch-in-version.js` reload stays as the fallback.

### 6. Local data sync (removes Claude from the loop)

Replace the Claude scheduled task with `punchin_sync.py`, run by Windows Task Scheduler at 7 AM:

- **Calendar + Gmail:** Google APIs with read-only OAuth scopes. The token goes in Windows Credential Manager, not the vault.
- **Weather:** Open-Meteo, which needs no key. **Pay periods:** plain Python, same rules as today.
- **Robinhood:** ⚠️ decision needed. The only official Robinhood API covers crypto. Stock accounts only have unofficial libraries, which can break and involve your login. Options: keep that one panel on a manual or Claude refresh, use the official crypto API only, or drop it.
- Writes the same `punch-in-data.js` shape as [[Dashboard data schema]], plus [[Dashboard snapshot]].

### 7. Later: code-level changes

For requests like "add a panel for my car savings", Jarvis writes a patch to a **staging copy** of the page and renders a headless screenshot. Kayden approves it on screen, then it's applied, with a backup and a change-log entry. Expect a local 8B model to get these wrong often, so they are never automatic.

## Phases

| # | Phase | Size | Done when |
|---|---|---|---|
| 0 | Fix stuck `speaking`; `JARVIS_LLM_PROVIDERS=ollama`; pull a tool-calling model | 1 session | 31 + new tests pass; no cloud AI call possible |
| 1 | `punch-in-config.js` + schema; page reads it (artifact first, then wallpaper) | 1 session | Changing a value in the file changes the wallpaper |
| 2 | `dashboard_control.py` + tests + `/dashboard-config` | 1 session | Typed `/command?text=set rows to 8` works with confirm + undo |
| 3 | Agent loop + confirmation + 30-phrase eval | 1–2 sessions | ≥ 90% correct tool calls on the eval |
| 4 | Vault memory (search, remember/recall, auto log entries) | 1–2 sessions | "What did we change yesterday?" answered from the change log |
| 5 | Live apply | 1 session | Change visible in ≤ 2 s |
| 6 | Local sync | 2 sessions + Robinhood decision | 7 AM data with the Claude task paused |
| 7 | Draft-and-approve code changes | later | — |

## Risks

- **Wrong actions:** covered by schema validation, a spoken confirmation, one-word undo, and backups.
- **GPU contention:** gaming (e.g. Black Myth: Wukong) needs the same 6 GB. Unload the model after 5 minutes idle (`keep_alive`) and accept a slower first reply after a game.
- **OneDrive conflicts:** vault writes are small appends. Jarvis never rewrites whole notes.
- **Prompt injection** from dashboard or email text: the text is treated as data (see [[Dashboard context]]), and any write needs spoken confirmation.

## Related

- [[Recommended next integrations]] · [[Safety rules]] · [[Dashboard UI and parameters]] · [[Dashboard sync]] · [[Brain Map/Brain Map|Brain Map]]
