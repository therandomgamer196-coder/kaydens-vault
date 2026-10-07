---
tags: [jarvis, plan, roadmap]
aliases: [Future plans, Blocked plans]
created: 2026-09-23
status: waiting
---

# Jarvis future plans

Things Kayden asked for, or saw in the reference JARVIS video, that can't be finished yet, with the reason and what unblocks each. The full roadmap is [[Autonomous agent plan]]; what exists today is in [[Jarvis OS dashboard]].

## Waiting on Kayden's permission settings

**Terminal on the dashboard + Jarvis running commands when a question needs it** (asked 2026-09-23)
- Wanted: a command line in the dashboard, a Claude Code 1:1 chat panel in the dashboard's style, and Jarvis deciding for himself when a question needs a command, for example downloading something or running a basic command, and only then running one.
- Status: `Jarvis\jarvis_terminal.py` is written but not connected. It runs typed PowerShell commands and headless `claude -p` chats as jobs you can stop, keeps one Claude conversation going across prompts, and logs every command to `logs\terminal.jsonl`. On 2026-09-23, Claude Code's safety check refused to connect it to the bridge, because a local web endpoint that runs shell commands and Claude Code counts as an unsafe agent.
- To unblock: Kayden decides in Claude Code how much to allow, for example a permission rule for this project, or approving the step when asked. Then connect `/term/shell`, `/term/claude`, `/term/job` and `/term/stop`, accepted only from the dashboard page itself, add the Terminal tab, and add the `run_command` tool with the permission tiers from [[Autonomous agent plan]] Phase 4. Read-only commands would run at once. Downloads, installs and anything else would show the exact command and need Kayden's "confirm". Admin commands would also need the Windows UAC prompt.
- Before Jarvis himself gets it: the bridge secret token (Phase 0) and a spoken confirmation flow.

## Waiting on other steps

- **Jarvis messaging existing Claude Code sessions** (from the video: "I can reach into existing sessions to send messages"). The Sessions tab can already see every session. Sending to one uses `claude -p --resume <session id>`, so it needs the terminal above first.
- **Brainstorm a build, then set Claude loose in the background** (from the video). Jarvis talks the plan through, writes it as a spec, and Kayden approves it in the Specs tab. Then Claude Code builds it headless, and the Runs tab shows progress. Needs the terminal above and a spec format, for example `brain/Specs/*.md`.
- **Exact plan usage percentages** (5-hour and weekly limits). Claude doesn't expose these locally; the Usage tab shows token totals instead. Revisit if Claude Code ever writes its limits to disk.
- **Editing memory notes in the dashboard.** The Memory tab reads notes today. Editing needs a safe write route (backup, then write, then a change-log entry).
- **Agent brain choosing actions (Phase 2).** `qwen2.5:7b` is downloaded for this. It lost to `llama3.2` for plain talking, but it should do better at picking tools.
- **Bridge secret token + Git (rest of Phase 0).**
- **Local 7 AM sync (Phase 8).** Needs the Robinhood decision.
- **Update the Punch In artifact test copy** with the green orb, so it matches the wallpaper again.

## Related

- [[Autonomous agent plan]] · [[Jarvis OS dashboard]] · [[Safety rules]] · [[Work log]]
