---
type: neuron
lobe: "[[Lobe - Dashboard Data Sync]]"
source: "[[brain/Punch In Dashboard/Dashboard sync|Dashboard sync]]"
kind: code
connections: 8
tags: [brain-map, lobe/dashboard-data-sync]
generated: 2026-09-22
---
# Punch In daily sync (7 AM)

> Scheduled task (cron 0 11 * * *) pulling calendar, pay periods, Gmail, Robinhood and weather, then writing the artifact DB and every punchin*.dash folder.

**Why:** Cut from 48 runs/day to 1 to reduce token cost; viewing the dashboard costs no tokens.

## Connections

- shares data with [[brain/Punch In Dashboard/Dashboard snapshot|Dashboard snapshot]] · stated
- references [[brain/Punch In Dashboard/Dashboard sync|Dashboard sync]] · stated
- shares data with [[punch-in-data.js]] · stated
- shares data with [[PUNCH_IN_DATA object]] · stated
- related to [[Refresh Punch In dashboard (paused)]] · stated
- references [[Greenfield Restaurant and Bar job]] · inferred 0.85
- references [[Papa John's job]] · inferred 0.85
- explains why [[Stale wallpaper data fix]] · inferred 0.95

## Lives in

- Lobe: [[Lobe - Dashboard Data Sync]]
- Source note: [[brain/Punch In Dashboard/Dashboard sync|Dashboard sync]]
