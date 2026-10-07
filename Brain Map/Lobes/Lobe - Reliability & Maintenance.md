---
type: lobe
region: Brainstem
color: "#22d3ee"
neurons: 12
cohesion: 0.29
tags: [brain-map, lobe]
generated: 2026-09-22
---
# Lobe - Reliability & Maintenance

> **Brainstem** — autonomic functions that keep Jarvis alive: autostart, watchdog, mic self-healing.

## Brain notes in this lobe

- [[brain/Core Brain Functions/Maintenance|Maintenance]]

## Neurons

- [[Jarvis watchdog]] — jarvis_watchdog.py checks /health every 30 s and kills/restarts a hung bridge; single instance via lock file.
- [[2026-09-22 outage]] — The bridge picked the unopenable Galaxy Buds mic and the wake-word thread died without retry, leaving ready:false.
- [[health and status endpoints]] — GET /health returns ok/ready/error/pid/mic fields; GET /status returns everything including dashboard context.
- [[tests-run_tests.py]] — 31 tests for bridge and watchdog with faked audio, safe to run while Jarvis is live.
- [[Stuck 'speaking' known issue]] — Open issue: in follow-ups Jarvis can stay flagged speaking:true and take room chatter as commands.
- [[Microphone choice order]] — Default order: built-in Microphone Array, wired headset, other mic, Bluetooth hands-free last; Stereo Mix never used.
- [[Audio validation rule]] — Any audio/TTS change must be tested with an audible sentence and /status must show speaking:false, ready:true, no error.
- [[Sign-in autostart]] — install-autostart.cmd adds a HKCU Run entry 'Jarvis' that launches start-watchdog.vbs at each sign-in.
- [[Bridge guard]] — The bridge relaunches the watchdog if it is gone, checked every 60 s; disable with JARVIS_NO_WATCHDOG=1.
- [[Mic self-healing]] — Mic failures are retried every 5 s after re-scanning devices, with a 5-minute cooldown for repeatedly failing mics.
- [[Single-instance lock]] — jarvis_bridge.lock with msvcrt.locking ensures only one bridge owns the mic.

## Wired to other lobes

- [[Lobe - Jarvis Core System]] — 4 connections
- [[Lobe - Logs & Change Tracking]] — 3 connections
- [[Lobe - Safety & Voice Privacy]] — 2 connections
- [[Lobe - Dashboard UI Widgets]] — 1 connection

Back to [[Brain Map]]
