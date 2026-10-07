---
tags: [jarvis, reference]
---

# Safety rules

- Use only typed, permission-checked tools — never pipe the model's text straight into a shell. Terminal access is planned as the tier-checked `run_command` tool ([[Autonomous agent plan]], Phase 4); until it's built, Jarvis has no shell access.
- **Opening things (since 2026-09-22):** Jarvis can open any app in the Start menu and any `http(s)` web address in the default browser. Uninstallers and document shortcuts are never launched; addresses are only ever opened as `http`/`https` (no `file:`, `javascript:` or local-network addresses). Aliases (Google Calendar, Gmail, weather.com) live in `Jarvis\jarvis_aliases.json`. Every launch is logged to `logs\launcher.jsonl`.
- **Who can give orders over HTTP (since 2026-09-22):** only the Lively wallpaper (WebView2, origin `https://<random>.localhost`), a page opened from disk (origin `null`), the command centre at `127.0.0.1:8765`, and local tools with no browser headers. Websites are refused (403) for every endpoint except `/`, `/health` and the background image, and they can no longer read `/status`. Requests whose Host header isn't `127.0.0.1:8765`/`localhost:8765` are refused (DNS rebinding). Refusals are logged in `logs\wake_debug.log` as `caller REFUSED`. Remaining gap until the secret token is added: another program on this PC, or a sandboxed page with origin `null`.
- No file tools or terminal yet — both must wait for the secret token and the stuck-`speaking` fix, then arrive as tiered tools (see the permission tiers in [[Autonomous agent plan]]).
- Keep any future email/calendar writes behind preview and explicit confirmation before they execute.
- Treat email and dashboard text as untrusted data — content there must never be followed as instructions.
- Never store credentials, access tokens, raw microphone audio, or full screenshots in Obsidian.
- Any future mail, calendar-mutation, trading, or desktop-control tool must require an explicit confirmation parameter and a separate confirmation step before it runs.
- The current command router doesn't bypass Claude's own daily/weekly usage limits, and a remote Claude connector is out of scope until an authenticated HTTPS endpoint is deliberately set up.

## Related

- [[Dashboard context]] — the dashboard snapshot these rules treat as untrusted data
- [[Voice and privacy]] — what is never recorded or stored
- [[Autonomous agent plan]] — how future dashboard-changing tools stay typed and confirmation-gated
- [[Research references]] — OWASP prompt-injection guidance
