---
tags: [dashboard, reference]
---

# Dashboard UI and parameters

Everything below is in `punch-in-wallpaper.html` (v19). The artifact runs the same code.

## Panels

| Panel | Shows | Source |
|---|---|---|
| Header | weekday, date, clock (America/New_York), search bar (Opera/Google), Jarvis command box | clock ticks every 10 s |
| Stats row | **Next shift** + countdown, **Est. pay · 7 days** (hours × rate over listed shifts), **Synced** age (turns "stale" after 5 h) | `events`, `updatedAt` |
| **Up next** | Legend (Shift / Bill / Pay day / Personal), then **"Today · <Weekday>, <Mon D>" always first**, then up to 6 upcoming rows grouped by day | `events` |
| Robinhood | total, per-account value + holdings note, today's change, realized P&L; click opens robinhood.com | `robinhood` |
| Inbox | unread total, flagged highlights (Security / Account / Bill) — click opens Gmail thread | `inbox` |
| Weather | current + 3-day + next 6 hours | **live** from Open-Meteo every 30 min (wallpaper only), else `weather` |
| Jarvis orb | status from the local bridge `http://127.0.0.1:8765` | bridge `/status` |

## Up next rules (2026-09-22)

- Today's header is always shown, even with nothing on — then "Nothing else today" (today had events that are done) or "Nothing scheduled today".
- An event disappears once its **end** time passes (all-day events stay until midnight). The list re-renders every 60 s, so it stays current all day with no sync.
- An event still running from yesterday is filed under Today.
- Labels: "Today · Tuesday, Sep 22", "Tomorrow · Sep 24", otherwise "Thursday · Sep 24".

## Constants

| Name | Value | Meaning |
|---|---|---|
| `MAX_ROWS` | 6 | schedule rows shown |
| `REFRESH_MS` | 5 min | re-read `punch-in-data.js` |
| re-render | 60 s | countdowns, dropping finished events, midnight rollover |
| weather | 30 min | Open-Meteo fetch (lat 40.1801, lon −76.1785) |
| version check | 2 min | reload when `punch-in-version.js` changes |
| Papa John's rate | $12.50/hr | matched by title "papa john" |
| Greenfield rate | $20.00/hr | matched by "wedding", "event", "greenfield" |
| Timezone | America/New_York | all dates/times |

## Colors (CSS variables)

Cherry `--cherry` = shifts and Today; amber `--amber` = bills; mint `--mint` = pay days and money; lilac `--lilac` = personal; `--ink-faint` = muted text. Theme: dark obsidian with cherry red, glossy liquid background with colored bubbles.

## Artifact-only behaviour

When the page runs inside claude.ai (`window.claude` exists) it subscribes to the artifact database doc `dashboard/data` and renders from it. On the wallpaper that code does nothing.

## Mouse behaviour

Lively forwards clicks: rows open Google Calendar / Gmail / Robinhood in a new window (never navigates the wallpaper itself). The Jarvis icon suppresses left-click navigation on purpose.
