---
slug: ai-interview-analysis
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A two-stage pipeline for transcribing recorded user interviews and extracting themes, sentiment, and cross-interview patterns at scale.
content_id: "2e50fff8bb9b87fb"
tags: [interviews, transcription, thematic-analysis, user-research, whisper]
---
# AI-Assisted Interview Analysis

## Summary

**One-sentence:** A two-stage pipeline for transcribing recorded user interviews and extracting themes, sentiment, and cross-interview patterns at scale.

**One-paragraph:** A two-stage pipeline for transcribing recorded user interviews and extracting themes, sentiment, and cross-interview patterns at scale. Haiku handles transcription; Sonnet extracts themes per interview; Opus synthesizes patterns across interviews. Human review is required between stages 2 and 3.

## Applies If (ALL must hold)

- Transcribing recorded user interviews or usability sessions (audio/video files).
- Extracting themes and sentiment across a batch of 5+ interviews in parallel.
- Building a research repository searchable by insight, theme, or participant.
- Pre-processing transcripts before human thematic analysis to remove mechanical work.

## Skip If (ANY kills it)

- When the interview moderation itself needs to be automated — AI cannot facilitate nuanced probing
- When the research question requires nonverbal behavioral data (gaze, hesitation, body language)
- When audio quality is poor (heavy accent + background noise) — transcription accuracy drops below 80%, making analysis unreliable
- When participant confidentiality is high-risk and SaaS tools cannot be used — run local transcription (Whisper) instead
- As a replacement for the researcher's interpretive judgment — themes require human validation before becoming findings

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

- parent skill: `geek/research/researcher/`
