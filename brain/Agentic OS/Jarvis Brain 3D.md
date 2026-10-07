---
tags: [agentic-os, dashboard, brain-map]
aliases: [brain graph, 3D brain, Jarvis Brain graph]
created: 2026-09-25
---

# Jarvis Brain 3D

> [!info] Label: dashboard. Part of [[Agentic OS]].

Jarvis's memory, which is this vault, drawn as a glowing, rotating 3D brain. Every note in `brain/` and every Graphify neuron is a node, coloured by the brain lobe it belongs to. Click a node to read what it is and which note it comes from. The flat version of the same map is [[Brain Map/Brain Map|Brain Map]].

## Open it

| Way | Link |
|---|---|
| **BRAIN GRAPH ↗** pill on the [[Jarvis OS dashboard]] | `http://127.0.0.1:8765/brain`, served by the bridge (needs Jarvis running; websites can't load it). `/os/open?what=brain` opens it in a window |
| Artifact (pinned in the claude.ai sidebar) | https://claude.ai/artifact/DGm2GkGjMiQ1Mv9ys5ZrFE |
| Local file | `Kaydens Vault\Brain Map\Jarvis Brain 3D.html`. Open it in a browser; for a smooth view use `Jarvis\open-on-rtx.ps1 "<that path>"` |
| Obsidian Graph view | **Jarvis Brain** shortcut (Desktop + Start menu). It runs `Jarvis\open-brain-graph.ps1`, which opens the vault on [[Jarvis Brain]] and switches to Graph view through the Local REST API plugin. In Obsidian itself, press `Ctrl+G` |

## Keeping it current

- The node data is embedded in the page (`const DATA = {nodes, links}`).
- **Rebuild everything:** follow the steps at the bottom of [[Brain Map/Brain Map|Brain Map]]: `/graphify . --update`, then `python graphify-out\build_brain_map.py`.
- **Hand-added nodes:** on 2026-09-23 and 2026-09-25, nodes were added directly to the page, without regenerating the map. A full rebuild drops them unless the notes they point to have been through Graphify by then.
- **After any change:** publish the page to the artifact URL above, so the pinned link and `/brain` match, and log it in [[Agentic OS change log]].
