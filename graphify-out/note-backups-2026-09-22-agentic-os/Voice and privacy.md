---
tags: [jarvis, reference]
---

# Voice and privacy

- Wake phrase: `Hey Jarvis`. Microphone audio is never sent to a cloud service.
- Mic selection: prefers a plugged headset/earbud, falls back to the laptop mic array; only the selected input stream is opened (never both). Override with `JARVIS_INPUT_DEVICE` (default `auto`) in `start-jarvis.cmd`.
- Wake detection: 0.2 VAD threshold, 0.35 wake score threshold — override with `JARVIS_VAD_THRESHOLD` / `JARVIS_WAKE_THRESHOLD` when tuning for a different mic.
- After wake: mic window stays open while you speak, ends ~0.8s after silence, 30-second safety max. Command capture calibrates an ambient-noise floor, applies a 180Hz high-pass filter, and requires two consecutive above-threshold chunks before it starts — cuts down on TV/fan/room noise (not a guarantee against nearby human speech).
- Transcription: local faster-whisper, kept warm after first use.
- Routing: `open calendar`, `open Gmail`, `open weather`, `open calculator`, `open Notepad` are safe allowlisted actions; `what time is it` answered locally; everything else goes to the local Ollama model (or configured fallback) and is spoken back. `/command?text=...` tests routing without the mic.
- Follow-ups: after the first response, keep talking without repeating the wake phrase. Say `close` to end the session. No speech for 4 seconds also ends it and returns to standby.
- The orb is clickable: click once to mute (disables listening, closes the response card), click again to unmute (starts a new listening session).

## Text-to-speech

- Preferred voice: Microsoft Edge neural `en-GB-RyanNeural` (audio generated online — text is sent to Microsoft's speech service for this). Test: `Invoke-RestMethod "http://127.0.0.1:8765/speak?text=Jarvis%20online"`.
- Windows SAPI is available for manual testing only — Jarvis will not silently fall back to a non-British system voice for real responses. This machine currently only has US English Windows voices installed; add a British one under Settings > Time & language > Speech and restart the bridge to get the accent.
- Wake detection pauses during TTS playback so Jarvis doesn't trigger on its own voice, and resumes automatically after.
- Audio path: PyAV decode → `sounddevice` → default Windows output directly. No media-player process is launched, so nothing lingers to block the next response.

## Audio validation rule

Any time audio, wake response, or TTS playback code changes: test with an audible sentence through the real speaker path, then check `/status` for `speaking:false`, `ready:true`, no error. A 200 response alone is never proof sound reached the speakers.

## What's not written here

Ambient audio, raw microphone recordings, and full screenshots are never written to this vault. Kayden asked (2026-09-22) for the dashboard's contents to be mirrored in this vault: [[Punch In Dashboard/Dashboard snapshot|Dashboard snapshot]] holds what the dashboard shows (inbox subjects, Robinhood totals with last-4 masks only, shifts). Nothing beyond what the dashboard displays is copied — never full account numbers, credentials, or email bodies.
