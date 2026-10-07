---
tags: [minecraft, modpack, app]
---

# Convergence app

A local Windows app that merges 2 to 4 Minecraft Java modpacks into one pack that loads. Built 2026-10-07. It replaces the hand-run scripts behind [[Convergence modpack]] and the old Claude artifact control page.

- **Folder:** `C:\Users\NCG\Documents\Convergence`
- **Open it:** the **Convergence** desktop shortcut (runs `pythonw app.py --open`; an Edge app window on `http://127.0.0.1:8777`)
- **Handoff files in the folder:** `CLAUDE.md` (full technical handoff), `STATUS.md` (verified, not verified, open list), `README.md` (how to use), `START_PROMPT.md` (prompt to paste into Claude Code in VS Code)

## How to use

1. **Discover:** search Modrinth, pick an installed CurseForge profile, or paste a CurseForge modpack link. Add 2 to 4 packs.
2. **Merge:** set the order (higher pack wins a config clash), name the pack, press **Build merged pack**.
3. Leave the Minecraft test window alone. It opens and closes by itself.
4. **Show the zip**, then in CurseForge: Create Custom Profile → Import. Give it 8 to 11 GB.

## What a build does

1. Reads each pack's versions and loader.
2. Picks the Minecraft version and loader that keeps the most mods.
3. Takes one file per mod; lists the mods with no build for that version.
4. Downloads (shared cache, hard links).
5. Merges configs, scripts and quest books.
6. Removes duplicates and wrong-loader jars, adds missing libraries, updates old ones.
7. Test-boots offline, removes whatever stops the main menu, boots again.
8. Writes a CurseForge-importable zip to Downloads.

## Parts

- `engine.py`: all the work, standard-library Python.
- `app.py`: local server on `127.0.0.1:8777` with Host and Origin checks.
- `ui/index.html`: one-file interface (Discover, Merge, Builds, Settings).
- `workspace/`: `cache`, `packs`, `builds/<name>/` (`instance`, `overrides`, `removed`, `report.json`).

## Status on 2026-10-07

- **Proven:** two Modrinth packs (Fabulously Optimized + Cobblemon Official) → 1.21.1 Fabric, 107 mods, Krypton removed by the repair loop, main menu on boot 2, 132 s in total.
- **Fixed on the way:** jars that support both Fabric and Forge were treated as Forge-only.
- **Not proven yet:** CurseForge-pack sources, Forge and NeoForge targets, cross-loader merges, 3 to 4 large packs, importing the zip into CurseForge.
- **Clean slate:** the workspace and the test zip were emptied to the Recycle Bin. The old "Convergence" test profiles are hidden from the Installed list.
- **2026-10-07 check:** `python app.py` returned HTTP 200 from the local status endpoint, and the page rendered in the browser pane. A Forge 1.20.1 CurseForge + Modrinth test build was not started because approval to fetch mod files is required.

## Limits to remember

- One pack runs on one Minecraft version and loader. Mods with no build for it are left out and listed.
- CurseForge search is blocked without an official API key, so CurseForge packs come in by link or from installed profiles. Modrinth search is open.
- A test boot needs that loader installed once in the CurseForge app.
- Game Boost is started by the user from the app. Claude never runs it.

## Next (from `STATUS.md`)

1. Forge 1.20.1 merge with a CurseForge pack.
2. Preview before downloading.
3. Per-mod switches and a quick rebuild.
4. Names and icons for CurseForge mods.
