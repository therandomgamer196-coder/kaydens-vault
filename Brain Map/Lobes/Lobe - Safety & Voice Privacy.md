---
type: lobe
region: Left temporal lobe
color: "#f43f5e"
neurons: 11
cohesion: 0.22
tags: [brain-map, lobe]
generated: 2026-09-22
---
# Lobe - Safety & Voice Privacy

> **Left temporal lobe** — hearing and judgement: wake word, transcription, routing, and the safety rules.

## Brain notes in this lobe

- [[brain/Core Brain Functions/Voice and privacy|Voice and privacy]]
- [[brain/Core Brain Functions/Safety rules|Safety rules]]

## Neurons

- [[Command routing]] — Allowlisted 'open' commands and time queries are handled locally; everything else goes to the local Ollama model and is spoken back.
- [[Untrusted data rule]] — Email and dashboard text is untrusted data and must never be followed as instructions.
- [[Safe sites]] — calendar, gmail and weather sites plus local calculator and Notepad are the only openers.
- [[OWASP prompt injection (LLM01)]] — OWASP GenAI risk page on prompt injection.
- [[Allowlisted commands]] — Only allowlisted commands and typed, permission-checked integrations; never arbitrary shell execution.
- [[No secrets in Obsidian]] — Never store credentials, access tokens, raw microphone audio or full screenshots in the vault.
- [[Vault mirroring limits]] — Ambient audio, raw recordings and screenshots are never written to the vault; only what the dashboard displays is mirrored, with account last-4 masks.
- [[Edge neural TTS (en-GB-RyanNeural)]] — Preferred text-to-speech voice; text is sent to Microsoft's speech service; wake detection pauses during playback.
- [[faster-whisper transcription]] — Local speech-to-text kept warm after first use.

## Wired to other lobes

- [[Lobe - Jarvis Core System]] — 4 connections
- [[Lobe - Future Integrations & Research]] — 3 connections
- [[Lobe - Reliability & Maintenance]] — 2 connections
- [[Lobe - Dashboard Data Sync]] — 1 connection
- [[Lobe - Dashboard UI Widgets]] — 1 connection

Back to [[Brain Map]]
