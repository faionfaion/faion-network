---
slug: requirements-validation
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: BABOK Task 7.
content_id: "e3f08c20f288ffc2"
tags: [requirements, validation, babok, quality, sign-off]
---
# Requirements Validation

## Summary

**One-sentence:** BABOK Task 7.

**One-paragraph:** BABOK Task 7.6: confirms that requirements accurately represent the business need and deliver expected value before any downstream commitment. Five steps: review quality attributes, choose validation technique, conduct session, address findings, obtain sign-off. Distinct from Verification (BABOK 7.5), which checks form/ambiguity/testability — Validation asks "are we building the right thing?"

## Applies If (ALL must hold)

- BAKOK Task 7.6 trigger: a requirement or design is ready to be confirmed against business need before downstream commitment.
- Before requirements are baselined in a Requirements Repository — validation is the gate.
- When a stakeholder need is restated by an agent (summary, paraphrase, transcription) — close the loop on representational drift.
- When an existing baselined requirement is challenged by new information (regulation, market signal, data result).
- Capstone gate before transitioning from Requirements Analysis to Solution Evaluation.

## Skip If (ANY kills it)

- Pre-elicitation: nothing to validate yet — run elicitation-techniques and requirements-documentation first.
- Pure technical-quality concerns (form, style, consistency) — that is Verification, not Validation.
- Throwaway prototypes meant to provoke a reaction — the prototype is the elicitation tool, not a sign-off candidate.
- Operational/maintenance changes with no new business need (dependency bumps, refactors).
- After delivery — use Solution Evaluation (BABOK ch. 8) and feedback-loop measurement instead.

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

- parent skill: `pro/ba/ba-core/`
