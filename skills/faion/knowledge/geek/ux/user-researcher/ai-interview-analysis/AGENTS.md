---
slug: ai-interview-analysis
tier: geek
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use AI to automate transcript processing and cross-interview theme extraction.
content_id: "2e50fff8bb9b87fb"
tags: [interview-analysis, transcription, theme-extraction, ai-agents, research]
---
# AI-Assisted Interview Analysis

## Summary

**One-sentence:** Use AI to automate transcript processing and cross-interview theme extraction.

**One-paragraph:** Use AI to automate transcript processing and cross-interview theme extraction. A local or cloud transcription model (Whisper, AssemblyAI) converts recordings to text, then a Claude agent segments speakers, extracts themes supported by verbatim quotes, scores sentiment, and produces a cross-interview pattern report. The human researcher reviews and interprets; the agent handles volume.

## Applies If (ALL must hold)

- Processing 5+ interview recordings where manual transcription/analysis would take days
- Extracting cross-interview themes for affinity diagramming or synthesis reporting
- Generating first-pass summaries of individual sessions before researcher review
- Running sentiment scoring on large transcript corpora to prioritize review order
- Producing pattern reports as input for product team debriefs

## Skip If (ANY kills it)

- Single sessions where a researcher can take notes live — no meaningful speed gain
- Moderated usability studies where in-session facilitator judgment is the core deliverable
- Studies involving sensitive disclosures (health, legal) without explicit AI-processing consent
- High-stakes research where hesitation, emotional cues, or nonverbal behavior are critical — AI is text-only
- Any pipeline where AI output goes to stakeholders without researcher review

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

- parent skill: `geek/ux/user-researcher/`
