---
tags: [trading, zero, handoff]
type: note
created: 2026-10-21
updated: 2026-10-22
status: growing
summary: Work that VS Code (or Kayden) needs Claude to do - script uploads, scheduled-task changes, anything touching Robinhood or the page database.
related: ["[[ZERO trading agent]]", "[[VS Code agent brief]]", "[[Pending scheduled-task changes]]"]
---

# Handoff to Claude

Add items under **Open**, newest first: date, what, which file, how it was tested, and whether it changes real-money behavior. Claude moves finished items to **Done**.

## Open
- [ ] **2026-10-22 (Scribe, 2:42 AM ET)** Scheduled tasks can't load `mcp__claude-code-remote__add_repo` (ToolSearch doesn't return it). The Lab's pushes fail with 403 and its notes don't reach the brain. The Scribe's own push at 2:42 AM worked without add_repo, so the 403 is specific to the Lab's sessions: give the Lab task the same repo access the Scribe has (see [[Daily desk 2026-10-22]]). No real-money change.
- [ ] **2026-10-22 (Scribe)** `graphify-out/build_brain_data.py` (the Jarvis Brain 3D builder the Scribe prompt runs) is not in the vault. The 3D page's data was last built 2026-10-22 03:42 UTC from head 52d3da5. Commit the script to `graphify-out/` so the Scribe can rebuild it. No real-money change.
- [ ] **2026-10-22 (Scribe)** Writing `config/rules_snapshot` was refused by the permission check (the doc doesn't exist yet). Create it once, or allow the Scribe to write it. No real-money change.
- [ ] 2026-10-21: Apply [[Pending scheduled-task changes]] (needs Kayden's "approve scheduled task changes"). Real money: items 3 and 7 touch real-money tasks.

## Done
- [x] 2026-10-21: Lab engine v1.5 uploaded (GM/NU stop-check fix) → `trading-os-code/lab_engine.py`.
