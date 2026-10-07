---
tags: [jarvis, reference]
---

# Voice and privacy

- Wake phrase: `Hey Jarvis`. Microphone audio is never sent to a cloud service.
- Mic selection: prefers a plugged headset/earbud, falls back to the laptop mic array; only the selected input stream is opened (never both). Override with `JARVIS_INPUT_DEVICE` (default `auto`) in `start-jarvis.cmd`.
- Wake detection: 0.2 VAD threshold, 0.35 wake score threshold — override with `JARVIS_VAD_THRESHOLD` / `JARVIS_WAKE_THRESHOLD` when tuning for a different mic.
- After wake: mic window stays open while you speak, ends ~0.8s after silence, 30-second safety max. Command capture calibrates an ambient-noise floor, applies a 180Hz high-pass filter, and requires two consecutive above-threshold chunks before it starts — cuts down on TV/fan/room noise (not a guarantee against nearby human speech).
- Transcription: local faster-whisper, kept warm after first use.
- Routing: open commands go to the app launcher (below); `what time is it` is answered locally; everything else goes to the local Ollama model (or configured fallback) and is spoken back. `/command?text=...` runs a command without the mic; `/preview?text=...` shows what an open command *would* do without opening anything.
- **Opening apps and websites** (`jarvis_launcher.py`, since 2026-09-22):
  - Verbs: "open", "launch", "pull up", "bring up", "go to", "visit", "load up". "Hey Jarvis", "can you", "please", "for me" are ignored.
  - **Say an address → browser:** "pull up youtube.com" / "youtube dot com" opens it in the default browser.
  - **Say a name → app:** "open YouTube" opens the installed app; if there isn't one and the name has a known website (YouTube, Netflix, Spotify, Discord…), that website opens instead and Jarvis says so. "open YouTube in the browser" forces the website.
  - Names are matched loosely: "open edge" → Microsoft Edge, "open opera" → Opera GX, "open calc" → Calculator, small mis-hearings like "spotifi" still work. Apps installed later are picked up automatically.
  - Aliases win over apps: "open calendar" → Google Calendar, "gmail", "weather" → weather.com, "vault"/"brain" → Obsidian, "browser" → Opera GX, "punch in" / "jarvis brain" → the claude.ai artifacts. Edit `Jarvis\jarvis_aliases.json` (read on every command, no restart); delete the `weather` alias if "open weather" should open the Windows Weather app instead.
- **Conversations (since 2026-09-22, `jarvis_conversation.py`):** only one conversation and one voice at a time. After "Yes, sir?" you have 3 s to start; after each answer, 2 s of no words ends the conversation and closes the response windows. Follow-ups keep context for 10 minutes ("what about Friday?").
- **Cutting him off:** just talk over him (he stops within ~0.3 s once your voice is clearly louder than his echo), or say "Hey Jarvis". "Shut up", "stop", "close", "cancel", "never mind", "that's all" silence him at once and close every response window; "thanks" / "okay" end the conversation quietly. Typed commands work the same way, and a typed command opens a 2 s window for a spoken follow-up.
- **Accuracy:** time, date, next shift / "do I work tomorrow", local weather and unread mail are answered exactly from the dashboard data (no model). Everything else goes to the local model with a short briefing of the dashboard and [[About Kayden]]; it's told to say "I don't have that" rather than guess.
- **Noise:** Jarvis measures the room from the seconds before "Hey Jarvis" and keeps re-measuring; speech must be 3× the room level, and steady sound (fan, hum) is ignored after 2.5 s.
- The orb is clickable: click once to mute (stops him talking, closes the response card, disables listening), click again to unmute (starts a new listening session). `/stop` is the kill switch without muting.

## Text-to-speech

- Voice (since 2026-09-23): Piper `en_GB-alan-medium`, fully offline. Nothing leaves the laptop. Fallback, or `JARVIS_TTS=edge`: Microsoft Edge neural `en-GB-RyanNeural` (audio generated online; the text is sent to Microsoft's speech service). Test: `Invoke-RestMethod "http://127.0.0.1:8765/speak?text=Jarvis%20online"`.
- Windows SAPI is available for manual testing only — Jarvis will not silently fall back to a non-British system voice for real responses. This machine currently only has US English Windows voices installed; add a British one under Settings > Time & language > Speech and restart the bridge to get the accent.
- Wake detection pauses during TTS playback so Jarvis doesn't trigger on its own voice, and resumes automatically after.
- Audio path: PyAV decode → `sounddevice` → default Windows output directly. No media-player process is launched, so nothing lingers to block the next response.

## Audio validation rule

Any time audio, wake response, or TTS playback code changes: test with an audible sentence through the real speaker path, then check `/status` for `speaking:false`, `ready:true`, no error. A 200 response alone is never proof sound reached the speakers.

## What's not written here

Ambient audio, raw microphone recordings, and full screenshots are never written to this vault. Kayden asked (2026-09-22) for the dashboard's contents to be mirrored in this vault: [[Punch In Dashboard/Dashboard snapshot|Dashboard snapshot]] holds what the dashboard shows (inbox subjects, Robinhood totals with last-4 masks only, shifts). Nothing beyond what the dashboard displays is copied — never full account numbers, credentials, or email bodies.
