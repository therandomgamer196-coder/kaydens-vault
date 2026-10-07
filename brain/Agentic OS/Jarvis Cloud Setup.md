---
tags: [agentic-os, jarvis, setup]
aliases: [Jarvis cloud, Jarvis 24/7, Jarvis Opus brain]
created: 2026-10-06
status: waiting-on-kayden
---

# Jarvis Cloud Setup

> [!todo] Current plan
> The cheaper hybrid plan is being set up now. Follow [[Jarvis Setup Checklist]].

How Jarvis gets a smarter brain (Claude Opus 5.5) and works around the clock in the cloud. Part of [[Agentic OS]]. Changes are logged in [[Agentic OS change log]].

> [!info] What runs where
> - **On the laptop (voice Jarvis):** wake word, mic, voice, the dashboards. Voice Jarvis is only awake while the laptop is on, because the mic is there.
> - **Claude Opus 5.5 (deep brain):** answers anything the instant answers don't cover. He can search and read this vault live, write his own notes in [[Jarvis Notes]], and search the web when the brain doesn't have the answer. It needs an API key (step 1).
> - **In the cloud (24/7 Jarvis):** a scheduled Claude session that works through [[Jarvis Inbox]] while the laptop is off. It needs the vault synced to GitHub (steps 2–3).

## Step 1: give Jarvis his Opus brain (about 5 minutes)

- [ ] Go to `console.anthropic.com`, sign in, and add credits under **Billing**. Set a **monthly spend limit** you're comfortable with.
- [ ] **Settings → API keys → Create key**, named "Jarvis".
- [ ] Open `C:\Users\NCG\Documents\Jarvis\secrets\anthropic.env` in Notepad. Paste the key after `ANTHROPIC_API_KEY=` and save.
- [ ] That's it. No restart is needed, because Jarvis reads the file on every question. The Jarvis OS dashboard `/status` shows `"claude": "ready"` within a minute.

> [!warning] Keep the key secret
> Only ever paste the key into that file, never into a chat, a note or a website. If it leaks, delete it in the console and make a new one.

Until the key is there, Jarvis answers with the local model (llama3.2), exactly as before.

## Step 2: sync the vault to GitHub (about 15 minutes)

This lets a cloud Jarvis read and write the brain while the laptop is off.

- [ ] Make a free GitHub account if you don't have one. Create a **private** repo called `kaydens-vault`.
- [ ] In Obsidian: **Settings → Community plugins → Browse → "Git"** (by Vinzent), then Install and Enable.
- [ ] Set up the plugin in the vault folder and push once. GitHub Desktop is the easiest way to sign in. Then turn on **Auto commit-and-sync interval: 5 minutes** and **Pull on startup**.
- [ ] On claude.ai, connect GitHub (Settings → Connectors / Claude Code → GitHub) and give it access to `kaydens-vault`.

## Step 3: turn on 24/7 Jarvis (I do this once step 2 is done)

- A **scheduled cloud task** runs every few hours on Opus 5.5:
  1. pulls the vault
  2. works through the open items in [[Jarvis Inbox]]: research, plans, drafts, summaries
  3. writes results into [[Jarvis Notes]] and ticks the items
  4. pushes the vault back
- Laptop Jarvis sees the new notes within minutes (Obsidian Git pulls them), and he can read them out when asked.
- **Cost:** the scheduled task runs on your Claude plan. Only the voice questions in step 1 use API credits.

## Free and cheaper options (researched 2026-10-07)

> [!tip] Cheapest setup that still works well
> - **Everyday brain:** a free fast online model ([[#Free brains|Groq or Cerebras]]), with the same brain/web tools.
> - **Opus 5.5:** only when he's told to "think hard", or for research.
> - **24/7 work:** a Claude scheduled task on the plan Kayden already pays for, with the vault in a free private GitHub repo.
> - **Total extra cost:** about $0–5 a month.

### What Opus would cost on its own

Official prices: Opus 5.5 is $4 in / $20 out per million tokens, Sonnet 5.5 $2 / $10, Haiku 4.5 $1 / $5. Web search is $10 per 1,000 searches. Cached prompt reads on Opus cost 0.05×.

Rough estimate (a guess, not a quote): a voice question with a brain search is about 8k tokens in and 1–1.5k out. That's about **5–6¢ on Opus**, about 3¢ on Sonnet and about 1.5¢ on Haiku. At 20 questions a day it comes to about $30, $15 or $7 a month.

### Free brains

| Option | Free limit (third-party summary, Sep 2026) | Good for Jarvis? |
|---|---|---|
| **Groq** (Llama 3.3 70B) | 30 requests/min, ~1,000/day | ✅ Very fast, tool calling, not trained on |
| **Cerebras** (Llama 3.3 70B) | 30 requests/min, ~1M tokens/day | ✅ Same, even faster |
| **OpenRouter** free models | 20/min, 50/day (1,000/day after a $10 top-up) | ⚠️ Fine as a backup |
| **GitHub Models** | 15/min, 150–1,000/day | ⚠️ Backup |
| **Gemini** free tier | Flash models only, low daily caps; free-tier prompts are used by Google | ❌ Not for the vault (finances, personal notes) |
| **Local llama3.2** (now) | Unlimited, offline | ✅ Stays as the offline fallback |

### Free 24/7 places to run things

- **Claude scheduled tasks:** already included in the Claude plan. This is the best fit for cloud Jarvis working through [[Jarvis Inbox]].
- **GitHub:** private repos are free, and Actions includes **2,000 free minutes/month** on private repos (unlimited on public ones). It could run a cron job against a free model, at $0.
- **Oracle Cloud Always Free:** an always-on ARM server, enough for a phone bot. Since June 2026 the free Ampere allowance is **2 OCPU / 12 GB** (it was 4/24), and enforcement is inconsistent, so set a $0 budget alert.

## Optional later: talk to Jarvis from your phone 24/7

- A small always-on server (about $5 a month), running a Claude agent with the same tools, connected to a Telegram or Discord bot. Ask for it when you want it.

## Status

- 2026-10-07: researched free/cheaper options (above). Proposed hybrid: free Groq/Cerebras everyday, Opus on demand.
- 2026-10-06: Opus brain code installed and tested (falls back to llama with no key). Claude Code set to Opus 5.5 at high effort. **Waiting on Kayden for steps 1–2.**
