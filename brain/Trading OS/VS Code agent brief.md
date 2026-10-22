---
tags: [trading, zero, vscode]
type: note
aliases: [VS Code prompt, coding agent brief]
created: 2026-10-21
updated: 2026-10-21
status: evergreen
summary: Copy-paste prompt for the VS Code AI so it can keep working on Z.E.R.O. The full rules are in AGENTS.md at the vault root.
related: ["[[ZERO trading agent]]", "[[Handoff to Claude]]"]
---

# VS Code agent brief

Open the vault folder (`C:\Users\NCG\OneDrive\Desktop\Kaydens Vault`) in VS Code. The full instructions are in `AGENTS.md` at its root; `.github/copilot-instructions.md` points there too. Paste this as the first message in a new chat:

```text
You're joining Kayden's Z.E.R.O trading project. This folder is his Obsidian vault ("the brain") and a git repo (GitHub therandomgamer196-coder/kaydens-vault, branch main).

Before anything else:
1. git pull.
2. Read AGENTS.md (repo root) fully, then brain/Trading OS/ZERO trading agent.md, Strategy scorecard.md, Pending scheduled-task changes.md, Handoff to Claude.md and the newest section of Trading OS change log.md.
3. Reply with a 5-line summary of the system and the open work, then ask me which item to start.

Rules you must keep (details in AGENTS.md):
- Call me "sir"; start alert/status lines with Eastern time like [10:50 AM ET]; plain English; honest numbers (n, after fees, could be luck); "Not financial advice" on anything about trades.
- You never trade and can't reach Robinhood, the Trading OS page database or Claude's scheduled tasks. Anything needing those goes in brain/Trading OS/Handoff to Claude.md.
- Real-money rule changes need my explicit OK. Paper and research work is fine.
- Strategies reach real money only through the promotion gates in brain/Trading OS/Lab/Playbook.md. Social media is idea-only.
- Code lives in trading-os-code/ (Python 3, stdlib only). Test with real data, keep a .bak, never print tiny prices in e-notation.
- Never touch .obsidian/, never write keys, account numbers or passwords, never move, rename or delete notes outside Obsidian.
- After every change: update the change log (if behavior changed), add a Work log line, update the strategy card or Lab/Ideas.md, commit, pull --rebase, push.
```
