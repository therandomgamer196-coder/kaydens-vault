---
tags: [dashboard, changelog]
---

# Dashboard change log

> [!important] Rule
> Every change to the Punch In dashboard (page, data, sync, or its Jarvis link) gets an entry here: date, what changed, parameters, files touched, and how to undo it. Newest first.
> Since 2026-09-25, changes to Jarvis himself, the Jarvis OS dashboard and the Jarvis visuals (such as the black hole) go in [[Agentic OS change log]]. See [[Agentic OS]].

## 2026-10-06

**Jarvis orb v2 on the v19 wallpaper (3:48 PM)**
- The inlined orb is now the shared orb v2: smoother and 3–4× cheaper per frame, with HUD rings, a scan sweep, ripples while speaking, and eased mode changes. The poll adds `talking` and the new `thinking` class from `/status.phase`.
- **Tested first in the artifact** (Version 32, which also replaced the artifact's old gold orb). Off this PC the artifact cycles idle → listening → thinking → speaking every 3.5 s; on the PC, `#orb-demo` does the same. Checked in headless Chromium with no page errors, and every script block passes `node --check`.
- **Files:** `punchin-v19.dash\punch-in-wallpaper.html` (orb block + `initJarvisOrb3D` + poll), `punch-in-version.js` → `20261006-orb-v2-1`. Swap script: `Jarvis\backups\orb-v2\deploy_orb.py`.
- **Undo:** copy `punch-in-wallpaper.html.bak-2026-10-06-pre-orb-v2` over the page and bump `punch-in-version.js`.
- **Startup:** Lively's sign-in startup entry had been disabled. It's re-enabled, so the v19 wallpaper comes back after every reboot.

**Jarvis poll guard on the v19 wallpaper (3:20 PM)**
- **Before:** the orb polled `/status` every 1.5 s with no timeout. One slow or failed answer flipped it to "Bridge unavailable" right away, and slow answers stacked up to 4 requests at once.
- **Now:** one request at a time, a 4 s timeout (`POLL_TIMEOUT_MS`), and "offline" only after 3 failures in a row (`OFFLINE_AFTER`). The text reads "Bridge unavailable · reconnecting…".
- **Tested first in the artifact** (Version 31) and in headless Chromium against a fake bridge:
  - one failed poll: stays "ready"
  - a 6 s stall: 1 request in flight, offline after ~12 s
  - down: offline after ~5 s
  - back up: "ready" within one poll
  - The old code flickered offline/ready and stacked 4 requests.
- **Files:** `punchin-v19.dash\punch-in-wallpaper.html` (the poll in the Jarvis block), `punch-in-version.js` → `20261006-poll-guard-1`. The page reloads itself within 2 min.
- **Undo:** copy `punch-in-wallpaper.html.bak-2026-10-06-pre-poll-guard` over the page and bump `punch-in-version.js`.
- Jarvis side: [[Agentic OS change log#2026-10-06]].

## 2026-09-23

**"OPEN JARVIS OS" button on the Punch In wallpaper (1:10 AM)**
- A green pill under the Jarvis orb (top right) opens the Jarvis OS dashboard in its own app window, using the same Edge window as the desktop shortcut, through the bridge's `/os/open?what=dashboard`. If Jarvis is offline, it opens `127.0.0.1:8765/dashboard` in a browser tab instead.
- Files: `punchin-v19.dash\punch-in-wallpaper.html` (CSS `.jarvis-os-btn`, button, `initJarvisOsButton`), `punch-in-version.js` → `20260923-os-button-1`, `Jarvis\jarvis_bridge.py`.
- Undo: copy `punch-in-wallpaper.html.bak-2026-09-23-pre-os-button` over the page and change `punch-in-version.js`.

**New main desktop dashboard: "Jarvis OS" Lively wallpaper + brain graph pill (1:00 AM)**
- New Lively wallpaper `jarvisos.dash` ("Jarvis OS"): the Jarvis OS dashboard laid out for the desktop, clear of the icon columns and the taskbar. Lively was restarted so it appears in the library; Kayden applies it himself. See [[Jarvis OS dashboard]].
- The dashboard header now has a **BRAIN GRAPH ↗** pill that opens the full 3D brain (`/brain`, 90 nodes). New bridge routes: `/brain`, and `/os/open?what=brain|dashboard`, which opens only those fixed pages.
- The dashboard clock is now 12-hour. The car savings and college cards were removed.
- Undo: in Lively, set Punch In back as the wallpaper and delete the `jarvisos.dash` folder. Bridge backups are in `Jarvis\backups`.

**Green network orb on the wallpaper and the Jarvis OS dashboard (12:35 AM)**
- Wallpaper: the gold particle orb was replaced by the shared green globe (`Jarvis\jarvis_orb.js`, inlined). A new `talking` class makes it pulse while Jarvis speaks. The Jarvis HUD colours (label, line, voice bars, response card) went from amber to green. Version beacon: `20260923-green-orb-1`.
- New dashboard at `http://127.0.0.1:8765/dashboard`, with desktop and Start menu shortcuts. See [[Jarvis OS dashboard]].
- Not done: the Terminal / Claude Code panel. Claude Code's safety check blocked connecting it; see [[Jarvis future plans]]. The artifact test copy still has the gold orb.
- Files: wallpaper page and `punch-in-version.js`; Jarvis `jarvis_orb.js`, `jarvis_dashboard.html`, `jarvis_os.py`, `jarvis_terminal.py` (not connected), `jarvis_bridge.py` (the `/dashboard`, `/orb.js`, `/os` routes), `assets\jarvis-orb.ico`.
- Undo the wallpaper: copy `punch-in-wallpaper.html.bak-2026-09-23-pre-green-orb` over the page and change `punch-in-version.js`. Undo the bridge: `backups\jarvis_bridge.py.2026-09-23-pre-piper`, then restart.

**Offline voice (Piper) and Qwen model (12:15 AM)**
- Jarvis now speaks with Piper `en_GB-alan-medium`, fully offline (`models\piper\`, 63 MB; `pip install piper-tts` 1.8.0). A 6-second sentence takes about 0.5 s to generate. If Piper fails, Edge (`en-GB-RyanNeural`) speaks instead. Switch back with env `JARVIS_TTS=edge`.
- Downloaded `qwen2.5:7b` (4.7 GB) but kept `llama3.2` for talking. In a test on real questions, Qwen took 3–15 s per answer, used lists and made up pay figures, while llama3.2 answered in under 1 s and correctly. Qwen is kept for the upcoming tool-choosing agent. To try it anyway, set `JARVIS_OLLAMA_MODEL=qwen2.5:7b`.
- Jarvis's briefing now includes each shift's hours and pay, so the model never does the maths itself.
- Files: `jarvis_voice.py`, `jarvis_bridge.py`, `jarvis_brain.py`, tests. 207/207 checks pass. Restarted; the audible test passed.
- Undo: `backups\jarvis_bridge.py.2026-09-23-pre-piper` over `jarvis_bridge.py`, or just set `JARVIS_TTS=edge`, then `restart-jarvis.cmd`.

## 2026-09-22

**Jarvis conversation rebuilt: one voice, cut-in, faster, more accurate (11:55 PM)**
- Fixes: "multiple Jarvises speaking" (every wake-word frame could start another session; replies overlapped), the stuck-`speaking` / room-chatter bug (he listened while talking and transcribed his own voice), response windows never closing.
- New: talk over him to cut him off (or say "Hey Jarvis"); "shut up" / "stop" / "close" / "cancel" / "never mind" silence him and close all response windows; 2 s with no words after he finishes closes the window; follow-up questions keep context for 10 min; exact instant answers for time, date, shifts, weather, unread mail; `/stop` kill switch; muting also stops speech.
- Faster: speech-to-text preloaded at start-up, "Yes, sir?" cached, Ollama called directly and streamed (spoken sentence by sentence), model kept loaded 30 min, Edge's silence padding trimmed. Measured: warm follow-up answer 0.5 s from the model; speech-to-text 0.66 s; Edge voice 0.3–1.4 s (the slowest step now).
- Accuracy: the model gets a short plain-English briefing instead of raw JSON, plus About Kayden; stale synced weather no longer overwrites the live reading.
- Parameters (env vars): `JARVIS_FOLLOW_UP_SECONDS=2`, `JARVIS_FIRST_WORDS_SECONDS=3` (after "Yes, sir?"), `JARVIS_END_OF_SPEECH_SECONDS=0.7`, `JARVIS_BARGE_IN=1`, `JARVIS_BARGE_IN_FACTOR=3`, `JARVIS_OLLAMA_KEEP_ALIVE=30m`, `JARVIS_LLM_PROVIDERS=ollama` (OpenAI fallback now off by default).
- Files: new `jarvis_conversation.py`, `jarvis_voice.py`, `jarvis_brain.py`; `jarvis_bridge.py`, `jarvis_interface.html`, tests (`test_conversation.py`, `test_brain.py`, `voicefakes.py`, `test_security.py`, `fakes.py`, `run_tests.py`). 202/202 checks pass; restarted; audible `/speak` test OK; live typed test closed the window 2.3 s after he finished.
- Undo: copy `backups\jarvis_bridge.py.2026-09-22-pre-conversation` over `jarvis_bridge.py` and `backups\jarvis_interface.html.2026-09-22-pre-close` over `jarvis_interface.html`, then `restart-jarvis.cmd` (the three new files can stay; the old bridge doesn't use them).

**Jarvis opens any app or website (11 PM)**
- New `Jarvis\jarvis_launcher.py`: "pull up youtube.com" → default browser; "open YouTube" → installed app, else the website; aliases in new `Jarvis\jarvis_aliases.json`. Replaces the old five-item `open` list in `handle_command`. New dry-run endpoint `/preview?text=`. Launches logged to `logs\launcher.jsonl`. See [[Voice and privacy]].
- Parameters: Start menu re-read every 10 min, or after a miss once 30 s have passed; match score ≥ 50; uninstallers/document shortcuts never launched.
- Files: `jarvis_bridge.py`, `jarvis_launcher.py` (new), `jarvis_aliases.json` (new), `tests\run_tests.py`, `tests\test_launcher.py` (new), `tests\test_security.py` (new). 90/90 tests pass. Restarted with `restart-jarvis.cmd`; `/health` ready.
- Undo: copy `backups\jarvis_bridge.py.2026-09-22-pre-launcher` over `jarvis_bridge.py` (and `backups\run_tests.py.2026-09-22-pre-launcher` over `tests\run_tests.py`), then `restart-jarvis.cmd`.

**Bridge locked to this PC — websites refused (11 PM)**
- Before: every response had `Access-Control-Allow-Origin: *` and commands ran from a plain GET, so any website open in the browser could send Jarvis commands and read `/status` (inbox subjects, Robinhood totals). Now only the wallpaper, the command centre and local tools are accepted; see [[Safety rules]].
- The wallpaper's real origin is Lively WebView2's `https://7364286255b74fbc.localhost` — any `https://*.localhost` origin is allowed. The first restart only allowed `null`, which blocked the wallpaper's orb for ~2 minutes (23:05–23:07) until fixed.
- Check: `logs\wake_debug.log` shows `caller allowed: GET /status origin='https://7364286255b74fbc.localhost'`.
- Undo: same backup as above.

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
