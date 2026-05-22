---
slug: cognitive-walkthrough
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A structured expert-inspection method that evaluates interface learnability by stepping through a known correct action sequence and answering four questions per step: does the user know what to do, can they see how, does the label make sense, and do they get feedback that it worked?.
content_id: "7ff06f68352581bb"
tags: [usability, evaluation, learnability, expert-review, methodology]
---
# Cognitive Walkthrough

## Summary

**One-sentence:** A structured expert-inspection method that evaluates interface learnability by stepping through a known correct action sequence and answering four questions per step: does the user know what to do, can they see how, does the label make sense, and do they get feedback that it worked?.

**One-paragraph:** A structured expert-inspection method that evaluates interface learnability by stepping through a known correct action sequence and answering four questions per step: does the user know what to do, can they see how, does the label make sense, and do they get feedback that it worked?

## Applies If (ALL must hold)

- Evaluating learnability for first-time users: kiosks, sign-up flows, onboarding.
- Pre-launch sanity check before recruiting participants for usability testing.
- Auditing a defined task path (checkout, account setup) where the correct sequence is known.
- Government / public-service flows where novice users dominate.

## Skip If (ANY kills it)

- Open-ended exploratory tasks (browsing)—no single correct sequence exists.
- Replacing real user research: walkthrough finds learnability issues, not preference or value.
- Subjective brand or aesthetic review—heuristic evaluation is the right method.
- Late-stage efficiency tuning for expert users—use keystroke-level model (KLM) or GOMS.

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
