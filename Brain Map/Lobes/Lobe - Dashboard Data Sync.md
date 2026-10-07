---
type: lobe
region: Right occipital lobe
color: "#34d399"
neurons: 6
cohesion: 0.53
tags: [brain-map, lobe]
generated: 2026-09-22
---
# Lobe - Dashboard Data Sync

> **Right occipital lobe** — what the dashboard sees: the daily sync and its data format.

## Brain notes in this lobe

- [[brain/Punch In Dashboard/Dashboard sync|Dashboard sync]]
- [[brain/Punch In Dashboard/Dashboard snapshot|Dashboard snapshot]]
- [[brain/Punch In Dashboard/Dashboard data schema|Dashboard data schema]]

## Neurons

- [[PUNCH_IN_DATA object]] — window.PUNCH_IN_DATA with updatedAt, events, inbox, robinhood, payPeriods and weather; same object as artifact doc dashboard/data.
- [[Punch In daily sync (7 AM)]] — Scheduled task (cron 0 11 * * *) pulling calendar, pay periods, Gmail, Robinhood and weather, then writing the artifact DB and every punchin*.dash folder.
- [[Refresh Punch In dashboard (paused)]] — Former hourly task, paused not deleted on 2026-09-22.

## Wired to other lobes

- [[Lobe - Dashboard Display Files]] — 6 connections
- [[Lobe - Logs & Change Tracking]] — 4 connections
- [[Lobe - Jarvis Core System]] — 2 connections
- [[Lobe - Kayden & Jobs]] — 2 connections
- [[Lobe - Safety & Voice Privacy]] — 1 connection
- [[Lobe - Dashboard UI Widgets]] — 1 connection

Back to [[Brain Map]]
