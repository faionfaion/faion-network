# Text-to-Speech Basics

## Summary

Convert text to natural speech using OpenAI TTS, ElevenLabs, or Google Cloud TTS. Covers voice
selection, SSML control for Google/Azure, caching by content hash, and the provider differences
every agent must know before routing a TTS call.

## Why

TTS providers have incompatible interfaces, rate limits, and SSML support. A call that works with
Google Cloud will produce literal angle-bracket noise in OpenAI TTS. Caching by `sha256(text +
voice + speed + model)` eliminates cost for repeated phrases — omitting it wastes money on every
pipeline replay.

## When To Use

- Converting article, news, or notification text to audio in an agent pipeline.
- Generating narration tracks for video content automation.
- Adding voice output to a chatbot or assistant interface.
- Creating audio previews of generated text for human review.
- Any single-pass synthesis where text fits under 4000 characters.

## When NOT To Use

- Text exceeds 4000 characters — use `tts-implementation` which provides `LongTextTTS` chunking.
- Sub-200ms latency required — OpenAI TTS adds 300-800ms minimum; cache known phrases instead.
- A specific person's voice is required — use ElevenLabs voice cloning (`tts-implementation`).
- SSML markup (pauses, prosody, say-as) is needed with OpenAI TTS — OpenAI does not support SSML;
  route SSML to Google Cloud or Azure only.
- Text contains heavy domain abbreviations (API, ETA, DB) without preprocessing — they are read
  literally and sound odd to listeners.

## Content

| File | What's inside |
|------|---------------|
| `content/01-providers.xml` | Provider comparison, voice options, model tiers, rate limits, cost. |
| `content/02-rules.xml` | Caching rule, SSML routing rule, text preprocessing rules, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts_basic.py` | `text_to_speech()` OpenAI wrapper + `SSMLBuilder` for Google/Azure. |
| `templates/voice-map.py` | Semantic voice routing by content type (news/assistant/narrator). |
| `templates/prompt-tts.txt` | Agent task prompt for TTS subagent (structured input/output). |
