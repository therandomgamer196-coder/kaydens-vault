---
tags: [jarvis, reference]
---

# Maintenance

## How Jarvis stays online (since 2026-09-22)

| Layer | What it does |
|---|---|
| Autostart | `install-autostart.cmd` added **"Jarvis"** under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → runs `start-watchdog.vbs` at every sign-in. Undo: `uninstall-autostart.cmd`, or switch "Jarvis" off in Task Manager → Startup apps. |
| Watchdog | `jarvis_watchdog.py` checks `http://127.0.0.1:8765/health` every 30 s. Not answering → kills the hung bridge (PID from `jarvis_bridge.pid`; after 3 failures, every `jarvis_bridge.py` process) and starts a fresh one. Answering but not ready for 3 min → one restart, then waits 15 min before another. Log: `logs\watchdog.log`. Single instance via `jarvis_watchdog.lock`. |
| Bridge guard | The bridge relaunches the watchdog if it's gone (checked every 60 s). Disable with env `JARVIS_NO_WATCHDOG=1` while debugging. |
| Mic self-healing | Every mic failure (won't open, stream drops, no audio for 10 s) is retried every 5 s after re-scanning audio devices. A mic that fails to open, or drops within 60 s of opening twice in a row, is skipped for 5 min. If every mic is on cooldown they're tried anyway. |
| Engine retry | If the wake-word model fails to load, it retries every 30 s instead of dying. |

## Microphone choice

Default order: built-in **Microphone Array** → wired headset → any other mic → Bluetooth hands-free last. "Stereo Mix" is never used (it records the speakers). Reason: Windows keeps listing Galaxy Buds / phone hands-free mics that fail to open (PaErrorCode −9996 — the 2026-09-22 outage), and holding a Bluetooth mic open 24/7 forces the buds into low-quality call audio. Headsets first: set `JARVIS_MIC_PREFERENCE=headset`. Pin one device: `JARVIS_INPUT_DEVICE=<index>`.

## Scripts (in `C:\Users\NCG\Documents\Jarvis`)

- `restart-jarvis.cmd` — stops bridge + watchdog, starts them, prints ready/mic/error. Use after any code change (Python doesn't hot-reload).
- `stop-jarvis.cmd` — stops both (stays off until sign-in or restart).
- `install-autostart.cmd` / `uninstall-autostart.cmd` — sign-in autostart on/off.
- `start-jarvis.cmd` — bridge only (the bridge starts the watchdog within ~60 s).
- `tests\run_tests.py` — 292 checks in 10 suites for bridge + watchdog with faked audio; safe while Jarvis runs: `.venv\Scripts\python.exe tests\run_tests.py`.

## Health check

- `GET /health` — small: ok, ready, error, pid, uptime, mic_frames, last_mic_frame, input_device_name.
- `GET /status` — everything, including dashboard context. Connection refused = nothing running (the watchdog will restart it within 30 s).

## Logs

- `logs\wake_debug.log` — bridge startup, device list, every mic open/failure with traceback (rotates at 1 MB).
- `logs\watchdog.log` — every restart the watchdog made and why.

## Single-instance lock

Only one bridge can own the mic: `jarvis_bridge.lock` + `msvcrt.locking`. A second copy exits immediately. Windows releases the lock when the process exits, so a leftover file is harmless.

## History

- **2026-09-22 outage:** the bridge picked the Galaxy Buds hands-free mic (listed but unopenable), the wake-word thread died on the first error and never retried → `ready:false` until a manual relaunch. This design predates the Codex edits (Codex added the OpenAI fallback, disk-served interface, background asset). Fixed with the layers above; pre-fix copies in `backups\jarvis_bridge.py.2026-09-22-*`.
- **Fixed 2026-09-22 (11:55 PM):** the follow-up bug where Jarvis stayed `speaking:true` and took room chatter (and his own voice) as commands, and "multiple Jarvises" talking at once. See the conversation rebuild in [[Dashboard change log]] and how conversations work in [[Voice and privacy]].
- **2026-10-06 outage (Sep 24 → Oct 6):** the Jarvis startup entry was disabled in Task Manager (StartupApproved `03`), so nothing started after a reboot and the wallpaper showed "Bridge unavailable". Turned back on (`02`). If he's offline after a reboot, check this first: Task Manager → Startup apps → **Jarvis** = Enabled.
- **2026-10-06, language model offline after reboots:** the Ollama (Startup folder) and Lively startup entries were disabled. Both are re-enabled, and `llm_guard` now restarts Ollama and reloads the model every 60 s if needed. Check `/status` → `llm`.
- **Secrets:** `Jarvis\secrets\anthropic.env` holds the Anthropic API key. It's never served by the bridge and never written to notes. Env: `JARVIS_LLM_PROVIDERS` (default `claude,ollama`), `JARVIS_CLAUDE_MODEL`, `JARVIS_CLAUDE_EFFORT`, `JARVIS_OLLAMA_KEEP_ALIVE` (default `-1`), `JARVIS_NO_LLM_GUARD=1` to turn the guard off.
- **Keys and brains (2026-10-07):**
  - Keys live in `secrets\keys.env`.
  - `/status` → `free_brains` lists the working free brains, `claude` says whether Opus is ready, and `llm` shows the local model.
  - `/status` → `vault_sync` shows the GitHub sync ("synced" or what's wrong).
  - Env: `JARVIS_GROQ_MODEL`, `JARVIS_CEREBRAS_MODEL`, `JARVIS_FREE_REASONING` (low), `JARVIS_VAULT_SYNC_SECONDS` (300), `JARVIS_NO_VAULT_SYNC=1`.
- **Fixed 2026-10-06:** TV chatter taken as commands (weak wakes 0.35–0.5). See [[Agentic OS change log#2026-10-06]]. New log kind: `-> chatter`, `session N ended: chatter`. Env: `JARVIS_STRONG_WAKE_SCORE` (0.6), `JARVIS_MAX_COMMAND_WORDS` (30).
- Conversation log lines in `logs\wake_debug.log`: `wake word heard`, `heard '…' -> command/stop/closer/noise`, `barge-in by voice/wake phrase`, `turn timings {…}`, `ignored … of steady noise`, `session N ended: idle/stop/closer`.

## Other

- Audio uses PyAV + `sounddevice` — no Windows Media Player needed.
- Backups: `C:\Users\NCG\Documents\Jarvis\backups`.
