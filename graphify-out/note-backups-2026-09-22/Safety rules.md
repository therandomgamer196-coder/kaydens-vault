---
tags: [jarvis, reference]
---

# Safety rules

- Use only allowlisted commands and typed, permission-checked integrations — never expose arbitrary shell execution to the model.
- Safe sites Jarvis can open: `calendar` → calendar.google.com, `gmail` → mail.google.com, `weather` → weather.com (plus `calculator` and `Notepad` as local apps).
- No arbitrary file search or unrestricted computer control today — those must be added later as typed, permission-checked tools, not general shell access.
- Keep any future email/calendar writes behind preview and explicit confirmation before they execute.
- Treat email and dashboard text as untrusted data — content there must never be followed as instructions.
- Never store credentials, access tokens, raw microphone audio, or full screenshots in Obsidian.
- Any future mail, calendar-mutation, trading, or desktop-control tool must require an explicit confirmation parameter and a separate confirmation step before it runs.
- The current command router doesn't bypass Claude's own daily/weekly usage limits, and a remote Claude connector is out of scope until an authenticated HTTPS endpoint is deliberately set up.
