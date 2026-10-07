---
tags: [log]
---

# Work log

Dated summary of work on Jarvis, the dashboard, and this vault. Details live in the linked notes. Newest first.

## 2026-09-22

- **Jarvis outage fixed** — Galaxy Buds hands-free mic + a wake-word thread that never retried. Mic self-healing, laptop mic array preferred, watchdog, bridge↔watchdog supervision, sign-in autostart, 31 tests in `Jarvis\tests`. → [[Maintenance]]
- **Dashboard showing 5-day-old data fixed** — sync wrote to the wrong wallpaper folder (`punchin.dash` instead of `punchin-v19.dash`). → [[Dashboard change log]]
- **Sync 48 runs/day → 1** — "Punch In daily sync (7 AM)" writes the artifact, every wallpaper folder, and [[Dashboard snapshot]]. → [[Dashboard sync]]
- **Up next** — today's date always on top; finished events drop off. → [[Dashboard UI and parameters]]
- **Artifact** — reads the synced data again (Version 30). → [[Punch In Dashboard]]
- **Vault** — new Punch In Dashboard section, updated Maintenance / Main information directory / Voice and privacy, vault graph republished with the dashboard cluster.
- **Claude Code** — PATH fixed, Git installed, Obsidian skills plugin and Graphify installed, `CLAUDE.md` added. → [[Claude Code setup]]
- **Open items** — Jarvis sometimes stays "speaking" during follow-ups and takes room chatter as commands; three Obsidian skill cards in Cowork still unsaved (the Claude Code plugin covers Claude Code; the cards only matter for Cowork).
