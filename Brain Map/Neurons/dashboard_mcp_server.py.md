---
type: neuron
lobe: "[[Lobe - Jarvis Core System]]"
source: "[[brain/Core Brain Functions/Dashboard context|Dashboard context]]"
kind: code
connections: 4
tags: [brain-map, lobe/jarvis-core-system]
generated: 2026-09-22
---
# dashboard_mcp_server.py

> Local read-only MCP server for Claude Desktop exposing dashboard summary, shifts, inbox, Robinhood, weather and Jarvis status tools.

**Why:** Prefer a local server over a public remote connector to keep data on the PC.

## Connections

- references [[brain/Core Brain Functions/Dashboard context|Dashboard context]] · stated
- references [[brain/Core Brain Functions/Main information directory|Main information directory]] · stated
- shares data with [[mcp-activity.jsonl log]] · inferred 0.85
- shares data with [[PUNCH_IN_DATA object]] · inferred 0.75

## Lives in

- Lobe: [[Lobe - Jarvis Core System]]
- Source note: [[brain/Core Brain Functions/Dashboard context|Dashboard context]]
