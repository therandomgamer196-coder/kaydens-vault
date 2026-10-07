---
tags: [agentic-os, changelog]
---

# Agentic OS change log

> [!important] Rule
> Every change to Jarvis, the Jarvis OS dashboard or the Jarvis visuals gets an entry here: the date, what changed, its parameters, the files touched, and how to undo it. Newest first. Changes to the Punch In wallpaper go in [[Dashboard change log]]. Jarvis changes from before 2026-09-25 are still in that log.

## 2026-10-07

**Hybrid brain (free everyday, Opus on "think hard") + brain synced to GitHub (9:25 AM)**
- **Free fast brains** (new `jarvis_freebrain.py`): Groq `openai/gpt-oss-120b`, then Cerebras `gpt-oss-120b`, both on low reasoning for speed. They have the same tools as the Opus brain, plus free web tools.
- **Routing** (`provider_order` in `jarvis_bridge.py`):
  - everyday: Groq, then Cerebras, then local llama3.2
  - "think hard", "research", "deep dive", "in depth", "take your time" or "use Opus": Opus 5.5 first
  - `JARVIS_CLAUDE_EVERYDAY=1` puts Opus first for everything, and `JARVIS_LLM_PROVIDERS` sets a fixed order
- **Free web tools** (new `jarvis_web.py`): DuckDuckGo search (with Wikipedia as backup) and page reading. Anything resolving to this PC or the home network is refused (SSRF guard, redirects checked too).
- **Keys:** one file, `secrets\keys.env` (`GROQ_API_KEY`, `CEREBRAS_API_KEY`, `ANTHROPIC_API_KEY`), read on every question. `anthropic.env` is still read too.
- **Brain sync** (new `jarvis_vaultsync.py`):
  - The vault is now a git repo: the first commit has 168 files, the remote is `github.com/therandomgamer196-coder/kaydens-vault`, and there's a `.gitignore`.
  - Every 5 min the bridge commits, pulls (rebase + autostash) and pushes, without ever showing a sign-in prompt. A conflict is rolled back and shown in `/status` → `vault_sync`.
  - The one-time sign-in is done with `connect-brain-to-github.cmd`.
- `/status` new fields: `free_brains`, `vault_sync`, `vault_sync_at`.
- **Checks:** all 10 suites pass (292 checks; new `test_freebrain.py` 16 and `test_vaultsync.py` 10). A live DuckDuckGo search and page read worked on the laptop. Restarted 9:23 AM: ready, model loaded. Vault sync is waiting on the GitHub sign-in, as expected.
- **Waiting on Kayden:** [[Jarvis Setup Checklist]] steps 1–5.
- **Undo:** `backups\jarvis_bridge.py.2026-10-07-pre-hybrid` and `backups\jarvis_agent.py.2026-10-07-pre-hybrid`, then restart. Sync off: `JARVIS_NO_VAULT_SYNC=1`.

## 2026-10-06

**Opus 5.5 brain, live vault access, own notes, always-loaded local model, orb v2 (3:50 PM)**
- **Deep brain** (new `jarvis_agent.py`): questions the instant answers don't cover go to **Claude Opus 5.5**, with adaptive thinking and high effort (`JARVIS_CLAUDE_MODEL`, `JARVIS_CLAUDE_EFFORT`).
  - **Tools:**
    - `search_brain`: live search of every note, re-scanned every 3 s
    - `read_note`
    - `list_recent_notes`
    - `write_note`: creates or appends notes, **only** in `brain/Jarvis Notes/`, with frontmatter and a link from [[Jarvis Notes]]
    - Anthropic's `web_search` (3 per question) and `web_fetch` (2), for when the brain lacks the answer
  - **Safety:** nothing is ever deleted, and he can't write outside Jarvis Notes. Note and web text is treated as data.
  - **Speed:** answers stream sentence by sentence. If nothing comes within 2.5 s he says "One moment, sir."
  - **Fallback:** no key, offline, or an API error → the local llama3.2 answers.
  - **Waiting on Kayden:** the API key in `Jarvis\secrets\anthropic.env`. See [[Jarvis Cloud Setup]].
