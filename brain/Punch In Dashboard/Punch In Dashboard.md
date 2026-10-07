---
tags: [dashboard, index]
aliases: [Punch In, PunchIn, dashboard]
---

# Punch In Dashboard

Kayden's personal dashboard: shift schedule, estimated pay, Robinhood totals, flagged inbox, weather, and the Jarvis orb. It exists in two places that run the **same page code**:

| Surface | Where | Reads data from |
|---|---|---|
| Live desktop wallpaper | Lively Wallpaper (Microsoft Store build), wallpaper **"Dashboard Version 19"** = folder `punchin-v19.dash` | `punch-in-data.js` sitting next to the page in that folder |
| Test copy (artifact) | https://claude.ai/artifact/BnMpwFjCK6U4bC4bns8LHv | the artifact's database, doc `dashboard/data` |

> [!important] Read before changing anything
> Check this folder first, change the dashboard, then add an entry to [[Dashboard change log]] with what changed and its parameters. Test visual changes in the artifact before applying them to the wallpaper.

## Notes

- [[Dashboard sync]] — the once-a-day 7 AM sync: what it pulls, where it writes, how to change it
- [[Dashboard UI and parameters]] — every panel, refresh interval, constant, and color
- [[Dashboard data schema]] — the exact shape of `punch-in-data.js` / `dashboard/data`
- [[Dashboard change log]] — dated record of every change
- [[Dashboard snapshot]] — what the dashboard is showing right now (refreshed by the daily sync)
- [[Core Brain Functions/Dashboard context|Dashboard context]] — how the dashboard feeds Jarvis

## File map

| File | Path | Role |
|---|---|---|
| Active wallpaper page | `C:\Users\NCG\AppData\Local\Packages\12030rocksdanister.LivelyWallpaper_97hta09mmv6hy\LocalCache\Local\Lively Wallpaper\Library\wallpapers\punchin-v19.dash\punch-in-wallpaper.html` | the real, running dashboard |
| Its data file | same folder `\punch-in-data.js` | **the copy Lively actually loads** |
| Version beacon | same folder `\punch-in-version.js` | change the string → wallpaper reloads itself within 2 min |
| Mirror data file | `C:\Users\NCG\Documents\PunchIn\punch-in-data.js` | kept in sync; used when the page is opened in a normal browser |
| Old wallpaper | `...\wallpapers\punchin.dash` | earlier version, not active; the sync still writes its data |
| Lively's active pick | `...\Lively Wallpaper\WallpaperLayout.json` → `LivelyInfoPath` | tells you which folder is live |
| Backups | `punch-in-wallpaper.html.bak-2026-09-22`, `punch-in-data.js.bak-2026-09-17` in the v19 folder; `punchin-v19.dash.backup-20260921` folder | roll back by copying over |

> [!note] Why the wallpaper path matters
> Lively's browser refuses absolute `file:///` URLs, so the page ignores `Documents\PunchIn` and loads the data file **next to itself**. Any new wallpaper version folder must get its own `punch-in-data.js` (the sync writes to every `punchin*.dash` folder automatically).
