---
title: Laptop health check 2026-10-04
date: 2026-10-04
tags: [laptop, performance, health-check]
related: "[[Work log]]"
---

# Laptop health check — 2026-10-04 (3:20 AM ET)

HP Victus 15-fa2xxx · Intel i5-13420H (8 cores / 12 threads) · 16 GB RAM · RTX 4050 Laptop · Samsung 512 GB SSD.

**Score: 48/100 (needs attention)**

| Area | Status | Reading |
|---|---|---|
| Storage | 🔴 | C: 26.6 GB free of 476 GB (6%) |
| Memory | 🟡 | 3.8 GB free of 15.6 GB |
| Battery | 🟢 | 100%, plugged in |
| Maintenance | 🟢 | restarted at 1:22 AM today; SSD reports Healthy |
| Startup | 🔴 | 19 programs start with Windows |
| Right now | 🟡 | CPU pinned at 100%: Defender (MsMpEng) is using about 85% |

## Why it sounded like a jet engine
- **Microsoft Defender full scan.** It was started on 2026-10-04 after Hydra and LuaTools were removed (MpCmdRun pid 18888), and it held the CPU at 100% with the disk 30–50% busy. It's temporary and ends when the scan finishes. Leave it running while plugged in.
- **Power plan set to "High performance".** This keeps clock speeds and fans up even at light load. Balanced is quieter.
- **Background extras:** the Claude VM (vmmem, about 1.8 GB), 6 node processes (about 600 MB), Intel XTU, Windhawk, Winstep Xtreme and Seelen UI.
- The GPU was idle (52 °C, 0%), so it isn't the cause.

## Where the disk space went
- Steam: 116 GB (`C:\Program Files (x86)\Steam`)
- AppData\Local\Packages: 13.5 GB
- Ollama models: 6.2 GB
- AppData\Local\Programs: 5.9 GB
- ProgramData: 7.9 GB
- Temp: 3.0 GB
- Downloads: 2.4 GB
- pagefile.sys: 15 GB

## Startup programs (19)
Opera GX + Opera GX Browser Assistant, Overwolf, Brave updater, Steam, Epic Games, Spotify, Edge auto-launch, UniConverter updater, Logi Download Assistant, Google Drive (3 entries), Hermes_Gateway, Ollama, Jarvis (it's in the startup list but wasn't running; JARVIS is meant to stay disabled), HP SEU launcher, Realtek audio, Windows Security.

Third-party services running: McAfee WebAdvisor (redundant with Defender), Intel XTU, Winstep Xtreme, Windhawk, HP agents (Comm Recover, One Agent, Print/Scan Doctor), NVIDIA, Codex sandbox, CoworkVMService.

## Recommendations (in order)
1. **Let the Defender scan finish**, then the fans calm down. Don't cancel it, because it's the post-cleanup malware check.
2. **Free 30–60 GB on C:.** Uninstall Steam games he no longer plays (Steam → Library → Manage → Uninstall), or move them to another drive. Empty Temp (3 GB, regenerates). Clear Downloads. Delete unused Ollama models (`ollama list`, then `ollama rm <name>`).
3. **Switch the power plan to Balanced:** Settings → System → Power → Power mode → Balanced. In OMEN Gaming Hub, use "Balanced" or "Quiet" fan mode when not gaming.
4. **Turn off startup apps:** Task Manager → Startup apps. Turn off Overwolf, Opera GX Assistant, Brave updater, Epic, Steam, Spotify, Edge auto-launch, UniConverter, Logi Download Assistant and Jarvis.
5. **Uninstall McAfee WebAdvisor** (Defender already protects) and anything unused among XTU, Winstep and Seelen UI.
6. **Close apps when they aren't needed:** the Claude desktop app and VM use about 4 GB of RAM. Close Ollama when not running local models.

## What was changed
Nothing. This check was read-only.

Related: [[Trading OS]] (runs from this laptop), Hermes agent (`Hermes_Gateway` starts with Windows).
