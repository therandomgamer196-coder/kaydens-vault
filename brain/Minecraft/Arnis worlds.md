---
tags: [minecraft, arnis]
---

# Arnis worlds

Part of [[Minecraft]]. Arnis turns OpenStreetMap data into Minecraft Java worlds.

## The crash (2026-09-27)

- **What happened:** the launcher's "Latest snapshot" installation auto-updated to 26.4 Snapshot 1. Opening an Arnis world then crashed with "Exception generating new chunk", a `FlatLevelSource.getBaseColumn` error saying "block is null".
- **Why:** Arnis fills the area outside the map with a superflat world whose bottom layers are air and which has villages turned on. When a village tried to generate near the map edge, the snapshot tripped over the air layers.
- **Fix applied:** turned off structure generation in "Arnis World 1" and "ephrata". Backups are saved next to the edited files. Arnis World 1 then loaded fine in 26.3.

## Normal-terrain rebuild

- **The world:** `saves\Ephrata - Normal Terrain (1.21.1)`.
- **Command:** `arnis-windows.exe --bbox "40.163104,-76.212686,40.191457,-76.156245" --scale 1.45 --ground-level 64 --fillground --output-dir <temp>`
- **Changes after the build:**
  - switched the generator to vanilla terrain with `mcworld.py set-generator normal`
  - stamped the world as 1.21.1 with `mcworld.py stamp-version 3955 1.21.1`
- **Result:** the ground sits at about Y 72–145 with solid stone underneath. It spawns at the north-west corner (0,0), and downtown is roughly X 4160, Z 1880.
- **Keep it moddable:** play it on 1.21.1, or copy it into a 1.21.1 NeoForge CurseForge profile. Opening it once in 26.x converts it permanently.

## Facts worth remembering

- Arnis 3.2.0 writes 1.21.1 chunks (DataVersion 3955) but labels `level.dat` as 1.21.4 (DataVersion 4189).
- `--output-dir` is a parent folder: Arnis creates `Arnis World N` inside it.
- DataVersions: 3955 = 1.21.1, 4189 = 1.21.4, 5023 = 26.3, 5119 = 26.4 Snapshot 1.
- Full procedure: the `minecraft-arnis` skill in `~/.claude/skills/`.
