# Multi-Burn-Rate SLO Recipe

## Summary

**One-sentence:** Multi-window multi-burn-rate SLO alert configuration: short+long windows for fast/slow burn detection, alert routing, false-positive tuning, runbook hooks.

**One-paragraph:** Multi-window multi-burn-rate SLO alert configuration: short+long windows for fast/slow burn detection, alert routing, false-positive tuning, runbook hooks. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`config`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Service has a published SLO with a defined error budget window (e.g. 30 days).
- Alerting platform supports multi-window multi-burn-rate expressions (Prom / Sumo / Datadog).
- On-call team agreed to consume burn-rate alerts (not raw error count).

## Skip If (ANY kills it)

- No SLO yet — define SLO first via slo-definition-template-per-service-class.
- Single-window alerting is fine for the maturity stage — multi-window overkill.
- Alert volume sensitivity prohibits any new alerts (need to clean up first).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SLO + window | YAML | slo-definition-template-per-service-class |
| Metric source | Prom / OTel | platform |
| Alert platform | Alertmanager / Datadog / Sumo | infra |
| On-call rotation | PagerDuty / OpsGenie | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/slo-definition-template-per-service-class` | Defines the SLO this recipe alerts against. |
| `geek/dev/software-developer/slo-burn-rate-review-protocol` | Consumer of the alerts produced. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `config_compose` | sonnet | Express recipe in target alerting DSL. |
| `threshold_tuning` | opus | Tune for false-positive trade-off. |
| `runbook_wiring` | sonnet | Link alert → runbook. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prometheus-rules.yaml` | Multi-window burn rate alert rules. |
| `templates/datadog-monitor.json` | Datadog SLO monitor JSON. |
| `templates/alert-routing.yaml` | Routing rules to on-call rotations. |
| `templates/_smoke-test.yaml` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-burn-rate-slo-recipe.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[slo-definition-template-per-service-class]]`
- `[[slo-burn-rate-review-protocol]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether multi-burn-rate-slo-recipe applies: root question — "Does the service have a published SLO with an error budget window AND an alerting platform that supports multi-window expressions?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
