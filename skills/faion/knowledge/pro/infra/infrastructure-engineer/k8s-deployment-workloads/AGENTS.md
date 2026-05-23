---
slug: k8s-deployment-workloads
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Workload-kind decision-record (config): Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob - pick rule + manifest skeleton with required fields per kind."
content_id: "7cb8d1aaa491110a"
complexity: medium
produces: decision-record
est_tokens: 3600
tags: [kubernetes, deployment, statefulset, daemonset, job]
---
# Kubernetes Deployment Workloads

## Summary

**One-sentence:** Workload-kind decision-record (config): Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob - pick rule + manifest skeleton with required fields per kind.

**One-paragraph:** Workload-kind decision-record (config): Deployment vs StatefulSet vs DaemonSet vs Job vs CronJob - pick rule + manifest skeleton with required fields per kind. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Choosing the right workload kind for a new service.
- Migrating a misclassified workload (e.g. StatefulSet that should be Deployment).
- Adding a periodic job to the cluster.
- Standardising workload-kind decisions across team services.

## Skip If (ANY kills it)

- Workload already running stably with a documented kind decision.
- Operator-managed workloads - CRD owns the choice.

**Ефективно для:**

- Stateless web/api - Deployment.
- Stable identity / ordered start - StatefulSet.
- Per-node agents (log/metric/CSI) - DaemonSet.
- One-shot / scheduled tasks - Job / CronJob.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload behaviour profile (stateless? identity? per-node? one-shot?) | doc | team |
| Kubernetes cluster | cluster | platform team |
| Image + entrypoint | OCI image | team |
| Persistence requirements | spec | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-basics` | Baseline manifest conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.json` | Decision-record skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-deployment-workloads.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-basics]]
- [[k8s-rolling-update]]
- [[k8s-scaling-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
