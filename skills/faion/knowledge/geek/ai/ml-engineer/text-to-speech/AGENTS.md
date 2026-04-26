# Text-to-Speech

## Summary

Convert text to natural-sounding audio using TTS APIs. ElevenLabs is the quality and latency leader (75ms Flash v2.5, voice cloning); Google/Azure are the cost leaders for high-volume production; OpenAI TTS integrates natively in OpenAI stacks. Always normalize abbreviations before synthesis and cache by content hash to avoid redundant API calls.

## Why

TTS enables automated audio pipelines (podcasts, audiobooks, video narration, accessibility, IVR) that scale without human voice actors. The market inflection point is 2025-2026 as latency drops below 100ms for real-time voice apps. Key failure modes — mispronounced abbreviations, long-text chunking artifacts, inconsistent cloned voices — are entirely preventable with text normalization and proper chunking at sentence boundaries.

## When To Use

- Automated podcast/audiobook generation from text content pipelines
- Voice narration for video generation workflows
- Accessibility layer for web or app content
- IVR or conversational voice bot responses requiring low-latency audio
- Agent workflows that produce audio reports or briefings

## When NOT To Use

- One-off manual narration where a human voice actor produces higher perceived quality
- Real-time &lt;75ms latency required and ElevenLabs Flash is not in budget
- Languages with less than 5% coverage in target voice model
- High-volume pipelines where ElevenLabs cost per character exceeds budget ceiling (use Google/Azure)
- Voice consistency across sessions is critical but cloning samples are unavailable

## Content

| File | What's inside |
|------|---------------|
| `content/01-providers.xml` | Provider comparison (ElevenLabs, OpenAI, Google, Azure, Coqui), selection rules by use case |
| `content/02-pipeline.xml` | Text normalization rules, chunking at sentence boundaries, streaming PCM, caching strategy, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/tts-cached.py` | ElevenLabs TTS with content-hash cache and text normalizer |
| `templates/chunk-text.py` | Sentence-boundary text chunker for long documents |
