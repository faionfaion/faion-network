# Kubernetes Rolling Update

## Summary

**One-sentence:** Rolling-update strategy config: maxUnavailable / maxSurge tuning, PodDisruptionBudget pair, minReadySeconds, progressDeadlineSeconds - produced as a Deployment patch.

**One-paragraph:** Rolling-update strategy config: maxUnavailable / maxSurge tuning, PodDisruptionBudget pair, minReadySeconds, progressDeadlineSeconds - produced as a Deployment patch. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Rolling out a new image of an existing Deployment.
- Tuning surge / unavailable for a service with strict latency SLOs.
- Pairing a rollout with a PodDisruptionBudget for safe drain.
- Diagnosing flaky deploys (premature ready signal, partial rollout).

## Skip If (ANY kills it)

- Stateful workload - use rolling+ordered (StatefulSet) or migration.
- Cluster supports a progressive-delivery engine (Argo Rollouts / Flagger) - use canary instead.

**Ефективно для:**

- Stateless Deployments з multi-replica шейпом.
- Latency-sensitive services із strict PDB.
- Cluster autoscalers що drain nodes.
- Release ритуали з progressDeadline gating.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Deployment with >= 2 replicas | k8s object | team |
| Defined readiness + liveness probes | manifest | team |
| Latency / availability SLO | doc | team |
| Optional PodDisruptionBudget | k8s object | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-basics` | Baseline workload conventions. |

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
| `scripts/validate-k8s-rolling-update.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-canary-progressive]]
- [[k8s-deployment-workloads]]
- [[k8s-scaling-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