- **Local model stays connected:**
  - The real reason the language model kept dropping: the **Ollama** and **Lively** startup entries were disabled, so after a reboot Ollama never started. Both are re-enabled.
  - `keep_alive` is now `-1`, so llama3.2 stays on the RTX for good (`ollama ps` → Forever).
  - A new `llm_guard` thread checks every 60 s: it starts Ollama if it's down and reloads the model if it was unloaded. `/status` shows `llm` (loaded/idle/offline) and `claude` (ready/no key).
- **Claude Code** now defaults to **Opus 5.5, high effort** (`~/.claude/settings.json`: `model`, `modelSettings.claude-opus-5-5.effortLevel`; backup `settings.json.bak-2026-10-06`). Verified: a test run reported `claude-opus-5-5`.
- **Orb v2** (`jarvis_orb.js`, shared by the dashboard and the v19 wallpaper):
  - 3–4× cheaper per frame: 0.6–0.9 ms against 2.1–2.3 ms in headless Chromium
  - depth-bucketed batch drawing, a cached glow sprite, a 60 fps cap, auto detail drop, and a pause when the page is hidden
  - **Looks:** HUD rings with rotating arcs, a scan sweep (listening and thinking), ripples while speaking, a core glow, twinkles, and eased mode changes
  - **New `thinking` mode**, from the bridge's `phase`
- **Checks:** 266/266 tests (new `tests\test_agent.py`, 26 checks, with a fake Claude API covering the tool loop, the thinking signature, filler and fallback). Restarted 3:50 PM: ready, `llm guard: local model loaded`.
- **Files:**
  - new: `jarvis_agent.py`, `secrets\anthropic.env`, `tests\test_agent.py`
  - changed: `jarvis_bridge.py`, `jarvis_brain.py`, `jarvis_orb.js`, `jarvis_dashboard.html`, `tests\run_tests.py`
- **Undo:**
  - Opus off: `JARVIS_LLM_PROVIDERS=ollama`, or empty the key file.
  - Orb: `backups\jarvis_orb.js.2026-10-06-pre-v2` and `backups\jarvis_dashboard.html.2026-10-06-pre-v2`.
  - Bridge: `backups\jarvis_bridge.py.2026-10-06-pre-chatter` (that undoes the chatter filter too).

**Bridge back online + TV/room-chatter filter (3:25 PM)**
- **Why "Bridge unavailable":** from Sep 24 the Jarvis startup entry was disabled, so after each reboot (9 since Oct 4) neither the bridge nor the watchdog started. Kayden asked for him back online: the startup entry was turned back on and the watchdog started. `/status` answers in about 10 ms when healthy, so the bridge itself was never slow.
- **Chatter filter** (`jarvis_conversation.py`): the log showed the wake model firing on TV voices at scores 0.35–0.50, and Whisper turning the show into "commands" (Sep 24: ~40 of ~70 sessions). Now:
  - a **weak wake** (first frame scored under `JARVIS_STRONG_WAKE_SCORE`, 0.6) is answered only if the first thing heard sounds said to Jarvis. That means short (≤ 14 words) and starting like a question or instruction ("open…", "what's…", "can you…", "sync…", "good morning"…). Otherwise the session ends quietly as `chatter`.
  - a **monologue** (> `JARVIS_MAX_COMMAND_WORDS`, 30 words) or a stuck-record transcript ("st st st st", "thank you thank you…") is never a command.
  - a **follow-up that cuts him off** must also sound directed, or it counts as junk; two junk turns end the session.
  - Logs show `-> chatter (weak wake 0.36)` and `session N ended: chatter`.
