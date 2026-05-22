---
slug: synthetic-users
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI-generated user profiles that simulate survey and interview responses for directional, pre-validation research.
content_id: "d6f934fd273d52f5"
tags: [synthetic-users, user-research, hypothesis-testing, ai-personas, validation]
---
# Synthetic Users

## Summary

**One-sentence:** AI-generated user profiles that simulate survey and interview responses for directional, pre-validation research.

**One-paragraph:** AI-generated user profiles that simulate survey and interview responses for directional, pre-validation research. Always labeled as synthetic; always followed by real-user validation before any product decision. The methodology's primary value is hypothesis triage — identifying what is worth investing in real-user research time.

## Applies If (ALL must hold)

- Early ideation: generating directional signal before real users can be recruited.
- Hypothesis stress-testing as a fast pre-filter ("Would this persona care about X?").
- Low-stakes concept validation where the cost of being wrong is recoverable.
- Generating adversarial edge-case responses to find blind spots in a survey instrument.
- Producing a research brief baseline that a human researcher then corrects.

## Skip If (ANY kills it)

- Go/no-go product decisions — synthetic data cannot replace real demand signal.
- Demand forecasting or pricing research — synthetic willingness-to-pay is systematically biased high.
- Any research where legal, medical, or safety consequences follow from findings.
- Final validation before launch — always run at least one round of real-user interviews.
- Stakeholder-facing deliverables presented as real research without disclosure.

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
