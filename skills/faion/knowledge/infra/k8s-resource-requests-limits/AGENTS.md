# Kubernetes Resource Requests and Limits

## Summary

**One-sentence:** Per-container request/limit config: CPU + memory pair design, QoS class targeting, headroom ratio, observability hooks - produced as patch spec for Deployment containers.

**One-paragraph:** Per-container request/limit config: CPU + memory pair design, QoS class targeting, headroom ratio, observability hooks - produced as patch spec for Deployment containers. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Tuning CPU / memory for a service that OOMs or is starved.
- Onboarding a new service that has zero requests/limits set.
- Aligning a workload to a target QoS class (Guaranteed / Burstable).
- Reducing cluster waste by right-sizing requests.

## Skip If (ANY kills it)

- Workload size has not been observed for at least one full traffic cycle.
- Cluster uses Vertical Pod Autoscaler in Auto mode for this workload.

**Ефективно для:**

- Latency-sensitive services що потребують Guaranteed QoS.
- Spike-prone web services з burstable headroom.
- Right-sizing на основі VPA recommendation.
- Cost reductions без regression.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Observed CPU + memory utilisation (p50, p95, p99) | metrics | platform team |
| Workload latency SLO | doc | team |
| LimitRange + ResourceQuota in namespace | k8s objects | platform team |
| VPA recommendation (optional) | k8s object | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-limitrange` | Defaults applied per namespace. |

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
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-resource-requests-limits.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-limitrange]]
- [[k8s-resource-quota]]
- [[k8s-scaling-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
