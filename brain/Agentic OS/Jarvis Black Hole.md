---
tags: [agentic-os, dashboard, visual]
aliases: [black hole, Jarvis singularity]
created: 2026-09-25
---

# Jarvis Black Hole

> [!info] Label: dashboard. Part of [[Agentic OS]].

A live, cinematic 3D black hole. Light bends around it, a glowing gas disk spins, and four small rainbow lights fall around it under its gravity. It reacts to Jarvis's idle, listening and speaking modes. It's a candidate face for Jarvis's orb or a background for the dashboard.

> [!note] Latest build
> The current page is the cloud build from 2026-09-25, 3:53 AM. It adds menu tabs, travel to the Sun and planets, live satellite clouds, Esri close-up imagery and place search. "What's in it" below still describes v6; see [[Agentic OS change log]] for v7, v8 and the cloud build.

## Open it

| Way | Link | Runs on |
|---|---|---|
| **Jarvis Black Hole** shortcut (Desktop + Start menu) | Edge app window with `C:\Users\NCG\Documents\Jarvis\assets\jarvis-black-hole.html` | RTX 4050, full quality |
| **Jarvis Galaxy** shortcut (Desktop) | the same page in a normal Edge browser window, with tabs and an address bar | RTX 4050, full quality |
| Script | `Jarvis\open-on-rtx.ps1` (add `-Restart` after an edit) | RTX 4050 |
| Artifact (pinned in the claude.ai sidebar, always the newest version) | https://claude.ai/artifact/TyaawfYELEMKHSPZnddJay | whatever GPU the browser uses. The Claude viewer also blocks the Esri close-up imagery, so the RTX window is the full-quality view |
| Website (not live yet) | `Jarvis\website\index.html`, for jarvisgalaxy.com once the domain is bought and hosted | the visitor's GPU |

## What's in it

- **The hole:**
  - Light rays are bent step by step, so there's a real shadow, a photon ring at 1.5× the horizon, and lensed stars behind it.
  - The disk is volumetric gas. It spins faster inside than outside and brightens on the side coming toward you (Doppler). It reddens near the hole.
- **The lights:** four small bright bodies, each pulled by the hole. Their orbits swing in to about 3.6 and back out to 8–9.5, and they slowly precess.
  - Each has a white-hot head and a thin rainbow tail, 0.42 s long, that thins and fades.
  - Every 2.5–8.5 s one races at 2.3–3.7× speed for 0.45–1 s. Its tail stretches and brightens while it does.
- **Camera look:**
  - 16-bit HDR, soft bloom from bright light only, and a smooth anamorphic lens streak.
  - ACES film curve with a toe for deep blacks.
  - Light lens colour fringing, grain only on lit pixels, and a vignette.
- **Buttons:**
  - Modes: IDLE / LISTENING / SPEAKING.
  - Colourways: JARVIS GREEN / EVENT GOLD / CRIMSON / NEBULA.
  - Quality: AUTO MAX / ULTRA 2× / SMOOTH / LITE.
  - FULL or a 2.39:1 letterbox, and FULLSCREEN.
- **Controls:** drag to orbit (it keeps drifting), scroll to zoom, **H** hides the interface, **F** or double-click for fullscreen.
- **HUD (top right):** render size and scale, FPS, GPU milliseconds per frame, GPU name.

## Resolution

AUTO MAX renders somewhere between 0.35× and 2× the screen resolution. On the RTX it starts at 1.25× and settles where a frame costs 9.5–13 ms of GPU time: as sharp as possible while still running at 60+ fps. That tops out at 2×, which is 4K on a 1080p screen. Below 1× a sharpen pass restores the edges. On Intel graphics it starts in SMOOTH (0.6×).

## Key parameters

| Parameter | Value |
|---|---|
| Camera distance / zoom range | 30 / 16–48 |
| Ray steps (AUTO MAX · ULTRA · SMOOTH · LITE) | 200 · 280 · 150 · 110 |
| Light gravity | GM 45, Paczyński–Wiita, 240 steps per simulated second |
| Tail width (head → end) | 0.024 → 0.009; head 0.03 |
| Bloom / streak / exposure | 0.035 (+ mode boost) / 1.3 / 1.05 |

## Updating it

1. Edit `Jarvis\assets\jarvis-black-hole.html` (this is the source). Back it up first as `.bak-YYYY-MM-DD`.
   - If the artifact was changed somewhere else, such as a cloud session, pull that version down first: read the artifact's `index.html`, back up the local page, then copy the artifact's version over it.
2. Look at it on the RTX: `Jarvis\open-on-rtx.ps1 -Restart`, then confirm with `nvidia-smi`.
3. Publish the same page to the artifact URL above so the pinned link shows the newest version.
4. Copy the page to `Jarvis\website\index.html`, and redeploy it once jarvisgalaxy.com is live.
5. Add an entry to [[Agentic OS change log]].
