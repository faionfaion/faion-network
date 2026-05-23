# Grafana — Deployment and Provisioning

## Summary

**One-sentence:** Generates a Grafana deployment config (Docker / Kubernetes / HA topology + database backend + provisioning configuration + Alloy agent migration + RBAC + backup) for production-grade setup.

**One-paragraph:** Generates a Grafana deployment config (Docker / Kubernetes / HA topology + database backend + provisioning configuration + Alloy agent migration + RBAC + backup) for production-grade setup. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Production Grafana deploy: K8s (Helm) або Docker з HA topology.
- Configuration-as-code: provisioning/datasources, dashboards, alerting.
- Міграція з Grafana Agent на Alloy (Agent EOL Nov 2025).
- HA setup з shared Postgres/MySQL та session storage.

## Applies If (ALL must hold)

- Need to deploy or upgrade a Grafana instance for production.
- HA / multi-replica setup required (≥2 nodes behind LB).
- Provisioning-as-code (datasources/dashboards/alerts via files).
- Migration from Grafana Agent → Alloy (Agent EOL Nov 2025).

## Skip If (ANY kills it)

- Local single-user Grafana for dev — Docker Compose is sufficient without ceremony.
- Managed Grafana (Grafana Cloud) — provisioning UI is the supported path.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target platform | kubernetes / docker / vm | Platform team |
| Database backend | Postgres / MySQL URL | Platform team |
| Provisioning repo | git path | SRE team |
| Backup target | S3 bucket / volume | Platform team |

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
| `draft-grafana-setup` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-grafana-setup.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
