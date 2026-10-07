---
tags: [dashboard, changelog]
---

# Dashboard change log

> [!important] Rule
> Every change to the dashboard (page, data, sync, or Jarvis link) gets an entry here: date, what changed, parameters, files touched, and how to undo it. Newest first.

## 2026-09-22

**Up next — today's date always on top; finished events hidden**
- `renderSchedule` now always starts with "Today · <Weekday>, <Mon D>" (cherry), then "Nothing else today" / "Nothing scheduled today" when nothing is left; events drop off after their end time; running-from-yesterday events file under Today. New helper `evEndMs`, new CSS `.row-empty`.
- Files: `punchin-v19.dash\punch-in-wallpaper.html`; version beacon bumped to reload Lively.
- Undo: copy `punch-in-wallpaper.html.bak-2026-09-22` back over the page and change `punch-in-version.js`.
- Tested in headless Chromium at 3:27 PM (shift upcoming), 11 PM (after shift), and next-morning (empty day) with the real data.

**Wallpaper was showing 5-day-old data — fixed**
- Cause: the refresh task wrote `punch-in-data.js` to `punchin.dash`, but the active wallpaper is `punchin-v19.dash` (Lively only loads the copy next to the page). "Synced 124h ago", Robinhood $125.48, and Sep 17 events were all stale.
- Fix: copied today's data into v19; the sync now writes to every `punchin*.dash` folder.

**Sync: 48 runs/day → 1 run/day at 7 AM**
- Merged the two hourly tasks into "Punch In daily sync (7 AM)" (see [[Dashboard sync]]); paused "Refresh Punch In dashboard". Added weather to the sync.

**Artifact reads live data again**
- The artifact had been republished from the wallpaper HTML and lost its database read, so it showed built-in placeholder data. The page now subscribes to `dashboard/data` when it runs inside claude.ai.
