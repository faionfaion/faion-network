---
slug: diary-study-execution
tier: pro
group: ux
domain: ux-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The operational and analytical phase of a running diary study: monitoring participant compliance, detecting low-quality entries, managing drop-off, coding entries against a fixed codebook, computing temporal patterns, and synthesizing findings into a structured report.
content_id: "a2a307acba101077"
tags: [diary-study, qualitative-research, participant-management, data-analysis, coding]
---
# Diary Study Execution and Analysis

## Summary

**One-sentence:** The operational and analytical phase of a running diary study: monitoring participant compliance, detecting low-quality entries, managing drop-off, coding entries against a fixed codebook, computing temporal patterns, and synthesizing findings into a structured report.

**One-paragraph:** The operational and analytical phase of a running diary study: monitoring participant compliance, detecting low-quality entries, managing drop-off, coding entries against a fixed codebook, computing temporal patterns, and synthesizing findings into a structured report. Lock the codebook before coding begins; adding themes mid-study invalidates cross-participant comparison.

## Applies If (ALL must hold)

- Multi-day diary study is already running and entries (text, photo, voice) are flowing into a single store.
- Cross-participant thematic and temporal coding of more than 50 entries with quote extraction and timeline charts.
- Mid-study quality monitoring: flag low-engagement participants, generic copy-paste entries, missed days.
- Producing the final report from already-coded data.

## Skip If (ANY kills it)

- Recruitment, screening, or onboarding calls — these require human trust and cannot be delegated to agents.
- Real-time participant chat or probing follow-up DMs while study is live (PII handling, emotional sensitivity).
- Studies where entries are voice-only without transcription pipeline or photos without vision/OCR — no usable text signal.
- Fewer than 5 participants — a human reads everything end-to-end faster than setting up the pipeline.

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

- parent skill: `pro/ux/ux-researcher/`
