---
tags: [minecraft, index]
---

# Minecraft

Kayden's Minecraft setup and the projects Claude has done on it. Each topic has its own note:

- [[Arnis worlds]]: real-world maps of Ephrata built with Arnis, the snapshot crash fix and the normal-terrain rebuild
- [[Convergence modpack]]: ATM10, Stellara, Beyond Depth and DeceasedCraft merged into one CurseForge pack, with its control page
- [[Convergence app]]: the desktop app that merges 2 to 4 modpacks by itself (search, build, test boot, export), in `Documents\Convergence`
- [[Controller and Game Boost]]: Kayden's Xbox Controller (Bedrock layout on Controllable, for the Elite Series 2) and the desktop Game Boost shortcut

## Setup

- **Game folder:** `%APPDATA%\.minecraft`, using the Microsoft Store launcher. Crash reports are in `crash-reports\` and worlds in `saves\`.
- **Launcher warning:** the "Latest snapshot" installation silently auto-updates to test builds. That is how the 26.4 Snapshot 1 crash happened on 2026-09-27, so play releases instead.
- **CurseForge:** `C:\Users\NCG\curseforge\minecraft\Instances\`. Installed packs:
  - All the Mons (1.21.1 NeoForge)
  - ATM10 Sky (1.21.1 NeoForge)
  - DeceasedCraft (1.20.1 Forge)
  - Cursed Walking (1.20.1 Forge)
  - Lancelot (1.21.10 NeoForge)
  - RLCraft (1.12.2)
- **Arnis:** `C:\Users\NCG\Downloads\arnis-windows.exe`, v3.2.0 with a full command-line mode.
- **Hardware:** 16 GB RAM and an RTX 4050, so give very large packs about 10 GB.

## Claude's tools for this

These live in `~/.claude/skills/` and load in every Claude Code session:
- **minecraft-arnis:** crash triage and world repair. Its `mcworld.py` reads and patches `level.dat`, world generation settings and region files.
- **modpack-merger:** combines modpacks. Its `packmerge.py` covers `info`, `fetch`, `analyze`, `build` and `check`.
