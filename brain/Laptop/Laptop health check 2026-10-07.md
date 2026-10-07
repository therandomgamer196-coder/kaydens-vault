---
title: Laptop health check 2026-10-07
date: 2026-10-07
tags: [laptop, performance, health-check]
---

# Laptop health check 2026-10-07

Weekly scheduled read-only check at 9:12 AM ET. HP Victus 15-fa2xxx. Compared with [[Laptop health check 2026-10-04]] baseline (score 48).

## Score: 64/100 (baseline 48, up 16)

| Area | Status | Detail | vs 2026-10-04 |
|---|---|---|---|
| Storage | 🔴 | C: 24.7 GB free of 476 GB (5.2%) | Worse (was 6%) |
| Memory | 🟢 | 7.2 of 15.6 GB free (46%) | OK |
| Startup | 🔴 | 19 startup entries | Same (19) |
| Right now | 🟢 | Total CPU 11%, nothing over 1% | Better (Defender scan finished) |
| Maintenance | 🟢 | Just rebooted (uptime under 1 day) | OK |
| Disk health | 🟢 | Samsung SSD and Toshiba HDD both Healthy | Same |

Power plan: **High performance** (unchanged, keeps fans higher). GPU: 44 °C, 0% use, 7.7 W.
Defender: real-time on, full scan 3 days ago, signatures 1 day old, no scan running.

## What's using CPU

Machine was idle: System 0.7%, python 0.2%, nvdisplay.container 0.2%, MsMpEng 0.1%. Not loud right now.
Top RAM: Claude app (~1.5 GB across processes), vmmem 550 MB, MsMpEng 355 MB, Explorer 316 MB, Overwolf 194 MB.

## Disk hogs

| Folder | Size | vs baseline |
|---|---|---|
| Steam (Program Files x86) | 116.3 GB | Same |
| AppData\Local\Packages | 15.7 GB | Up from 13.5 GB |
| .ollama | 6.2 GB | Same |
| AppData\Local\Temp | 3.3 GB | Up from 3 GB |
| Downloads | 2.8 GB | — |

## Startup (19)

Google Drive (x3 entries), Hermes_Gateway, Ollama, HP SEU launcher, Opera GX + Browser Assistant, Overwolf, Brave updater, Spotify, Epic, Steam, **Jarvis**, Edge auto-launch, SecurityHealth, Realtek audio, UniConverter updater, Logi Download Assistant.

- ⚠️ **Jarvis is still listed as a startup entry** (not running at check time). It should stay disabled.
- Hydra / LuaTools: not installed, not running. Good.
- Third-party services running: McAfee WebAdvisor, Windhawk, Winstep Xtreme, Wondershare NativePush, HP agents (One Agent, Comm Recover, Print Scan Doctor), NVIDIA FrameView/Container, Intel Graphics, Codex sandbox, Claude CoworkVM.

## Top recommendations

1. **Free space on C: (critical, 5.2%)** – Uninstall unused Steam games: Steam > Library > right-click game > Manage > Uninstall (or move to the Toshiba HDD via Steam > Settings > Storage). Empty Temp (3.3 GB) and Recycle Bin; `ollama rm` unused models (6.2 GB).
2. **Disable Jarvis and trim startup** – Task Manager (Ctrl+Shift+Esc) > Startup apps > Disable Jarvis, Overwolf, Epic, Opera GX Assistant, UniConverter, Logi Download Assistant, Edge auto-launch, Brave updater.
3. **Switch power plan to Balanced** – Settings > System > Power & battery > Power mode (or OMEN Gaming Hub > Quiet) for less fan noise.
4. Remove McAfee WebAdvisor (redundant with Defender) – Settings > Apps > Installed apps > McAfee WebAdvisor > Uninstall.
5. Remove Wondershare NativePush/UniConverter if unused.

## What was changed

Nothing (read-only).