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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-synthetic-users.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-persona-building]]
- [[ai-interview-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/synthetic-report.json`

```json
{
  "concepts": [
    {
      "id": "c1",
      "summary": "Onboarding cuts to 3 steps"
    },
    {
      "id": "c2",
      "summary": "Onboarding adds biometric"
    },
    {
      "id": "c3",
      "summary": "Onboarding offers SSO-only"
    },
    {
      "id": "c4",
      "summary": "Onboarding offers passkey-only"
    },
    {
      "id": "c5",
      "summary": "Onboarding deferred to first-action"
    }
  ],
  "synthetic_reactions": [
    {
      "concept_id": "c1",
      "reaction": "Welcome \u2014 fewer steps reads as professional.",
      "surprise_flag": false
    }
  ],
  "decision_grade": false,
  "validation_plan_url": "FILL_ME",
  "validation_window_days": 21,
  "high_stakes_disallowed": true
}
```

### `templates/prompt-synthetic-reaction.txt`

```text
Prompt template — Agent prompt for synthetic user reactions.

Fill the slots below per task.

[CONTEXT]
...

[TASK]
...

[OUTPUT_FORMAT]
...

[CONSTRAINTS]
- Follow content/01-core-rules.xml.
- Output MUST validate against content/02-output-contract.xml.
```

### `templates/_smoke-test.json`

```json
{
  "concepts": [
    {
      "id": "c1",
      "summary": "Onboarding cuts to 3 steps"
    },
    {
      "id": "c2",
      "summary": "Onboarding adds biometric"
    },
    {
      "id": "c3",
      "summary": "Onboarding offers SSO-only"
    },
    {
      "id": "c4",
      "summary": "Onboarding offers passkey-only"
    },
    {
      "id": "c5",
      "summary": "Onboarding deferred to first-action"
    }
  ],
  "synthetic_reactions": [
    {
      "concept_id": "c1",
      "reaction": "Welcome \u2014 fewer steps reads as professional.",
      "surprise_flag": false
    }
  ],
  "decision_grade": false,
  "validation_plan_url": "FILL_ME",
  "validation_window_days": 21,
  "high_stakes_disallowed": true
}
```
