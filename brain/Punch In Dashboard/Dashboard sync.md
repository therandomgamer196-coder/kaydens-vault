---
tags: [dashboard, reference]
---

# Dashboard sync

## Current setup (since 2026-09-22)

- **Scheduled task:** "Punch In daily sync (7 AM)" — id `trig_01DJvsxgtDnL4qEUUeV46dvz`, cron `0 11 * * *` (11:00 UTC = 7 AM EDT, 6 AM once clocks fall back), permission mode auto, requires Kayden's laptop, model claude-opus-5.
- **One run per day.** Viewing or re-reading the dashboard never costs tokens — the page only reads a local file. The token cost is this one run.
- **Paused, not deleted:** "Refresh Punch In dashboard" (`trig_01XS4doPEyBoNuKiBDqPyrUh`, was hourly at :19). Before 2026-09-22 the two tasks ran every hour = 48 runs/day.

## What one run does

1. **Calendar** — primary calendar, 00:00 today → +7 days (America/New_York). Finished events are included; the page hides them itself.
2. **Pay periods** — Papa John's ($12.50/hr, periods end Tuesdays) and Greenfield ($20/hr, periods end Fridays); each is a 14-day period found from payday-marker events, hours summed over the whole period.
3. **Gmail** — `is:unread in:inbox`, newest 15; flags security / account / bill mail, lists the rest as noise.
4. **Robinhood** — every account's value, holdings, day change, all-time realized P&L. Read-only.
5. **Weather** — Open-Meteo for Ephrata, PA (best effort; keeps the old value on failure).
6. **Writes** the artifact database (`dashboard/data`), then `punch-in-data.js` to `Documents\PunchIn` and to **every** `punchin*.dash` wallpaper folder (skips names containing "backup").
7. **Verifies** fresh file times. If the laptop is asleep/offline at 7 AM, only the artifact updates and the wallpaper keeps yesterday's data until the next run.

## Changing it

- Time or frequency: edit the cron on the scheduled task (UTC). Two runs a day: `0 11,19 * * *` (7 AM + 3 PM EDT).
- An extra run right now: fire the task on demand (costs one run).
- New data source: add a step to the task prompt **and** a field to [[Dashboard data schema]] **and** a renderer in the page — then log it in [[Dashboard change log]].

## Verified 2026-09-22

Synced figures matched the live connectors: Robinhood Individual −$0.44 (−$0.97 margin cash + ~$0.53 SOL), Agentic $4.99 cash, total $4.55; Gmail 201 unread.
