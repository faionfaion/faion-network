---
slug: synthetic-users
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a directional feedback report from AI-generated research participants during ideation, with a mandatory human-validation gate before any product decision.
content_id: "8774b54c69030c96"
complexity: medium
produces: report
est_tokens: 4900
tags: [synthetic-users, ai-generated-participants, ideation, validation-gate, directional]
---
# Synthetic Users

## Summary

**One-sentence:** Produces a directional feedback report from AI-generated research participants during ideation, with a mandatory human-validation gate before any product decision.

**One-paragraph:** Synthetic users (AI-generated research participants) provide zero-cost directional feedback at ideation speed. They are NOT a substitute for real users — they reflect LLM priors, not your customer base. This methodology produces a directional report (concepts + simulated reactions + open questions) explicitly labelled requires-real-user-validation before any product decision. Used correctly, synthetic users compress idea-to-feedback from weeks to hours.

**Ефективно для:** founder / PM, що тестує 5–10 concept variants за день перед real-user research.

## Applies If (ALL must hold)

- Ideation: ≥5 concept variants need directional feedback before research budget.
- Output explicitly labelled not-decision-grade.
- Plan exists to validate top synthetic findings with real users within 30 days.

## Skip If (ANY kills it)

- Decision is high-stakes (medical / financial / safety) — synthetic users are unsafe here.
- Real-user research is available and affordable — use it.
- Validation plan does not exist — output will be misused.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Concept variants | markdown × N | PM |
| Target persona seed (synthetic basis) | JSON | PM |
| Validation plan (real users, 30 days) | markdown | research |
| Open questions list | list | PM |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-persona-building]] | Persona seed source for synthetic basis. |
| [[ai-interview-analysis]] | Real-user validation companion. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-report` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/synthetic-report.json` | JSON skeleton: concepts + reactions + decision_grade + validation + high_stakes flag. |
| `templates/prompt-synthetic-reaction.txt` | Agent prompt for synthetic user reactions. |
| `templates/_smoke-test.json` | Filled 5-concept ideation report. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-synthetic-users.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-persona-building]]
- [[ai-interview-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
