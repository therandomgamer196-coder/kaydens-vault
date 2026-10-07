---
tags: [agentic-os, jarvis, index]
aliases: [Agentic OS, Jarvis OS project]
created: 2026-09-25
---

# Agentic OS

This is the project that turns Jarvis into Kayden's own agentic operating system. He's a voice that answers and acts, with a dashboard that shows everything he's doing and visuals that give him a face. It is **not** part of the [[Punch In Dashboard]] project: Punch In is the shift, pay and schedule wallpaper, and Agentic OS is Jarvis himself.

> [!important] Where changes go
> Every change to Jarvis, the Jarvis OS dashboard or the Jarvis visuals gets a dated entry in [[Agentic OS change log]]. Only changes to the Punch In wallpaper page, its data or its sync go in [[Dashboard change log]].

## Dashboard

> [!tip] Brain and cloud (2026-10-06)
> Jarvis now thinks with Claude Opus 5.5 once his API key is in (see [[Jarvis Cloud Setup]]). He searches this vault live, keeps his own notes in [[Jarvis Notes]], and works through [[Jarvis Inbox]].


The screens of the Agentic OS, all labelled **dashboard**:

| Piece | What it is | Open it |
|---|---|---|
| [[Jarvis OS dashboard]] | The main desktop dashboard: clock, green orb, runs, sessions, projects, specs, memory, usage | **Jarvis Dashboard** shortcut, `http://127.0.0.1:8765/dashboard`, or the Lively wallpaper "Jarvis OS" |
| [[Jarvis Black Hole]] | A cinematic 3D black hole with orbiting lights. It's a candidate face or background for Jarvis | **Jarvis Black Hole** shortcut (runs on the RTX), or the pinned artifact |
| [[Jarvis Brain 3D]] | Jarvis's memory (this vault) drawn as a glowing 3D brain | **BRAIN GRAPH ↗** on the dashboard, the pinned artifact, or the **Jarvis Brain** shortcut (Obsidian graph) |

## Links

Every link in one place, so nobody has to dig through old chats. Each note above has the details.

| What | Link |
|---|---|
| Jarvis Black Hole artifact (pinned) | https://claude.ai/artifact/TyaawfYELEMKHSPZnddJay |
| Jarvis Brain 3D artifact (pinned) | https://claude.ai/artifact/DGm2GkGjMiQ1Mv9ys5ZrFE |
| Punch In wallpaper artifact (pinned, Punch In project) | https://claude.ai/artifact/BnMpwFjCK6U4bC4bns8LHv |
| Older vault graphs (2D, 2026-09-22) | https://claude.ai/artifact/BSW3n4jc46mvbP5hsVyK2P · https://claude.ai/artifact/1WRQH55JGGdQEnZyGcDThQ |
| Jarvis bridge (only while Jarvis runs) | `http://127.0.0.1:8765`: `/health`, `/status`, `/dashboard`, `/brain`, `/preview?text=` (dry run, opens nothing) |
| Black hole page | `C:\Users\NCG\Documents\Jarvis\assets\jarvis-black-hole.html` |
| Black hole website (not live yet) | `C:\Users\NCG\Documents\Jarvis\website\`, for jarvisgalaxy.com once the domain is bought and hosted |
| 3D brain page | `Kaydens Vault\Brain Map\Jarvis Brain 3D.html` |
| Shortcuts (Desktop + Start menu) | **Jarvis Dashboard**, **Jarvis Black Hole**, **Jarvis Brain**, plus **Jarvis Galaxy** (Desktop only: the black hole in a normal Edge browser window on the RTX) |
| Scripts | `Jarvis\open-on-rtx.ps1` (any page on the RTX), `Jarvis\open-brain-graph.ps1` (Obsidian graph view), `Jarvis\restart-jarvis.cmd` |

## Jarvis's parts

- [[Voice and privacy]]: wake word, conversation, voice (Piper), and opening apps and websites
- [[Safety rules]]: what he may do, the bridge lock, what he must never do
- [[Autonomous agent plan]]: the roadmap (permission tiers, files, terminal, local agent brain, self-improvement)
- [[Jarvis future plans]]: what's asked for but blocked, and what unblocks each item
- [[Maintenance]] and [[Main information directory]]: how he stays online, paths, ports, tests

## Running visuals on the RTX

The laptop has Intel graphics and an RTX 4050. Opera GX draws on the Intel chip: its High performance setting is on the installer (`OperaGXSetup.exe`), not on `opera.exe`. The Claude app was set to High performance by 2026-09-25, but its viewer blocks outside map servers. Every Jarvis visual therefore opens in an Edge app window forced onto the RTX:

- **`Jarvis\open-on-rtx.ps1 [file or URL] [-Restart]`** does this for any page. It uses `--force_high_performance_gpu` with its own profile, `%LOCALAPPDATA%\JarvisBlackHole`. `-Restart` closes only that profile's windows first, so an edited page loads fresh. With no target it opens the black hole.
- **Check:** `nvidia-smi` lists `msedge.exe` as a C+G process.
- A web link such as an artifact can't choose the GPU; it runs on whatever the browser uses. To put Opera GX on the RTX too, Kayden adds `C:\Users\NCG\AppData\Local\Programs\Opera GX\opera.exe` as *High performance* in Settings → System → Display → Graphics.