- **Checks:** 9 new real-log tests; whole suite **240/240 pass** (`tests\run_tests.py`). Restarted 3:24 PM; ready=True in ~7 s.
- **Files:** `jarvis_conversation.py`, `jarvis_bridge.py` (passes the wake score), `tests\test_conversation.py`.
- **Undo:** copy `backups\jarvis_conversation.py.2026-10-06-pre-chatter` and `backups\jarvis_bridge.py.2026-10-06-pre-chatter` back, then `restart-jarvis.cmd`. Or keep the code and set `JARVIS_STRONG_WAKE_SCORE=0` to turn off the weak-wake check.
- Wallpaper side of this fix: [[Dashboard change log#2026-10-06]].

## 2026-09-25

**New Jarvis Galaxy desktop shortcut: the black hole in a normal Edge browser window (4:17 AM)**
- **What:** a new **Jarvis Galaxy** shortcut on the Desktop opens the black hole page in a regular Microsoft Edge browser window, with tabs and an address bar, on the RTX 4050. It uses the same profile (`%LOCALAPPDATA%\JarvisBlackHole`) and flag (`--force_high_performance_gpu`) as the **Jarvis Black Hole** shortcut, but without `--app`. It adds `--new-window --start-maximized`. The **Jarvis Black Hole** shortcut is unchanged and still opens the same page as an app window.
- **Icon:** `Jarvis\assets\jarvis-orb.ico`, the same as the other Jarvis shortcuts.
- **Checked:** launched it; the Edge browser process has no `--app`, opens `jarvis-black-hole.html` and has the RTX flag, and `nvidia-smi` lists `msedge.exe`.
- **Files:** `C:\Users\NCG\OneDrive\Desktop\Jarvis Galaxy.lnk` (new).
- **Undo:** delete `Jarvis Galaxy.lnk` from the Desktop.

**Jarvis Black Hole: 3:53 AM cloud build pulled down and opened on the RTX, plus a website folder (4:00 AM)**
- **What happened:** the artifact was republished from a cloud session at 3:53 AM (artifact version `1790322807-64f8`, 6.5 MB), but the local page was still v8 from 2:29 AM. The cloud build was copied over `Jarvis\assets\jarvis-black-hole.html`, so the two are now byte-identical (SHA-256 `f8f23b44…6ce4`).
- **What the cloud build adds** (from its code):
  - Menu tabs: Mode, Travel, Style, Earth and Display.
  - Travel to the binary core, the Sun, Mercury, Venus, Earth, the Moon, Mars, Jupiter, Saturn and more. Planet positions come from Astronomy Engine 2.1.19, loaded from jsDelivr.
  - Earth's NASA Blue Marble and Black Marble imagery is built into the page.
  - Close-ups stream Esri World Imagery (down to about 0.3 m per pixel), though not inside the Claude viewer.
  - Live EUMETSAT satellite clouds (clouds.matteason.co.uk), refreshed every 3 hours.
  - Place search: Photon, with OpenStreetMap Nominatim as the fallback.
  - Overlays: an "AI network across the sky" and cinema bars. Every source is credited on screen.
- **Opened on the RTX:** `open-on-rtx.ps1 -Restart`; `nvidia-smi` lists `msedge.exe`.
- **Website:** the new folder `Jarvis\website\` holds `index.html`, a copy of the page, ready to host at jarvisgalaxy.com. At 4:00 AM the domain had no DNS records, so it's probably unregistered. Nothing is bought or published yet: Kayden buys the domain and chooses the host. The page never calls localhost or the bridge, so it's safe to host publicly.
- **GPU check:** the Claude app is now set to High performance in Windows (`claude.exe` shows in `nvidia-smi`). Opera GX's High performance entry is on its installer (`OperaGXSetup.exe`), not on `opera.exe`, so Opera GX still draws on the Intel chip.
- **Files:** `Jarvis\assets\jarvis-black-hole.html` (backup `.bak-2026-09-25-v8`), `Jarvis\website\index.html` (new).
- **Undo:** copy the v8 backup over the page and run `open-on-rtx.ps1 -Restart`. The artifact still holds the cloud build, so republish the backup there as well. Delete `Jarvis\website\` to remove the website folder.

**Jarvis Black Hole v8: real Earth, Space-bar look, travel, weather and zoom detail (3:00 AM)**
- **Look:** tap **Space** and it stays on; hold it and it's on only while held (Esc also stops it). The mouse is captured and the view eases after it. There's no more edge-turning, and no more drifting back on its own. The camera only orbits the hole while you're "home"; **R** or **HOLE** takes you back.
- **Travel:** HOLE / EARTH / GIANT / DUNE WORLD fly you there on a smooth arc and end on the sunlit side. Scroll speed scales with the distance to the nearest surface, so you can glide down to about 250 m above Earth. Drag orbits whatever world you're near.
- **Earth replaces the ocean world.** It uses NASA GIBS imagery, which is public domain; Google Earth's imagery can't legally be copied into the page.
  - Day colour: Blue Marble Next Generation.
  - Night: VIIRS Black Marble city lights.
  - Coastlines and water: the OpenStreetMap land/water mask.
  - Resolution: a global layer at about 10 km per pixel, plus two detail windows that load as you fly in, down to 500 m per pixel. Below that, procedural ground detail takes over.
  - It is turned to the **real current time and season**, so the lit side is the one lit right now: the subsolar point comes from the UTC time, solar declination and the equation of time.
- **Earth weather and effects:**
  - climate bands: equatorial rising air, dry subtropics, storm tracks
  - trade winds and westerlies moving the clouds
  - five spiral storms turning the right way for their hemisphere, with clear eyes
  - cloud shadows
  - lightning in storm clouds at night
  - sun glint off wave-roughened oceans
  - city lights dimmed under cloud
  - auroras round the real geomagnetic poles
  - a blue limb and sunset colours along the terminator
- **Other planets:** new zoom detail and weather.
  - Gas giant: bands sheared by zonal winds into eddies, a great storm with spiral lanes, and lightning on the night side.
  - Dune world: dune ridges, craters and turbulent dust-storm fronts.
  - Moon: maria, and craters at six sizes that appear as you get closer.
  - Asteroids: craters and fine bumps.
- **Artifact limit:** the claude.ai artifact can't load NASA tiles (its security policy), so Earth there shows a simplified stand-in. The RTX window shows the real imagery.
- **Files:** `Jarvis\assets\jarvis-black-hole.html` (backups `.bak-2026-09-25-v7`, `-v8a`); artifact Version 9.
- **Next:** volumetric 3D nebulae, comet and sun, then a performance pass.

**Jarvis Black Hole v7: deep space you can fly through (2:05 AM)**
- **Camera:** it follows the mouse to look around; hold the mouse near an edge to keep turning. Scroll flies forward and back, drag orbits the hole. **R** or RECENTER goes back to the hole, **L** or MOUSE LOOK turns look-around on and off. After 20 s without input the view drifts back to the hole. You can't fly into the hole (r ≥ 3.6) or into a planet.
- **3D around the hole:**
  - A ringed gas giant, with ring shadows, a great storm and a Cassini-like gap.
  - An ocean world with a sun glint, blue limb, drifting clouds and animated auroras, plus its orbiting moon.
  - A desert world with a drifting dust storm.
  - An asteroid belt (r 34–74) lit by the sun and the disk.
  - All of them are lensed when they pass behind the hole.
- **Sky:** six star layers with real star colours, a faint Milky Way with dust lanes, distant galaxies, and two far-off planets.
- **Space weather and phenomena:**
  - the Helix Nebula
  - Pillars of Creation-style columns
  - a Crab-like remnant with a pulsar flashing and sweeping its beams
  - a spiral galaxy
  - a comet with ion and dust tails
  - a sun with flares and a coronal mass ejection every ~26 s
  - the planet auroras and dust storm above
- **Realism:**
  - thin-disk brightness that peaks just outside the innermost stable orbit (r = 3)
  - colour from the Doppler-shifted temperature
  - seamless lensing everywhere (the same bending maths inside and outside the marched region)
- **New ORIGINAL B/W colourway:** a true monochrome film look.
- **Colour:** fuller and brighter overall: exposure 1.05 → 1.22, a saturation boost, and vibrance that lifts muted colours most. The blacks stay deep.
- **Mode buttons:** disk spin (1 / 1.6 / 2.15×), the lights and the camera drift glide to their new speed on a spring. A surge of light on each change. The active button breathes, and the header shows the live SPIN value.
- **Files:** `Jarvis\assets\jarvis-black-hole.html` (backup `.bak-2026-09-25-v6`); artifact Version 7.
- **Undo:** copy the v6 backup over the page, then run `open-on-rtx.ps1 -Restart`.
- **Next:** the nebulae, comet and sun are drawn on the sky at infinity (no parallax). Making them true 3D volumes is the next step.

**Agentic OS project created in the vault (1:40 AM)**
- New folder `brain/Agentic OS/`: [[Agentic OS]] (the project index, with every link), this change log, [[Jarvis Black Hole]] and [[Jarvis Brain 3D]]. Linked from [[Jarvis Brain]].
- The black hole entry below moved here from the Punch In [[Dashboard change log]]. It isn't a Punch In change.
- The new notes were added to the 3D brain page, and its artifact was republished.

**Jarvis Black Hole v6: gravity-driven lights, no rake, deeper blacks, sharper resolution (1:35 AM)**
- **Lights:**
  - Four small lights, each pulled by the hole (Paczyński–Wiita gravity, GM 45). They swing in to r≈3.6 and out to 8–9.5, and their orbits precess.
  - Each has a white-hot head and a thin rainbow tail, 0.42 s long, thinning from 0.024 to 0.009.
  - Every 2.5–8.5 s a light races at 2.3–3.7× speed for 0.45–1 s. Its tail stretches and brightens meanwhile.
- **The "rake" is gone.** It had two causes:
  - The lens streak sampled every 4th texel, so each light left a dotted horizontal line. Its taps are now closer than the blur.
  - The old tails were estimated from a circle point at each ray step, which broke into teeth. Tails are now exact: the closest approach between each ray step and each tail segment.
- **Deeper blacks:**
  - Bloom comes only from bright light (soft threshold 0.05).
  - A toe curve after the ACES film curve.
  - Grain only on lit pixels.
  - Dimmer galaxy band (0.2 → 0.11) and nebula (0.04 → 0.012).
  - Stronger vignette (0.6 → 0.7).
- **Resolution:**
  - On the RTX it starts at 1.25× and climbs to 2× while a frame stays under 9.5–13 ms of GPU time (60+ fps).
  - Below 1×, a sharpen pass restores edges.
  - Intel graphics still start in SMOOTH, and the HUD tells you to use the shortcut.
- **Tools:** new `Jarvis\open-on-rtx.ps1` opens any page in the RTX Edge window. Artifact Version 6, pinned in the claude.ai sidebar.
- **Checks:** checked in headless Edge (shaders compile; screenshot clean). Running on the RTX: `nvidia-smi` lists `msedge.exe`.
- **Files:** `Jarvis\assets\jarvis-black-hole.html` (backup `jarvis-black-hole.html.bak-2026-09-25`), `Jarvis\open-on-rtx.ps1` (new).
- **Undo:** copy the backup over the page, then run `open-on-rtx.ps1 -Restart`.

**Jarvis Black Hole: cinematic WebGL prototype, running on the RTX 4050** (moved from the Punch In dashboard log)
- **What it is:** a live 3D black hole with a lensed accretion disk, photon ring, orbiting rainbow light trails, HDR bloom, and adaptive supersampling up to 2×. It has four colourways and Jarvis's idle, listening and speaking modes. It's a candidate look for Jarvis's orb or a dashboard background.
- **Where it lives:** published as the claude.ai artifact [Jarvis Black Hole](https://claude.ai/artifact/TyaawfYELEMKHSPZnddJay). There's also a local copy at `Jarvis\assets\jarvis-black-hole.html`.
- **Lag fix:**
  - The Claude app and Opera GX run on the Intel graphics, because neither has a Windows graphics preference.
  - The new **Jarvis Black Hole** shortcut (desktop and Start menu) opens the page in its own Edge app window with `--force_high_performance_gpu` and a separate profile (`%LOCALAPPDATA%\JarvisBlackHole`). `nvidia-smi` confirmed `msedge.exe` on the RTX.
  - To put Claude or Opera on the RTX as well, Kayden sets them to High performance in Settings → System → Display → Graphics.
- **Undo:** delete the shortcut and `%LOCALAPPDATA%\JarvisBlackHole`.
