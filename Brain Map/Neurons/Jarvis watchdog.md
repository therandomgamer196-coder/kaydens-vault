---
type: neuron
lobe: "[[Lobe - Reliability & Maintenance]]"
source: "[[brain/Core Brain Functions/Maintenance|Maintenance]]"
kind: code
connections: 7
tags: [brain-map, lobe/reliability-maintenance]
generated: 2026-09-22
---
# Jarvis watchdog

> jarvis_watchdog.py checks /health every 30 s and kills/restarts a hung bridge; single instance via lock file.

## Connections

- triggers [[health and status endpoints]] · stated
- references [[brain/Core Brain Functions/Maintenance|Maintenance]] · stated
- triggers [[Sign-in autostart]] · stated
- references [[tests-run_tests.py]] · stated
- explains why [[2026-09-22 outage]] · inferred 0.85
- triggers [[Bridge guard]] · inferred 0.85
- references [[Jarvis bridge]] · inferred 0.95

## Lives in

- Lobe: [[Lobe - Reliability & Maintenance]]
- Source note: [[brain/Core Brain Functions/Maintenance|Maintenance]]
