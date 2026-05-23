---
slug: api-monitoring-metrics
tier: pro
group: software-developer
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource.
content_id: "c3dca0b38adcc5c6"
complexity: medium
produces: config
est_tokens: 3600
tags: [api-monitoring, prometheus, metrics, red-method, observability]
---
# API Monitoring — Metrics

## Summary

**One-sentence:** Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource.

**One-paragraph:** Instrument every API using the RED method (Rate, Errors, Duration) per endpoint and USE method (Utilization, Saturation, Errors) per resource. This methodology pins the testable rules, output contract, and procedure that turn the abstract pattern into a reviewable artefact. Apply when the preconditions hold; otherwise the decision tree routes to `skip-this-methodology`. Output is the artefact described in `content/02-output-contract.xml`, validated by the bundled script.

**Ефективно для:**

- Team that needs a reusable, reviewable take on api monitoring — metrics for production code or operations.
- Cross-team alignment on the contract this methodology produces (no hand-rolled variants).
- Onboarding new contributors to the software-developer domain via a worked example + decision tree.
- Audit: traceable rule IDs in every conclusion of the decision tree.
- Pre-flight check before scoping a larger initiative that depends on this pattern.

## Applies If (ALL must hold)

- Task signal matches the scope of this methodology (see decision tree).
- The produced artefact has a named downstream consumer who will review it.
- Required inputs (data, repo state, infra access) are reachable when the work starts.
- The team can absorb the procedure without violating the failure-mode detectors.

## Skip If (ANY kills it)

- Task is clearly outside this methodology's scope — see `06-decision-tree.xml` for the skip branch.
- A more specific methodology already covers the exact use case better.
- The required preconditions for the failure-mode repairs cannot be met.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal | Markdown / JSON | requester |
| Parent skill context | Markdown | `pro/dev/software-developer/AGENTS.md` |
| Existing artefact (if updating) | per output-contract | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + `skip-this-methodology` rule | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-api-monitoring-metrics` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | JSON skeleton for the config artefact |
| `templates/config.md` | Markdown skeleton for the config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-monitoring-metrics.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/software-developer/AGENTS.md`
- Sibling methodologies: see `pro/dev/software-developer/` index

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
