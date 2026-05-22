---
slug: vui-testing-best-practices
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A four-layer VUI test strategy: unit (intent accuracy), integration (dialog flow completion), user (moderated session with 5+ real users), stress (noise, accents, interruptions).
content_id: "ada06c04a4224ca6"
tags: [voice-ui, testing, usability-testing, voice-interfaces, vui]
---
# VUI Testing Best Practices

## Summary

**One-sentence:** A four-layer VUI test strategy: unit (intent accuracy), integration (dialog flow completion), user (moderated session with 5+ real users), stress (noise, accents, interruptions).

**One-paragraph:** A four-layer VUI test strategy: unit (intent accuracy), integration (dialog flow completion), user (moderated session with 5+ real users), stress (noise, accents, interruptions). Bucket accuracy by accent/age/gender — overall percentage hides subgroup failures of 15–30 points. Track "completion at attempt N" not just "completion" — N=2 is acceptable, N=4 is a failure. Lock LLM voice agent seeds for deterministic regression.

## Applies If (ALL must hold)

- Pre-launch validation of an Alexa skill, Google Action, custom IVR, or LLM voice agent.
- Regression testing after NLU model updates or prompt changes.
- Measuring intent accuracy, task completion, and error rate against a baseline.
- Stress-testing under realistic noise and accent diversity before scaling.

## Skip If (ANY kills it)

- TTS-only output (read-aloud, screen readers) — that is a11y testing, not VUI testing.
- Pure copy review without runtime testing — covered by content design heuristics.
- Latency or load tuning of the speech stack — use load testing tooling instead.

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

- parent skill: `pro/ux/ux-ui-designer/`
