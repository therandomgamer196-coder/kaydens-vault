---
tags: [jarvis, reference, tooling]
aliases: [Claude Code]
---

# Claude Code setup

Claude Code is the preferred place to change Jarvis and the Punch In dashboard (set up 2026-09-22).

## Install state

| Piece | Where / version | Notes |
|---|---|---|
| Claude Code | `C:\Users\NCG\.local\bin\claude.exe`, 2.1.272 | was installed but **not on PATH** ("claude is not recognized") — `C:\Users\NCG\.local\bin` added to the user PATH |
| Git for Windows | `C:\Program Files\Git`, 2.55.0 | required by Claude Code on Windows; installed via winget |
| Obsidian skills | plugin `obsidian@obsidian-skills` 1.0.1, user scope, enabled | from kepano/obsidian-skills (Obsidian's own team): Obsidian Markdown, Bases, JSON Canvas, Obsidian CLI and more |
| Project instructions | `C:\Users\NCG\Documents\CLAUDE.md` | tells Claude Code where everything lives, to read this vault first, and to log every change |
| Graphify | `graphifyy` 0.9.65 (pip, Python 3.12) → `graphify.exe` in Python312\Scripts; skill at `C:\Users\NCG\.claude\skills\graphify` | turns a folder (code, docs, notes) into a queryable knowledge graph. Official package is `graphifyy` (double y) — other graphify* packages on PyPI aren't the author's. `graphify install` also created `C:\Users\NCG\.claude\CLAUDE.md` (just points Claude Code at the skill) |

## Starting it

Open a **new** PowerShell window (old windows don't see the PATH change), then:

```powershell
cd $HOME\Documents
claude --add-dir "C:\Users\NCG\OneDrive\Desktop\Kaydens Vault" --add-dir "C:\Users\NCG\AppData\Local\Packages\12030rocksdanister.LivelyWallpaper_97hta09mmv6hy\LocalCache\Local\Lively Wallpaper\Library\wallpapers"
```

Slash commands like `/plugin` are typed **inside** Claude Code, not in PowerShell. From PowerShell the equivalents are `claude plugin marketplace add <owner/repo>` and `claude plugin install <plugin>@<marketplace>`.

## Using Graphify

- Inside Claude Code: `/graphify .` (graph of the current folder), then ask questions about it.
- From PowerShell: `graphify .` — no leading slash (PowerShell reads it as a path).
- Obsidian output: add `--obsidian --obsidian-dir "<folder>"` to write the graph as notes. Point it at a **separate folder**, not `brain\`, so generated notes never mix with Jarvis's hand-kept notes.
- Update: `python -m pip install --upgrade graphifyy` then `graphify install`.
