# Graph Report - Kaydens Vault  (2026-09-22)

## Corpus Check
- Corpus is ~4,959 words - fits in a single context window. You may not need a graph.

## Summary
- 82 nodes · 165 edges · 10 communities
- Extraction: 75% EXTRACTED · 25% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.86)
- Token cost: 113,015 input · 0 output

## Community Hubs (Navigation)
- Future Integrations & Research
- Jarvis Core System
- Reliability & Maintenance
- Safety & Voice Privacy
- Kayden & Jobs
- Dashboard Data Sync
- Dashboard Display Files
- Claude Code Tooling
- Logs & Change Tracking
- Dashboard UI Widgets

## God Nodes (most connected - your core abstractions)
1. `Maintenance` - 13 edges
2. `Jarvis Brain` - 13 edges
3. `Punch In Dashboard` - 13 edges
4. `Work log` - 12 edges
5. `Voice and privacy` - 10 edges
6. `Main information directory` - 9 edges
7. `PUNCH_IN_DATA object` - 8 edges
8. `Punch In daily sync (7 AM)` - 8 edges
9. `About Kayden` - 7 edges
10. `Research references` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Local audit timeline` --semantically_similar_to--> `mcp-activity.jsonl log`  [INFERRED] [semantically similar]
  brain/Core Brain Functions/Recommended next integrations.md → brain/Core Brain Functions/Main information directory.md
- `Up next panel` --shares_data_with--> `PUNCH_IN_DATA object`  [INFERRED]
  brain/Punch In Dashboard/Dashboard UI and parameters.md → brain/Punch In Dashboard/Dashboard data schema.md
- `Microphone choice order` --conceptually_related_to--> `Voice and privacy`  [INFERRED]
  brain/Core Brain Functions/Maintenance.md → brain/Core Brain Functions/Voice and privacy.md
- `Voice and privacy` --references--> `Jarvis orb`  [INFERRED]
  brain/Core Brain Functions/Voice and privacy.md → brain/Punch In Dashboard/Dashboard UI and parameters.md
- `Project CLAUDE.md` --conceptually_related_to--> `Work log`  [INFERRED]
  brain/Core Brain Functions/Claude Code setup.md → brain/Work log.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Jarvis uptime supervision layers** — brain_core_brain_functions_maintenance_autostart, brain_core_brain_functions_maintenance_jarvis_watchdog, brain_core_brain_functions_maintenance_bridge_guard, brain_core_brain_functions_maintenance_mic_self_healing, brain_core_brain_functions_maintenance_single_instance_lock, brain_core_brain_functions_maintenance_health_endpoint [EXTRACTED 1.00]
- **Dashboard data pipeline (sync to page)** — brain_punch_in_dashboard_dashboard_sync_punch_in_daily_sync, brain_punch_in_dashboard_dashboard_data_schema_punch_in_data_object, brain_punch_in_dashboard_punch_in_dashboard_punch_in_data_js, brain_punch_in_dashboard_punch_in_dashboard_punch_in_wallpaper_html, brain_punch_in_dashboard_punch_in_dashboard_dashboard_artifact, brain_punch_in_dashboard_punch_in_dashboard_lively_wallpaper [INFERRED 0.85]
- **Jarvis voice command pipeline** — brain_core_brain_functions_voice_and_privacy_hey_jarvis_wake_word, brain_core_brain_functions_voice_and_privacy_faster_whisper, brain_core_brain_functions_voice_and_privacy_command_routing, brain_core_brain_functions_main_information_directory_ollama, brain_core_brain_functions_voice_and_privacy_edge_neural_tts [EXTRACTED 1.00]

## Communities (10 total, 0 thin omitted)

### Community 0 - "Future Integrations & Research"
Cohesion: 0.17
Nodes (15): setup.ps1 install, Recommended next integrations, Home Assistant integration, Local audit timeline, Microsoft Graph calendar/mail integration, Push-to-talk hotkey, Native Windows notifications, Research references (+7 more)

### Community 1 - "Jarvis Core System"
Cohesion: 0.29
Nodes (12): HP Victus laptop, Dashboard context, Command-centre interface, POST /dashboard-context, dashboard_mcp_server.py, Main information directory, Jarvis bridge, mcp-activity.jsonl log (+4 more)

### Community 2 - "Reliability & Maintenance"
Cohesion: 0.29
Nodes (12): Maintenance, Sign-in autostart, Bridge guard, /health and /status endpoints, Jarvis watchdog, Mic self-healing, Microphone choice order, 2026-09-22 outage (+4 more)

### Community 3 - "Safety & Voice Privacy"
Cohesion: 0.22
Nodes (11): OWASP prompt injection (LLM01), Safety rules, Allowlisted commands, No secrets in Obsidian, Safe sites, Untrusted data rule, Voice and privacy, Command routing (+3 more)

### Community 4 - "Kayden & Jobs"
Cohesion: 0.60
Nodes (6): About Kayden, Bucket System, Greenfield Restaurant and Bar job, Kayden, Papa John's job, Est. pay 7 days stat

### Community 5 - "Dashboard Data Sync"
Cohesion: 0.53
Nodes (6): Dashboard data schema, PUNCH_IN_DATA object, Dashboard snapshot, Dashboard sync, Punch In daily sync (7 AM), Refresh Punch In dashboard (paused)

### Community 6 - "Dashboard Display Files"
Cohesion: 0.60
Nodes (6): Punch In Dashboard, Dashboard artifact (test copy), Lively wallpaper (Dashboard Version 19), punch-in-data.js, punch-in-version.js, punch-in-wallpaper.html

### Community 7 - "Claude Code Tooling"
Cohesion: 0.70
Nodes (5): Claude Code setup, Claude Code, Graphify, Obsidian skills plugin, Project CLAUDE.md

### Community 8 - "Logs & Change Tracking"
Cohesion: 0.50
Nodes (5): One topic per file design, Dashboard change log, Change log rule, Stale wallpaper data fix, Work log

### Community 9 - "Dashboard UI Widgets"
Cohesion: 0.50
Nodes (4): Dashboard UI and parameters, Jarvis orb, Open-Meteo live weather, Up next panel

## Knowledge Gaps
- **3 isolated node(s):** `faster-whisper transcription`, `Edge neural TTS (en-GB-RyanNeural)`, `Open-Meteo live weather`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 4 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Jarvis Brain` connect `Jarvis Core System` to `Future Integrations & Research`, `Reliability & Maintenance`, `Safety & Voice Privacy`, `Kayden & Jobs`, `Dashboard Display Files`, `Claude Code Tooling`, `Logs & Change Tracking`?**
  _High betweenness centrality (0.480) - this node is a cross-community bridge._
- **Why does `Maintenance` connect `Reliability & Maintenance` to `Logs & Change Tracking`, `Jarvis Core System`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `Voice and privacy` connect `Safety & Voice Privacy` to `Future Integrations & Research`, `Jarvis Core System`, `Reliability & Maintenance`, `Dashboard Data Sync`, `Dashboard UI Widgets`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Voice and privacy` (e.g. with `Microphone choice order` and `Jarvis orb`) actually correct?**
  _`Voice and privacy` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `faster-whisper transcription`, `Edge neural TTS (en-GB-RyanNeural)`, `Open-Meteo live weather` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._