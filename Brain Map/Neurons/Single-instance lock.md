---
type: neuron
lobe: "[[Lobe - Reliability & Maintenance]]"
source: "[[brain/Core Brain Functions/Maintenance|Maintenance]]"
kind: rationale
connections: 1
tags: [brain-map, lobe/reliability-maintenance]
generated: 2026-09-22
---
# Single-instance lock

> jarvis_bridge.lock with msvcrt.locking ensures only one bridge owns the mic.

**Why:** A second copy exits immediately; stale lock files are harmless because Windows releases the lock on exit.

## Connections

- references [[brain/Core Brain Functions/Maintenance|Maintenance]] · stated

## Lives in

- Lobe: [[Lobe - Reliability & Maintenance]]
- Source note: [[brain/Core Brain Functions/Maintenance|Maintenance]]
