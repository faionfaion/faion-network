# Kubernetes Scaling and Availability

## Summary

**One-sentence:** Scaling + availability spec (config): HorizontalPodAutoscaler v2, topology-spread, anti-affinity, PDB, multi-AZ node-pool target - produced as deployment-extension manifest.

**One-paragraph:** Scaling + availability spec (config): HorizontalPodAutoscaler v2, topology-spread, anti-affinity, PDB, multi-AZ node-pool target - produced as deployment-extension manifest. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Adding HorizontalPodAutoscaler v2 to a service.
- Spreading pods across availability zones / nodes.
- Tightening PDB to survive node-pool upgrades.
- Recovering from co-located outages (all pods on one node).

## Skip If (ANY kills it)

- Workload with stable, predictable load - fixed replicas may be cheaper.
- Single-zone cluster - topology spread cannot help.

**Ефективно для:**

- Traffic-spiky web services з clear CPU/QPS signal.
- Multi-AZ clusters з node-pool diversity.
- Cost-controlled scale-up з max bounds.
- Cluster autoscaler integrated з HPA.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| metrics-server installed | cluster addon | platform team |
| Custom or external metrics adapter (if scaling on QPS) | addon | platform team |
| Multi-zone node pool | infra | platform team |
| Observed traffic profile (peak / trough) | metrics | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/k8s-resource-requests-limits` | Requests must be sane for HPA to work. |
| `pro/infra/infrastructure-engineer/k8s-rolling-update` | PDB design conventions. |

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-k8s-scaling-availability.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[k8s-rolling-update]]
- [[k8s-resource-requests-limits]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config.json`

```json
{
  "service": "acme-api",
  "hpa": {
    "api_version": "autoscaling/v2",
    "min_replicas": 3,
    "max_replicas": 20,
    "metrics": [
      {
        "type": "Resource",
        "resource": {
          "name": "cpu",
          "target": {
            "type": "Utilization",
            "averageUtilization": 70
          }
        }
      }
    ],
    "stabilization_window_seconds": 300
  },
  "topology_spread": {
    "topology_key": "topology.kubernetes.io/zone",
    "max_skew": 1
  },
  "pdb": {
    "name": "acme-api-pdb",
    "min_available": "60%"
  },
  "owner": {
    "name": "Olena Boyko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```

### `templates/_smoke-test.json`

```json
{
  "service": "acme-api",
  "hpa": {
    "api_version": "autoscaling/v2",
    "min_replicas": 3,
    "max_replicas": 20,
    "metrics": [
      {
        "type": "Resource",
        "resource": {
          "name": "cpu",
          "target": {
            "type": "Utilization",
            "averageUtilization": 70
          }
        }
      }
    ],
    "stabilization_window_seconds": 300
  },
  "topology_spread": {
    "topology_key": "topology.kubernetes.io/zone",
    "max_skew": 1
  },
  "pdb": {
    "name": "acme-api-pdb",
    "min_available": "60%"
  },
  "owner": {
    "name": "Olena Boyko",
    "role": "platform lead"
  },
  "produced_at": "2026-05-23T10:00:00Z"
}
```
