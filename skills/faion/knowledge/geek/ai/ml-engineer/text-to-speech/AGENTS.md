---
slug: text-to-speech
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Convert text to natural-sounding audio using TTS APIs.
content_id: "61f771d3a2960b3c"
tags: [text-to-speech, audio-synthesis, voice-cloning, streaming-audio, voice-pipeline]
---
# Text-to-Speech

## Summary

**One-sentence:** Convert text to natural-sounding audio using TTS APIs.

**One-paragraph:** Convert text to natural-sounding audio using TTS APIs. ElevenLabs is the quality and latency leader (75ms Flash v2.5, voice cloning); Google/Azure are the cost leaders for high-volume production; OpenAI TTS integrates natively in OpenAI stacks. Always normalize abbreviations before synthesis and cache by content hash to avoid redundant API calls.

## Applies If (ALL must hold)

- Automated podcast/audiobook generation from text content pipelines
- Voice narration for video generation workflows
- Accessibility layer for web or app content
- IVR or conversational voice bot responses requiring low-latency audio
- Agent workflows that produce audio reports or briefings

## Skip If (ANY kills it)

- One-off manual narration where a human voice actor produces higher perceived quality
- Real-time <75ms latency required and ElevenLabs Flash is not in budget
- Languages with less than 5% coverage in target voice model
- High-volume pipelines where ElevenLabs cost per character exceeds budget ceiling (use Google/Azure)
- Voice consistency across sessions is critical but cloning samples are unavailable

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
