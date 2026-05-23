# A/B Testing Basics

## Summary

**One-sentence:** Defines an A/B experiment up-front: hypothesis, variants, primary metric, target sample size; deterministic hash-bucketing on (experiment_id+user_id) for stable assignment.

**One-paragraph:** Defines an A/B experiment up-front: hypothesis, variants, primary metric, target sample size; deterministic hash-bucketing on (experiment_id+user_id) for stable assignment. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Testing a UI/UX change (button text, layout, checkout flow) before full rollout.
- Evaluating an algorithm improvement (ranking, recommendation) with a quantitative success metric.
- Stakeholders accept a 1–4 week test horizon before shipping the winning variant.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Testing a UI/UX change (button text, layout, checkout flow) before full rollout.
- Evaluating an algorithm improvement (ranking, recommendation) with a quantitative success metric.
- Stakeholders accept a 1–4 week test horizon before shipping the winning variant.

## Skip If (ANY kills it)

- No clear primary metric or no instrumentation to measure it — instrument first.
- Sample size too small to reach 95% power on the expected effect — pick a higher-traffic surface.
- Change is a bug fix or accessibility fix that must ship regardless of metric movement.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment hypothesis | 1-sentence write-up | PM |
| Primary metric definition | metric name + numerator/denominator | analytics |
| Baseline rate + MDE | historical baseline + smallest effect worth detecting | analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ab-testing-implementation]] | plumbing for typed events, exposure dedup, and analyzer |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-experiment` | sonnet | Define hypothesis + metric + MDE + sample size. |
| `draft-bucketing-code` | haiku | Mechanical hash-based assignment. |
| `pre-register-doc` | sonnet | One-page pre-registration document. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment_definition.json` | Pre-registration template: hypothesis + variants + metric + MDE + target sample size |
| `templates/bucketing.py` | Deterministic hash-based bucketing for stable variant assignment |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing-basics.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[ab-testing-implementation]]
- [[feature-flags-rollout-targeting]]
- [[feature-flags-types-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a clear primary metric AND enough traffic to reach 80% power on the expected effect?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
