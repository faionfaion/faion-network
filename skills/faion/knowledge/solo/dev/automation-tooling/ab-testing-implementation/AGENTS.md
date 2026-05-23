---
slug: ab-testing-implementation
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Implements typed ExperimentEvent, ExperimentTracker with in-request exposure dedup, ExperimentAnalyzer using z-test + Wilson CIs, and ExperimentReporter for dashboards.
content_id: "4e7814564a65017a"
complexity: deep
produces: code
est_tokens: 4300
tags: [a-b-testing, experiment-tracking, statistical-analysis, event-analytics, reporting]
---
# A/B Testing Implementation

## Summary

**One-sentence:** Implements typed ExperimentEvent, ExperimentTracker with in-request exposure dedup, ExperimentAnalyzer using z-test + Wilson CIs, and ExperimentReporter for dashboards.

**One-paragraph:** Implements typed ExperimentEvent, ExperimentTracker with in-request exposure dedup, ExperimentAnalyzer using z-test + Wilson CIs, and ExperimentReporter for dashboards. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Building plumbing for experiments: deterministic assignment, exposure tracking, conversion events.
- Need a typed event layer landing cleanly in Mixpanel/Amplitude/PostHog/warehouse.
- Stakeholders demand confidence intervals and per-variant breakdowns, not just point estimates.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Building plumbing for experiments: deterministic assignment, exposure tracking, conversion events.
- Need a typed event layer landing cleanly in Mixpanel/Amplitude/PostHog/warehouse.
- Stakeholders demand confidence intervals and per-variant breakdowns, not just point estimates.

## Skip If (ANY kills it)

- Using a managed platform (Optimizely, GrowthBook) that already provides analyzer + dashboards.
- Only a single experiment per quarter — manual SQL is cheaper than building plumbing.
- No exposure model yet — design the experiment first (see ab-testing-basics).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Experiment definition | experiment_definition.json | ab-testing-basics output |
| Event schema | TypedDict / Pydantic model | team |
| Analytics sink | Mixpanel/Amplitude/PostHog/Postgres | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ab-testing-basics]] | experiment design and sample-size calculation upstream of this code |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-event-types` | haiku | Mechanical typed dataclass + Pydantic model generation. |
| `implement-analyzer` | sonnet | Z-test + Wilson interval requires careful numeric code. |
| `dashboard-reporter` | sonnet | Layout + per-variant breakdown. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment_event.py` | Typed ExperimentEvent (exposure + conversion) with stable schema |
| `templates/analyzer.py` | Two-proportion z-test with Wilson 95% CI |
| `templates/_smoke-test.py` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ab-testing-implementation.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[ab-testing-basics]]
- [[feature-flags-types-lifecycle]]
- [[feature-flags-services-testing]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a managed platform with an analyzer, or do we own plumbing?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
