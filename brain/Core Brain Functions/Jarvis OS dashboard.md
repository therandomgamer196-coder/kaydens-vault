---
tags: [jarvis, dashboard, reference]
aliases: [Jarvis dashboard, JARVIS OS]
created: 2026-09-23
---

# Jarvis OS dashboard — new main desktop dashboard

> [!important] New main desktop dashboard (2026-09-23)
> Jarvis OS is now also a Lively wallpaper, **"Jarvis OS"** (`...\Lively Wallpaper\Library\wallpapers\jarvisos.dash\jarvis-os.html`), meant to replace Punch In as the main desktop dashboard. To apply it: open Lively, click **Jarvis OS**, then click **Set as wallpaper**. It leaves room on the left for the desktop icons and at the bottom for the taskbar, and the orb animates even when Jarvis is offline. The panels need Jarvis running. **BRAIN GRAPH ↗** opens the 3D brain in the default browser through the bridge's `/os/open` route. Punch In (`punchin-v19.dash`) stays installed; switching back is one click in Lively. The daily 7 AM sync only writes to `punchin*.dash` folders. This wallpaper reads live data from Jarvis instead.

Jarvis's own control room, modelled on ethanplusai's JARVIS setup (TikTok, 2026-09-05) but built from Kayden's data. Open it from the **Jarvis Dashboard** shortcut on the desktop or in the Start menu (an Edge app window), or go to `http://127.0.0.1:8765/dashboard`. It only works while Jarvis is running.

## What's on it

| Tab | Shows | Comes from |
|---|---|---|
| **Home** | The Punch In clock (weekday, date, live time), the green network orb, what Jarvis last said and heard, response timings, and today's cards: next shift, pay this week, inbox, Robinhood, weather | `/status`, the wallpaper's dashboard data |
| **Runs** | Everything Jarvis heard and did, newest first: wake words, what he heard and how he classified it, apps opened, cut-ins, turn timings | `logs\launcher.jsonl`, `logs\wake_debug.log` |
| **Sessions** | Every Claude Code conversation on this PC from the last 7 days, marked running, waiting on you or idle | `~\.claude\projects\*\*.jsonl`, read-only |
| **Projects** | Jarvis, the Punch In dashboard and Kaydens Vault, with their latest activity | Jarvis files, [[Dashboard change log]], recent vault notes |
| **Specs** | The Jarvis OS roadmap phases and their status | [[Autonomous agent plan]] |
| **Memory** | Every note in `brain/`, readable in the dashboard | This vault |
| **Usage** | Claude Code tokens used in the last 5 hours and 7 days, by model | Claude Code transcripts. The exact plan percentages are only in Claude's Settings > Usage |

**BRAIN GRAPH ↗** (pill in the header) opens the full interactive 3D brain graph (`http://127.0.0.1:8765/brain`, served from `Brain Map\Jarvis Brain 3D.html`) in a new window. It now has 96 nodes, including the [[Agentic OS]] notes (2026-09-25). More: [[Jarvis Brain 3D]]. Websites can't load it.

**Shortcuts (desktop + Start menu):** **Jarvis Dashboard** opens this dashboard in an app window. **Jarvis Brain** opens this vault in Obsidian and switches to Graph view (`Jarvis\open-brain-graph.ps1`, through the Local REST API plugin's `graph:open` command; the key is read from the plugin at run time). The Punch In wallpaper also has an **OPEN JARVIS OS** button under the orb.

## The orb

`Jarvis\jarvis_orb.js` is one shared renderer used by both the dashboard and the Punch In wallpaper:
- a glowing green globe with a dense web of about 640 dots (380 on the wallpaper) and 34 swirling strands, some tinted blue as in the reference
- on the dashboard, Kayden's 82 Brain Map topics inside it as brighter nodes, with the lobe hubs labelled
- the live data as gold nodes: next shift, pay this week, inbox, Robinhood, weather
- **Idle:** slow drift. **Listening:** brighter and faster, and it breathes with the mic. **Speaking:** pulses with his voice, and sparks run along the strands.
- On the dashboard you can drag to rotate it and hover a node to read its note.

On the wallpaper it replaced the gold orb on 2026-09-23, and the Jarvis label, line, voice bars and response card turned green to match. The backup is `punch-in-wallpaper.html.bak-2026-09-23-pre-green-orb`.

## Files

`jarvis_dashboard.html` (the page), `jarvis_orb.js` (the orb), `jarvis_os.py` (the data behind `/os`, `/os/brain` and `/os/note`), `assets\jarvis-orb.ico` (the shortcut icon). The bridge serves the page and the orb to local callers only; the data routes follow the same website lock as `/status` (see [[Safety rules]]).

## Related

- Part of the [[Agentic OS]] project; log changes in [[Agentic OS change log]]. Other Agentic OS dashboard pieces: [[Jarvis Black Hole]], [[Jarvis Brain 3D]].
- [[Autonomous agent plan]] · [[Jarvis future plans]] · [[Voice and privacy]] · [[Dashboard change log]] (entries before 2026-09-25)
