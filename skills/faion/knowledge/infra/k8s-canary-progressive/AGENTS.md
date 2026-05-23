# Kubernetes Canary and Progressive Delivery

## Summary

**One-sentence:** Progressive-delivery spec (config): Argo Rollouts / Flagger strategy, weight steps, analysis templates with SLO queries, auto-promote / auto-rollback thresholds.

**One-paragraph:** Progressive-delivery spec (config): Argo Rollouts / Flagger strategy, weight steps, analysis templates with SLO queries, auto-promote / auto-rollback thresholds. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Releasing a stateless service where failure-blast-radius matters.
- Adopting Argo Rollouts or Flagger for progressive delivery.
- Wiring SLO-driven auto-promote / auto-rollback to a release.
- Replacing big-bang rollout with traffic-shifting canary.

## Skip If (ANY kills it)

- Single-replica service - no canary traffic available.
- Workload requires strict in-order traffic (state machine) - canary mixes versions.

**Ефективно для:**

- HTTP services з measurable error-rate + latency SLOs.
- GitOps + automated rollback.
- Multi-step weight shifts (5/25/50/100).
- Service-mesh-backed traffic splitting (Istio / Linkerd).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Argo Rollouts / Flagger installed | cluster addon | platform team |
| SLO source (Prometheus / Cloud Monitoring) | metrics | platform team |
| Service mesh OR ingress controller with traffic-split support | infra | platform team |
| Defined SLOs (error-rate + latency) | doc | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-rolling-update` | Baseline rolling-update conventions. |
| `pro/infra/infrastructure-engineer/k8s-deployment-workloads` | Deployment shape. |

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
| `scripts/validate-k8s-canary-progressive.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-rolling-update]]
- [[k8s-deployment-workloads]]
- [[k8s-scaling-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
