# Gce Spot Vms

## Summary

**One-sentence:** Use GCE Spot VMs (up to 91% discount) for fault-tolerant batch and burst workloads: instance templates, shutdown scripts, MIG autohealing, GKE spot node pools, and cost-optimization patterns.

**One-paragraph:** Spot VMs offer up to 91% discount over standard on-demand pricing but can be preempted by GCP with a 30-second warning at any time. Spot VMs have no 24-hour limit (unlike the legacy Preemptible VMs they replace) and support the same machine types, regions, and features. They are suitable for batch processing, dev/test environments, fault-tolerant stateless services, and GKE burst capacity. Always use MIGs with autohealing to automatically recreate preempted instances.

**Ефективно для:**

- Batch workload, що толерує переривання (preempted < 24h).
- Stateless workers з checkpointing у Cloud Storage.
- Mixed MIG зі стандартними + Spot VMs для baseline + burst.
- Significant cost saving (60–91%) на non-critical compute.

## Applies If (ALL must hold)

- Batch processing pipelines (data transforms, ML training, rendering) that checkpoint progress — preemption loses at most one checkpoint interval of work.
- Dev and test environments — workloads are not user-facing; interruptions are acceptable and savings are significant.
- GKE burst capacity via spot node pools — non-critical Pods run on spot nodes with tolerations; critical Pods remain on standard nodes.
- Stateless microservices with MIG autohealing and enough instances that losing one zone's Spot capacity does not breach SLO.
- CI/CD build agents — builds are retried on preemption; savings are 60-91%.

## Skip If (ANY kills it)

- Stateful workload that cannot be checkpointed or restarted.
- Production-critical SLO that cannot tolerate preemption.
- Steady, predictable load — committed-use discounts may be cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload tolerance | checkpoint design doc | team |
| Checkpoint store | Cloud Storage bucket | data eng |
| Restart hook | shutdown script | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gce-instance-templates]] | Sibling methodology that supplies context required here. |
| [[gce-managed-instance-groups]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gce-spot-vms.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gce-spot-vms.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gce-spot-vms.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gce-instance-templates]]
- [[gce-managed-instance-groups]]
- [[gce-autoscaling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gce-spot-vms vs an adjacent sibling).
