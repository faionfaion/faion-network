---
slug: survey-design
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Designs a bias-linted survey: <=12 questions, no leading/double-barreled/loaded wording, mandatory open-text for top 2 themes, sample-size N>=120 per segment for 90% CI +/-9%.
content_id: "1f2db72381860c1d"
complexity: medium
produces: spec
est_tokens: 4400
tags: [survey, quantitative, bias-lint, sample-size]
---
# Survey Design

## Summary

**One-sentence:** Designs a bias-linted survey: <=12 questions, no leading/double-barreled/loaded wording, mandatory open-text for top 2 themes, sample-size N>=120 per segment for 90% CI +/-9%.

**One-paragraph:** Survey-authoring methodology producing a survey doc + bias-lint pass + sample-size checklist. Caps at 12 questions per survey, enforces bias linting (no leading, double-barreled, loaded, or assumes-prior-knowledge wording), requires open-text fields for the top 2 themes, and demands N>=120 responses per segment for 90% CI +/-9% before publishing any conclusion.

**Ефективно для:**

- Quantitative validation після qualitative interviews.
- Pricing willingness-to-pay survey.
- NPS / CSAT квартальний пульс.
- Feature-prioritisation MaxDiff survey.
- Persona segmentation: підтвердити hypothesis по >=120 респондентах.

## Applies If (ALL must hold)

- Quantitative validation after qualitative interviews.
- Willingness-to-pay (pricing) survey.
- Quarterly NPS / CSAT pulse.
- Feature-prioritisation MaxDiff or Kano survey.
- Persona segmentation validation across >=120 respondents.

## Skip If (ANY kills it)

- Pre-interview exploration; do qualitative first.
- Open-ended discovery; use interviews + observation.
- Single-question pulse via SMS / popup (not a survey).
- Compliance-mandated survey with fixed wording (no design freedom).
- Sample < 30 (no statistical interpretation possible).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis to test | 1 sentence | PM / researcher |
| Target segment list | persona doc | persona-building |
| Distribution channel + expected reach | estimate | GTM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[persona-building]] | supplies the segments and minimum sample-size targets |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-questions` | sonnet | Compose <=12 questions ordered easy -> hard -> demographics. |
| `bias-lint` | haiku | Mechanical regex + pattern check for leading/double-barreled/loaded. |
| `sample-size-calc` | haiku | Compute required N per segment for CI target. |
| `pilot-and-iterate` | sonnet | Run pilot N=10; rewrite questions with confusion signals. |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-design-doc.md` | Survey doc skeleton (hypothesis + questions + sample plan) |
| `templates/question-bank.md` | Pre-vetted question phrasings by survey type |
| `templates/bias-linter.py` | Lint questions for leading/double-barreled/loaded patterns |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-survey-design.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[user-research-at-scale]]
- [[persona-building]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
