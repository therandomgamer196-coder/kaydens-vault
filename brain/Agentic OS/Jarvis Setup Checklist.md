---
tags: [agentic-os, jarvis, checklist]
aliases: [Jarvis checklist, hybrid brain setup]
created: 2026-10-07
status: in-progress
---

# Jarvis Setup Checklist

The free/cheap version of [[Jarvis Cloud Setup]]:
- **Everyday questions:** free fast online models (Groq, Cerebras)
- **"Think hard" / research:** Claude Opus 5.5, pay-per-use
- **24/7 work:** a cloud task on the Claude plan, with the brain synced through a private GitHub repo

Changes are logged in [[Agentic OS change log]].

## Done by Claude ✅

- [x] **Hybrid brain:** Groq first, then Cerebras, then local llama3.2. Saying "think hard", "research", "deep dive", "take your time" or "use Opus" sends that question to Opus first. Code: `jarvis_freebrain.py`, routing in `jarvis_bridge.py` (`provider_order`).
- [x] **Free web tools:** DuckDuckGo search (Wikipedia if it fails) and page reading (`jarvis_web.py`). They refuse anything on this PC or the home network, so a web page can't make Jarvis press his own buttons.
- [x] **Same brain tools on every model:** `search_brain`, `read_note`, `list_recent_notes`, `write_note` (only in [[Jarvis Notes]]).
- [x] **One key file:** `Documents\Jarvis\secrets\keys.env`. It's read on every question, so no restart is needed.
- [x] **Vault is a git repo:** first snapshot committed (168 files). The remote is set to `github.com/therandomgamer196-coder/kaydens-vault`, and `.gitignore` skips Obsidian's per-device workspace files.
- [x] **Jarvis syncs the brain every 5 min** (`jarvis_vaultsync.py`): commit, pull, push. It never pops up a sign-in. A conflict is rolled back and shown in `/status` → `vault_sync`.
- [x] **Tests:** all suites pass, including new ones for the free brain, web safety and vault sync.

## Kayden's steps 🙋

- [ ] **1. Groq key (free, 2 min):** sign up at `console.groq.com` → **API Keys** → **Create**. Paste it after `GROQ_API_KEY=` in `secrets\keys.env` and save.
- [ ] **2. Cerebras key (free backup, 2 min):** sign up at `cloud.cerebras.ai` → **API Keys**. Paste it after `CEREBRAS_API_KEY=`.
- [ ] **3. GitHub repo (2 min):** on github.com, signed in as `therandomgamer196-coder`: **New repository** → name `kaydens-vault` → **Private** → don't add a README → **Create**.
- [ ] **4. Connect it (1 min):** double-click `Documents\Jarvis\connect-brain-to-github.cmd`. Sign in to GitHub in the browser window that opens. From then on Jarvis syncs by himself.
- [ ] **5. Let Claude's cloud see the repo:** on claude.ai, in the GitHub connector settings, give access to `kaydens-vault`. Then tell Claude "repo is connected".
- [ ] **6. Optional, paid: Opus key** for "think hard". Get it at `console.anthropic.com`: add a little credit, set a **monthly limit**, create a key, and paste it after `ANTHROPIC_API_KEY=`.

> [!warning] Keys
> Only paste keys into `secrets\keys.env`. Never put them in chat, notes or websites.

## Claude's steps after Kayden's 🔜

- [ ] Test Groq and Cerebras live with a real question (the brain search and a web search).
- [ ] Create the **cloud Jarvis** scheduled task, which works through [[Jarvis Inbox]] every few hours.
- [ ] Watch the first few cloud runs and the first laptop ↔ cloud sync.
