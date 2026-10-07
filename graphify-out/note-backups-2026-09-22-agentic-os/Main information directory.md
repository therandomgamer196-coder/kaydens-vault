---
tags: [jarvis, reference]
---

# Main information directory

- Project folder: `C:\Users\NCG\Documents\Jarvis`
- Bridge: `http://127.0.0.1:8765` (localhost-only; never leaves the machine)
- Dashboard file it's embedded in: `punchin-v19.dash\punch-in-wallpaper.html` (Lively must be running this exact wallpaper)
- Runtime: `C:\Users\NCG\Documents\Jarvis\.venv` (Python 3.11–3.13; 3.12 recommended — 3.14 currently lacks compatible wheels)
- Launcher: starts automatically at sign-in (watchdog → bridge, fully hidden). By hand: `restart-jarvis.cmd`. See [[Maintenance]].
- Backups: `C:\Users\NCG\Documents\Jarvis\backups`
- Logs: `C:\Users\NCG\Documents\Jarvis\logs\mcp-activity.jsonl` — MCP tool calls only, redacted (emails, long numbers, API-key-looking values are stripped)
- Claude Desktop connector: `dashboard_mcp_server.py` (see [[Dashboard context]])

## Install (one-time)

1. Install Python 3.12.
2. `Set-Location "$HOME\Documents\Jarvis"` in PowerShell, then run `.\setup.ps1`.
3. Setup downloads openWakeWord's models and checks for `hey jarvis`. If missing, drop a verified `.onnx` at `models\hey_jarvis.onnx`.
4. Install Ollama, `ollama run llama3.2` to pull the local model.
5. First launch: allow microphone access for Python when Windows prompts.

## Start / stop

- Start / restart: `restart-jarvis.cmd`. Stop: `stop-jarvis.cmd`.
- Verify it's up: open `http://127.0.0.1:8765/` — should show the command-centre interface, not a connection error.
- Only one instance can hold the microphone at a time (see Maintenance note for the lock mechanism).
- Windows startup: registered 2026-09-22 via `install-autostart.cmd` (HKCU Run entry "Jarvis"); undo with `uninstall-autostart.cmd`.
