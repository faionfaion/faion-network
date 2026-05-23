# Service Bootstrap Checklist

## Summary

**One-sentence:** A 12-item bootstrap checklist for a new service: repo, CI, logging, metrics, healthcheck, runbook, on-call, dashboards, alerts, secrets, deploy, postmortem template.

**One-paragraph:** A 12-item bootstrap checklist for a new service: repo, CI, logging, metrics, healthcheck, runbook, on-call, dashboards, alerts, secrets, deploy, postmortem template. Day-one checklist a new service must satisfy before traffic. Each item has a binary 'done' criterion and an owner. Missing items block traffic, not just deployment. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- New service being stood up that will take production traffic within 30 days.
- Greenfield repo or extracted-from-monolith service without standardised observability.
- Want a defensible day-one floor reviewable by SRE / platform.
- Output produces `checklist` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- New service being stood up that will take production traffic within 30 days.
- Greenfield repo or extracted-from-monolith service without standardised observability.
- Want a defensible day-one floor reviewable by SRE / platform.

## Skip If (ANY kills it)

- Short-lived spike not destined for production.
- Service replicates an existing inheriting all bootstrap from a parent platform template (use template version instead).
- Internal cron job with no externally observable contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo creation rights | GitHub/GitLab perm | platform |
| Observability stack access | Prometheus/Grafana | ops |
| Secrets backend | vault/op | security |
| CI templates | yaml | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[logging-patterns]] | Structured logging applied at bootstrap. |
| [[qa-rollback-trigger-canon]] | Rollback triggers wired before traffic. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 7-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-from-template` | sonnet | Mechanical: instantiate template. |
| `verify-checklist` | haiku | Per-item binary check. |
| `write-runbook` | opus | Cross-cutting: synthesise the service contract into a runbook. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap_checklist.json` | JSON template scaffolding the artefact contract. |
| `templates/runbook.md` | Markdown skeleton for the artefact. |
| `templates/dashboards.json` | JSON template scaffolding the artefact contract. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-service-bootstrap-checklist.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[logging-patterns]]
- [[qa-rollback-trigger-canon]]
- [[decomposition-django]]
- [[django-celery]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is this a new production-bound service that will take traffic within 30 days?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
