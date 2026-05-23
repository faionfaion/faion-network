# Kubernetes LimitRange

## Summary

**One-sentence:** Per-namespace LimitRange config: container defaults, min/max bounds, ratio constraints - produced as a namespaced YAML applied before workloads.

**One-paragraph:** Per-namespace LimitRange config: container defaults, min/max bounds, ratio constraints - produced as a namespaced YAML applied before workloads. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Onboarding a new namespace that will host arbitrary workloads.
- Enforcing sane defaults so pods without explicit requests still get resources.
- Setting ratio limits (request:limit) to prevent runaway burst.
- Aligning a namespace with platform-wide resource defaults.

## Skip If (ANY kills it)

- Cluster-wide policy already covers the namespace (no per-ns override needed).
- Single-tenant dev cluster where defaults dont matter.

**Ефективно для:**

- Shared multi-team clusters.
- Namespaces що приймають foreign workloads (CI / sandbox).
- Compliance setups з required defaults.
- Cost-controlled namespaces з ratio enforcement.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Kubernetes namespace | k8s ns | platform team |
| Cluster resource baselines | doc | platform team |
| Workload size profile (small/medium/large) | doc | team |
| Operator/owner of the namespace | RACI | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-resource-requests-limits` | Per-container request/limit conventions. |

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
| `scripts/validate-k8s-limitrange.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[k8s-resource-requests-limits]]
- [[k8s-resource-quota]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
