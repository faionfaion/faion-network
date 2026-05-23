# Kubernetes ResourceQuota

## Summary

**One-sentence:** Namespace ResourceQuota config: aggregate CPU/memory/storage caps, object-count caps, pod-priority scopes - produced as YAML enforced cluster-wide.

**One-paragraph:** Namespace ResourceQuota config: aggregate CPU/memory/storage caps, object-count caps, pod-priority scopes - produced as YAML enforced cluster-wide. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Onboarding a tenant namespace to a shared cluster.
- Capping the cluster cost a single team can consume.
- Limiting object counts (PVCs, Services, ConfigMaps) per namespace.
- Differentiating quotas across pod priority classes.

## Skip If (ANY kills it)

- Single-tenant cluster with no multi-tenancy boundary.
- Namespace is read-only (cluster-owned addons).

**Ефективно для:**

- Multi-team / multi-tenant clusters.
- Cost allocation by namespace.
- Fair-share scheduling з priority-class scopes.
- Compliance setups з hard caps.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes namespace | k8s ns | platform team |
| Cluster capacity baseline | doc | platform team |
| Tenant SLA / budget | doc | team / FinOps |
| LimitRange already in place | k8s object | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-limitrange` | Per-pod defaults that ResourceQuota relies on. |

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
| `scripts/validate-k8s-resource-quota.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-limitrange]]
- [[k8s-resource-requests-limits]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
