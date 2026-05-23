---
slug: ab-testing
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Run a controlled experiment comparing one variant against control on a pre-declared primary metric, with sample-size and guardrail definitions, and emit a stop / ship / iterate decision with statistical confidence."
content_id: "b7f4b22564934e1d"
complexity: deep
produces: spec
est_tokens: 4800
tags: ["ab-testing", "quantitative-research", "experimentation", "statistics", "conversion-optimization"]
---
# A/B Testing

## Summary

**One-sentence:** Run a controlled experiment comparing one variant against control on a pre-declared primary metric, with sample-size and guardrail definitions, and emit a stop / ship / iterate decision with statistical confidence.

**One-paragraph:** Design decisions made on opinion produce debates without resolution. This methodology pins the A/B test plan: one primary metric (declared before the test), one variant against control (multi-variant tests are split or use a different methodology), pre-computed sample size for the minimum detectable effect, guardrail metrics that cannot regress, an end-date that does not slide, and a typed decision (SHIP | KILL | ITERATE) read from the result. Output: an experiment spec artefact downstream analysts and engineers consume without re-deriving the design.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Conversion-optimisation experiments on a live product with sufficient traffic.
- Pricing or packaging tests where revenue impact can be measured.
- Onboarding flow changes where a primary activation metric is well-defined.
- Validating a UX hypothesis after qualitative research suggested a directional change.

## Skip If (ANY kills it)

- Traffic is too low to reach significance within a reasonable window — use qualitative testing or analytics interpretation instead.
- The change is regulatory or accessibility-mandated — ship without A/B; testing is theatre.
- Multiple uncontrolled changes are launching simultaneously — A/B confounds will swamp signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Primary metric definition | event + filter rules | success-metrics spec |
| Baseline conversion rate | 4-week average | analytics export |
| Sample-size calculation | inputs: baseline, MDE, power, alpha | pre-test computation |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/success-metrics-definition` | supplies the primary + guardrail metrics |
| `solo/ux/ux-researcher/heuristic-evaluation` | sibling lens — qualitative complement to quantitative experiments |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ab-testing.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-ab-testing.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[success-metrics-definition]]
- [[heuristic-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
