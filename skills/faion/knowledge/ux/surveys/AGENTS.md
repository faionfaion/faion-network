# Surveys and Questionnaires

## Summary

**One-sentence:** Produces a quantitative-survey instrument (NPS/CSAT/SUS/SEQ + custom items) with sampling plan, channel mix, fielding window, and analysis plan — validated for question-construction antipatterns before fielding.

**One-paragraph:** Surveys collect structured data from large user populations to quantify attitudes and validate qualitative findings at scale. This methodology emits a survey-instrument config: instrument (NPS / CSAT / SUS / SEQ / custom), sampling target, channel mix, fielding window, and analysis plan. It enforces standard rules — no double-barreled questions, no leading wording, ordinal-scale labels disclosed, response-rate target ≥ a benchmark. Output drives a tool-agnostic config consumed by Typeform / Qualtrics / SurveyMonkey / Google Forms.

**Ефективно для:**

- Validating qualitative research findings at scale (n ≥ 100).
- Benchmarking product satisfaction (NPS / CSAT / SUS / SEQ) over time.
- Pre / post launch feature-preference measurement.
- Multi-channel sampling (email + in-app + intercept) з documented bias-control.

## Applies If (ALL must hold)

- Research question requires quantification with confidence intervals.
- Sample size ≥ 100 is achievable within the fielding window.
- A documented analysis plan can be authored before fielding.

## Skip If (ANY kills it)

- n < 30 — qualitative methods produce better signal.
- Exploratory phase — surveys assume the constructs to measure are known.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Research question | Markdown | researcher |
| Sample-frame estimate | number | data team |
| Channel access | list of channels with quotas | marketing / product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | self-contained methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: instrument-mandatory, no-double-barrel, no-leading-wording, ordinal-labels-disclosed, response-rate-target, analysis-plan-pre-registered | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `frame-question` | sonnet | Concise question crafting. |
| `draft-items` | sonnet | Items + neutrality checks. |
| `lint-items` | haiku | Mechanical double-barrel + leading detector. |
| `analysis-plan` | sonnet | Pre-registration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-config.json` | Skeleton survey-config artefact |
| `templates/item-bank.csv` | Reusable item bank with neutral wording |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-surveys.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[tree-testing]]
- [[diary-studies]]
- [[focus-groups]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by research goal type to instrument + scale + channel; small-n branch routes to qualitative methods; post-hoc analyses are forced into exploratory flag. Each leaf cites a rule from `01-core-rules.xml`.
