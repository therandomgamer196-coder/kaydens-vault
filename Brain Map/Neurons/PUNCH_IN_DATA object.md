---
type: neuron
lobe: "[[Lobe - Dashboard Data Sync]]"
source: "[[brain/Punch In Dashboard/Dashboard data schema|Dashboard data schema]]"
kind: code
connections: 8
tags: [brain-map, lobe/dashboard-data-sync]
generated: 2026-09-22
---
# PUNCH_IN_DATA object

> window.PUNCH_IN_DATA with updatedAt, events, inbox, robinhood, payPeriods and weather; same object as artifact doc dashboard/data.

**Why:** Only last 4 digits of account numbers are ever stored.

## Connections

- references [[brain/Punch In Dashboard/Dashboard data schema|Dashboard data schema]] · stated
- shares data with [[Punch In daily sync (7 AM)]] · stated
- shares data with [[punch-in-data.js]] · stated
- shares data with [[Dashboard artifact (test copy)]] · inferred 0.95
- shares data with [[brain/Punch In Dashboard/Dashboard snapshot|Dashboard snapshot]] · inferred 0.85
- shares data with [[dashboard_mcp_server.py]] · inferred 0.75
- shares data with [[POST dashboard-context]] · inferred 0.75
- shares data with [[Up next panel]] · inferred 0.95

## Lives in

- Lobe: [[Lobe - Dashboard Data Sync]]
- Source note: [[brain/Punch In Dashboard/Dashboard data schema|Dashboard data schema]]
