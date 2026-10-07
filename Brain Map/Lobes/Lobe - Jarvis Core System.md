---
type: lobe
region: Left parietal lobe
color: "#ff7a18"
neurons: 12
cohesion: 0.29
tags: [brain-map, lobe]
generated: 2026-09-22
---
# Lobe - Jarvis Core System

> **Left parietal lobe** — the core of Jarvis: bridge, model, interface, and the index that ties it together.

## Brain notes in this lobe

- [[brain/Jarvis Brain|Jarvis Brain]]
- [[brain/Core Brain Functions/Main information directory|Main information directory]]
- [[brain/Core Brain Functions/Dashboard context|Dashboard context]]

## Neurons

- [[Jarvis bridge]] — Localhost-only HTTP server at 127.0.0.1:8765 (jarvis_bridge.py) that hosts Jarvis and serves /health, /status and the command-centre UI.
- [[Jarvis]] — A local Windows voice assistant embedded in the Punch In Lively Wallpaper dashboard; this vault is his memory.
- [[POST dashboard-context]] — The wallpaper posts a read-only snapshot (calendar, inbox, Robinhood, weather) to the bridge.
- [[dashboard_mcp_server.py]] — Local read-only MCP server for Claude Desktop exposing dashboard summary, shifts, inbox, Robinhood, weather and Jarvis status tools.
- [[HP Victus laptop]] — The machine Jarvis runs on: RTX 4050 with 6GB VRAM and Intel i5, which caps local model size.
- [[Ollama local model]] — Local LLM runtime; `ollama run llama3.2` pulls the model that answers non-allowlisted commands.
- [[mcp-activity.jsonl log]] — Redacted log of MCP tool calls only; emails, long numbers and API-key-like values are stripped.
- [[Command-centre interface]] — Full-screen local UI at 127.0.0.1:8765 mirroring the orb and panels; ?screensaver=1 enables screensaver mode.
- [[restart-jarvis.cmd]] — Script that stops and restarts bridge and watchdog; use after any code change since Python does not hot-reload.

## Wired to other lobes

- [[Lobe - Future Integrations & Research]] — 4 connections
- [[Lobe - Reliability & Maintenance]] — 4 connections
- [[Lobe - Safety & Voice Privacy]] — 4 connections
- [[Lobe - Dashboard Display Files]] — 3 connections
- [[Lobe - Kayden & Jobs]] — 3 connections
- [[Lobe - Logs & Change Tracking]] — 2 connections
- [[Lobe - Dashboard Data Sync]] — 2 connections
- [[Lobe - Claude Code Tooling]] — 1 connection

Back to [[Brain Map]]
