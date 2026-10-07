---
type: brain-map
tags: [brain-map, index]
generated: 2026-09-22
---
# Brain Map

> [!info] Generated — don't hand-edit
> Built by Graphify from every note in `brain/`, then rewritten into this folder by `graphify-out/build_brain_map.py`. The real notes stay in `brain/`; this folder only holds the map. Rebuild steps are at the bottom.

Jarvis's memory as a brain: **82 nodes** (65 neurons + 17 brain notes), **165 connections**, **10 lobes**. Hub notes ([[Jarvis Brain]], [[Maintenance]], …) are the white nodes; neurons are coloured by lobe.

## Ways to look at it

- **Graph view** — `Ctrl+G`. Colours below. Zoom in to read labels, drag a node to see what it pulls with it.
- **Canvas** — [[Brain Map/Jarvis Brain Map.canvas|Jarvis Brain Map]]: the lobes laid out as two hemispheres.
- **3D** — open `Brain Map\Jarvis Brain 3D.html` in a browser (glowing, rotating, click a node for details).
- **Table** — [[Main brain Base.base|Main brain Base]] lists every note and neuron.

## Lobes

| Lobe | Region | Colour | Neurons |
|---|---|---|---|
| [[Lobe - Future Integrations & Research]] | Left frontal lobe | `#c084fc` | 15 |
| [[Lobe - Jarvis Core System]] | Left parietal lobe | `#ff7a18` | 12 |
| [[Lobe - Reliability & Maintenance]] | Brainstem | `#22d3ee` | 12 |
| [[Lobe - Safety & Voice Privacy]] | Left temporal lobe | `#f43f5e` | 11 |
| [[Lobe - Kayden & Jobs]] | Right temporal lobe | `#facc15` | 6 |
| [[Lobe - Dashboard Data Sync]] | Right occipital lobe | `#34d399` | 6 |
| [[Lobe - Dashboard Display Files]] | Left occipital lobe | `#60a5fa` | 6 |
| [[Lobe - Claude Code Tooling]] | Right frontal lobe | `#e879f9` | 5 |
| [[Lobe - Logs & Change Tracking]] | Cerebellum | `#a3e635` | 5 |
| [[Lobe - Dashboard UI Widgets]] | Right parietal lobe | `#818cf8` | 4 |

## Hubs (most connected)

- [[brain/Core Brain Functions/Maintenance|Maintenance]] — 13 connections
- [[brain/Jarvis Brain|Jarvis Brain]] — 13 connections
- [[brain/Punch In Dashboard/Punch In Dashboard|Punch In Dashboard]] — 13 connections
- [[brain/Work log|Work log]] — 12 connections
- [[brain/Core Brain Functions/Voice and privacy|Voice and privacy]] — 10 connections
- [[brain/Core Brain Functions/Main information directory|Main information directory]] — 9 connections
- [[Punch In daily sync (7 AM)]] — 8 connections
- [[PUNCH_IN_DATA object]] — 8 connections

## Circuits

Groups of nodes that work together as one flow:

- **Jarvis uptime supervision layers**: [[Sign-in autostart]] → [[Jarvis watchdog]] → [[Bridge guard]] → [[Mic self-healing]] → [[Single-instance lock]] → [[health and status endpoints]]
- **Jarvis voice command pipeline**: [[Hey Jarvis wake word]] → [[faster-whisper transcription]] → [[Command routing]] → [[Ollama local model]] → [[Edge neural TTS (en-GB-RyanNeural)]]
- **Dashboard data pipeline (sync to page)**: [[Punch In daily sync (7 AM)]] → [[PUNCH_IN_DATA object]] → [[punch-in-data.js]] → [[punch-in-wallpaper.html]] → [[Dashboard artifact (test copy)]] → [[Lively wallpaper (Dashboard Version 19)]]

## Cross-lobe links worth checking

Inferred by the model, not stated in a note — confirm or fix the note if one is wrong:

- [[Command routing]] triggers [[Ollama local model]] · inferred 0.95
- [[Jarvis orb]] triggers [[health and status endpoints]] · inferred 0.95
- [[POST dashboard-context]] related to [[Untrusted data rule]] · inferred 0.95
- [[Stale wallpaper data fix]] explains why [[Punch In daily sync (7 AM)]] · inferred 0.95
- [[Jarvis watchdog]] references [[Jarvis bridge]] · inferred 0.95
- [[Up next panel]] shares data with [[PUNCH_IN_DATA object]] · inferred 0.95
- [[Dashboard artifact (test copy)]] shares data with [[PUNCH_IN_DATA object]] · inferred 0.95
- [[Microphone choice order]] related to [[brain/Core Brain Functions/Voice and privacy|Voice and privacy]] · inferred 0.85

## Rebuild

After notes in `brain/` change, in Claude Code opened on the vault folder:

1. `/graphify . --update` — re-reads only changed notes (`Brain Map/` is excluded by `.graphifyignore`).
2. `python graphify-out\build_brain_map.py` — regenerates this folder, the canvas, the 3D page, and Graph view colours.
