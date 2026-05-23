# Gce Autoscaling

## Summary

**One-sentence:** Configure GCE autoscalers for MIGs using CPU, load-balancing, custom Cloud Monitoring metrics, schedule-based, and predictive signals with scale-in controls to prevent flapping.

**One-paragraph:** The GCE autoscaler adjusts the size of a Managed Instance Group in response to one or more scaling signals: CPU utilization, load balancing capacity, custom Cloud Monitoring metrics, time-based schedules, or ML-based predictive forecasting. Multiple signals can be combined; the autoscaler scales to whichever signal demands the most capacity. Scale-in controls prevent rapid downscaling that would cause flapping during brief traffic dips.

**Ефективно для:**

- Stateless web/API tier у Managed Instance Group зі stable load shape.
- CPU-target autoscaling (60–70%) як дефолт для compute-bound workload.
- Custom-metric autoscaling (queue depth) для воркерів через Cloud Monitoring.
- Scheduled scaling профілі для добового / робочого циклу.

## Applies If (ALL must hold)

- Any MIG-backed service with variable traffic — CPU-based autoscaling is the correct default.
- HTTP(S) services behind a Google Cloud Load Balancer — load balancing utilization signal tracks requests-per-second more accurately than CPU for frontend services.
- Queue-draining workers — custom Cloud Monitoring metric (queue depth) drives scaling proportional to backlog size.
- Predictable daily or weekly traffic patterns (e.g., business-hours web apps) — schedule-based autoscaling pre-provisions capacity before demand arrives.
- Applications with initialization time longer than 2 minutes — predictive autoscaling prevents latency spikes at ramp-up by starting instances before traffic arrives.

## Skip If (ANY kills it)

- Stateful workload that cannot tolerate instance replacement.
- GKE Pod autoscaling — use HPA/VPA/CA instead.
- Cloud Run autoscaling — use `cloud-run-autoscaling`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| MIG | existing MIG | GCE deploy |
| Scaling metric | CPU / custom / schedule | team |
| Min/max replicas | int range | capacity planner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gce-managed-instance-groups]] | Sibling methodology that supplies context required here. |
| [[gce-instance-templates]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gce-autoscaling.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gce-autoscaling.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gce-autoscaling.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gce-managed-instance-groups]]
- [[gce-instance-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gce-autoscaling vs an adjacent sibling).
