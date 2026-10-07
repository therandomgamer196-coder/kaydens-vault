---
tags: [jarvis, index]
---

# Jarvis Brain

## Role

Jarvis is a local Windows voice assistant embedded in the Punch In Lively Wallpaper dashboard. This vault is his memory: project setup, exact operating behavior, safety rules, and what he needs to know about Kayden — enough that he never has to open the source code to answer a question about himself.

## Contents

- [[About Kayden]] — who Kayden is, so Jarvis can answer personally
- [[Core Brain Functions/Main information directory|Main information directory]] — paths, ports, launcher, install/start/stop
- [[Core Brain Functions/Dashboard context|Dashboard context]] — what the wallpaper feeds Jarvis, the Claude Desktop MCP connector
- [[Core Brain Functions/Voice and privacy|Voice and privacy]] — wake word, mic, thresholds, TTS, audio validation rule
- [[Core Brain Functions/Safety rules|Safety rules]] — allowlisted actions, safe sites, what Jarvis must never do
- [[Core Brain Functions/Maintenance|Maintenance]] — /status fields, the single-instance lock, troubleshooting "not responding"
- [[Core Brain Functions/Recommended next integrations|Recommended next integrations]] — roadmap
- [[Core Brain Functions/Research references|Research references]] — background reading
- [[Core Brain Functions/Claude Code setup|Claude Code setup]] — how to open this project in Claude Code, installed plugins
- [[Core Brain Functions/Jarvis OS dashboard|Jarvis OS dashboard]] — **new main desktop dashboard** (Lively wallpaper "Jarvis OS" + `127.0.0.1:8765/dashboard`): clock, orb, runs, sessions, projects, specs, memory, usage, brain graph
- [[Core Brain Functions/Jarvis future plans|Jarvis future plans]] — what's asked for but blocked or waiting, and what unblocks each
- [[Core Brain Functions/Autonomous agent plan|Autonomous agent plan]] — the Jarvis OS roadmap: permission tiers, apps/files/terminal, local agent brain, vault memory, self-improvement, fully local

### Agentic OS

- [[Agentic OS/Agentic OS|Agentic OS]]: the project that makes Jarvis an agentic OS. It has every link (artifacts, bridge routes, shortcuts, scripts) and its own [[Agentic OS/Agentic OS change log|change log]].
  - Dashboard: [[Core Brain Functions/Jarvis OS dashboard|Jarvis OS dashboard]], [[Agentic OS/Jarvis Black Hole|Jarvis Black Hole]], [[Agentic OS/Jarvis Brain 3D|Jarvis Brain 3D]].

### Punch In Dashboard

- [[Punch In Dashboard/Punch In Dashboard|Punch In Dashboard]] — the wallpaper + artifact: files, daily sync, UI parameters, data schema, change log, current snapshot

### Trading OS

- [[Trading OS/Trading OS|Trading OS]]: Kayden's trading desk. It covers the live Robinhood dashboard, the $15 real-money [[Trading OS/Auto-trader|Auto-trader]], the [[Trading OS/Crypto 24-7 monitor|Crypto 24/7 monitor]] (paper), the [[Trading OS/Liquidity sweep plan|Liquidity sweep plan]], a [[Trading OS/Trading glossary|Trading glossary]] and its own [[Trading OS/Trading OS change log|change log]]. Read it first for anything trading, stocks, crypto or NQ.

### Minecraft

- [[Minecraft/Minecraft|Minecraft]]: Kayden's Minecraft setup, the [[Minecraft/Arnis worlds|Arnis worlds]] and the [[Minecraft/Convergence modpack|Convergence modpack]].

- [[Work log]] — dated summary of every work session

### Brain Map

- [[Brain Map/Brain Map|Brain Map]] — generated Graphify map of this vault: lobes, neurons, hubs, circuits (Graph view `Ctrl+G`, canvas, 3D page). Generated notes live in `Brain Map/`, never in `brain/`.
- [[Main brain Base.base|Main brain Base]] — table of every note and neuron

### Design note

Each topic lives in exactly one file, linked from here — nothing is duplicated between this index and the notes it points to. When something changes, edit the one file it belongs to.
