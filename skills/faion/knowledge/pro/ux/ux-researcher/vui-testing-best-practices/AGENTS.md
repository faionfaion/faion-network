---
slug: vui-testing-best-practices
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: VUI testing across three accuracy tiers with deterministic assertions and LLM-judge scoring.
content_id: "ada06c04a4224ca6"
tags: [voice-testing, quality-assurance, llm-judge, nlu-testing, asr]
---
# VUI Testing Best Practices

## Summary

**One-sentence:** VUI testing across three accuracy tiers with deterministic assertions and LLM-judge scoring.

**One-paragraph:** VUI testing across three accuracy tiers with deterministic assertions and LLM-judge scoring.

## Applies If (ALL must hold)

- Pre-launch validation of an Alexa Skill, Google Action, or custom voice agent: stress-test intent recognition + dialog flow before certification.
- Multilingual/accent expansion: regression-test ASR accuracy and prompt naturalness across locales using batched audio fixtures.
- Continuous regression: every voice prompt or NLU model change re-runs a corpus of utterance fixtures and asserts intent + slot extraction accuracy.
- Field testing prep: scripted noise-injection runs before recruiting real users.

## Skip If (ANY kills it)

- Voice is a single shortcut, not a primary interface (e.g., a "tap-and-hold to speak" search): standard usability testing covers it.
- You don't yet have a working dialog model — start with Wizard-of-Oz prototyping, not test automation.
- Single-turn command testing only: an NLU benchmark (intent classification F1) is enough; a full VUI test suite is overkill.

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
