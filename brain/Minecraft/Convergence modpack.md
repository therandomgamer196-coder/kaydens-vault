---
tags: [minecraft, modpack]
---

# Convergence modpack

Part of [[Minecraft]]. This is Kayden's own CurseForge pack, merging four packs he likes. It was built on 2026-09-27.

## What it is

- **Sources, in config priority order:**

  | Pack | Version | Loader | Mods |
  |---|---|---|---|
  | Beyond Depth 12.8.3 | 1.20.1 | Forge | 526 |
  | DeceasedCraft 5.10.17 | 1.20.1 | Forge | 317 |
  | Stellara 1.3 | 1.21.1 | NeoForge | 191 |
  | ATM10 8.2 | 1.21.1 | NeoForge | 495 |

  That's 1,148 unique mods.
- **Target: 1.20.1 Forge 47.4.22, with 1,057 mods.** 1.21.1 would have lost DeceasedCraft's guns, vehicles and zombies (TaCZ and others) and Beyond Depth's Alex's Mobs and Alex's Caves.
- **Cut: 91 mods.**
  - 63 have no 1.20.1 build. These are mostly ATM10's newest mods, such as Oritech, Actually Additions, Just Dire Things and Eternal Starlight.
  - 28 are covered by an equivalent already in the pack, for example Sodium → Embeddium and JourneyMap → Xaero's.
- **Quests and scripts:** the Beyond Depth and DeceasedCraft quest books are merged into one. ATM10's quests and scripts are 1.21-only, so they aren't included.
- **RAM:** give the pack 10 GB or more.

## Files

- **Importable pack:** `Downloads\Convergence-1.0.0.zip`. In CurseForge: Create Custom Profile → Import.
- **Build folder:** `%LOCALAPPDATA%\Temp\modpack-build`. It holds `plan.json`, `analysis.json`, `pack_data.json`, `icons.png` (1,141 mod icons) and the `sources/` packs.
- **Control page:** https://claude.ai/artifact/H7GHbxNeTVxjhpgjiJ4Qc1. It's Minecraft-styled and:
  - turns whole packs and single mods on or off,
  - has a search bar for the pack list,
  - has a "Find a mod online" search where Claude suggests CurseForge mods and modpacks and **Add** saves them.

## How to apply page changes

1. Say "rebuild Convergence from the page".
2. Claude reads the page's saved data:
   - `settings/selection` holds `disabledPacks` and `disabledMods` (project IDs),
   - `added/*` holds the requested mods and modpacks.
3. Each added mod gets checked on CurseForge for a 1.20.1 Forge file.
4. The merger rebuilds with `packmerge.py build`: turned-off packs go in `disabled_sources`, turned-off mods in `remove_projects`, and additions in `add_projects` or as new sources.
5. Claude sets each added item's `status` to `added` or `unavailable`, with a `note`.

## First launch fix (2026-09-27, about 11 PM)

- **What broke:** the first launch stopped with "Mod loading has failed". Nine mods needed newer or missing libraries.
- **Fixed in the installed profile** (`curseforge\minecraft\Instances\Convergence`):
  - updated Sophisticated Core and Backpacks, Miner's Delight, Moog's Structure Lib, End Structures, Voyager Structures and SuperMartijn642's Core Lib,
  - added FLIB, DragonLib and Armor Model API.
- **Set aside:** old versions go to `mods_backup_2026-09-27`, along with Shield API 1.1.2 (it blocked a newer bundled copy) and Advanced Peripherals (CurseForge has no CC:Tweaked new enough).
- **Result:** after the fixes the jar check shows no real problems.

## Version 1.0.1 (2026-09-27, about 11:30 PM)

- **What happened:** Kayden imported the 1.0.0 zip a second time, which created the profile **"Convergence (1)"**. It crashed with the original errors, because the fixes had only gone into the first profile, "Convergence".
- **Both profiles fixed:** the same library swaps, the controller files and the default options. Either profile works.
- **New zip:** `Downloads\Convergence-1.0.1.zip`, with 1,058 mods, the library fixes and the controller included. The broken 1.0.0 zip moved to the build folder as `Convergence-1.0.0-old.zip`.
- **Lesson:** fixing an installed profile doesn't fix the zip. Always rebuild the zip after fixing a profile.

## Open items

- Kayden still has to import it. Then run `packmerge.py check` on the instance before the first launch to catch missing dependencies.
- Turn off FTB Chunks' minimap, since Xaero's is the map.
- Possible ports of small open-source 1.21-only mods, on request.
- Full procedure: the `modpack-merger` skill in `~/.claude/skills/`.
