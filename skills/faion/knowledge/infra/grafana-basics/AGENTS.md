# Grafana — Basics

## Summary

**One-sentence:** Generates a Grafana baseline config (datasource registry + dashboards-as-code via JSON / Grafonnet + alerting rules + folder structure + RBAC) covering metrics + logs + traces.

**One-paragraph:** Generates a Grafana baseline config (datasource registry + dashboards-as-code via JSON / Grafonnet + alerting rules + folder structure + RBAC) covering metrics + logs + traces. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший Grafana setup в команді — baseline що масштабується.
- Перехід з UI-clicked dashboards на dashboards-as-code (JSON / Grafonnet).
- Multi-datasource integration: Prometheus + Loki + Elastic.
- Alerting baseline: SLO-based rules з notification channels.

## Applies If (ALL must hold)

- Observability stack uses Grafana (any version).
- Dashboards or alerts will be maintained over time (≥3 months horizon).
- Multi-engineer team needs reproducible dashboards.
- At least one data source emits metrics, logs, or traces.

## Skip If (ANY kills it)

- Single-use ad-hoc dashboard with no maintenance horizon.
- Team has standardised on a non-Grafana viewer (Datadog, New Relic) without Grafana hybrid.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Data sources list | YAML (name, type, url) | Platform team |
| Dashboard repo path | git path | SRE team |
| Alert channel registry | YAML (channel → webhook/email) | SRE team |
| RBAC model | table (team → folder permissions) | Platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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
| `draft-grafana-basics` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-grafana-basics.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
