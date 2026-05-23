# QA Rollback Trigger Canon

## Summary

**One-sentence:** Pre-declared rollback triggers (error rate, latency, business KPI, customer alert) with thresholds, observation windows, and named on-call owner.

**One-paragraph:** Pre-declared rollback triggers (error rate, latency, business KPI, customer alert) with thresholds, observation windows, and named on-call owner. Triggers are observable signals + thresholds + windows + an owner. Hitting any one rolls back automatically (or with one-click on-call confirm). Decisions recorded. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Releases ship behind rolling deploy or canary and need automatic rollback signals.
- On-call has been blamed for slow rollback because thresholds were not pre-agreed.
- Have multiple incident types with different signals (latency, error, business).
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Releases ship behind rolling deploy or canary and need automatic rollback signals.
- On-call has been blamed for slow rollback because thresholds were not pre-agreed.
- Have multiple incident types with different signals (latency, error, business).

## Skip If (ANY kills it)

- Single VM deploy with no rollback mechanism — fix deploys first.
- Pre-product with no monitoring — write monitoring first.
- Compliance-locked release where rollback requires legal sign-off — different control.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Monitoring stack | Prometheus/Grafana/Datadog access | ops |
| Critical-path SLOs | ops/slo.yaml | ops |
| Deploy mechanism | rolling/canary tooling | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-perf-run-verdict-template]] | Perf verdict references the same SLOs. |
| [[qa-suite-health-metrics-canon]] | Suite health metrics may be signals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-triggers` | opus | Cross-cutting synthesis of incident history + SLOs. |
| `translate-to-monitor` | sonnet | Translate each trigger into a Prometheus alert rule. |
| `assign-on-call` | haiku | Lookup PagerDuty schedule for the named owner. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollback_canon.yaml` | YAML configuration scaffolding the artefact. |
| `templates/alerts.yaml` | YAML configuration scaffolding the artefact. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-rollback-trigger-canon.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-perf-run-verdict-template]]
- [[qa-rc-smoke-pack-template]]
- [[qa-bug-bash-runbook]]
- [[release-qa-cycle-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a rollback mechanism and monitoring to act on declared triggers?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
