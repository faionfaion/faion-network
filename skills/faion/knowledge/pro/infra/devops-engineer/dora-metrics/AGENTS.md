---
slug: dora-metrics
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a DORA metrics dashboard spec: data sources, four core metrics + reliability, target band, collection cadence, and feedback loop into team rituals.
content_id: "eefb9f9546876c33"
complexity: medium
produces: config
est_tokens: 4400
tags: [dora, delivery, metrics, mttr, deployment-frequency]
---
# DORA Metrics

## Summary

**One-sentence:** Generates a DORA metrics dashboard spec: data sources, four core metrics + reliability, target band, collection cadence, and feedback loop into team rituals.

**One-paragraph:** Generates a DORA metrics dashboard spec: data sources, four core metrics + reliability, target band, collection cadence, and feedback loop into team rituals. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший DORA dashboard з Git + CI + incident сигналів.
- Перевід команди на elite-tier (deploy ≥1×/day, MTTR <1h).
- Quarterly retro якорі через DORA tier change.
- Платформенний benchmark для multi-team org.

## Applies If (ALL must hold)

- Team has a measurable delivery pipeline (Git → CI → deploy).
- Leadership wants outcome-level metrics (not vanity output).
- At least one cycle of metric review can run per quarter.

## Skip If (ANY kills it)

- Team is pre-deployment-pipeline (still hand-rolling releases) — instrument the pipeline first.
- No leadership buy-in; metrics will be theatre without action.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Deploy event source | CI / CD / k8s rollout | Platform |
| Incident source | PagerDuty / OpsGenie / Jira | SRE |
| Commit/MR source | Git platform API | Platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | upstream context not required |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-dora-metrics` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dora-metrics.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-platform-idp-core]]
- [[finops]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
