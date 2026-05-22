---
slug: capacity-headroom-check
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: For each capacity-bound resource (compute, db connections, queue depth, storage), current utilization vs.
content_id: 11901448e3b392f1
methodology_refs:
  - finops-devops-cost-rightsizing
  - prometheus-monitoring
  - aws-monitoring-observability
  - cloud-run-autoscaling
  - gce-autoscaling
  - k8s-limitrange
  - k8s-resource-quota
  - k8s-scaling-availability
---

# Capacity headroom check

**Slug:** `capacity-headroom-check` · **Tier:** pro · **Complexity:** light

## Context

For each capacity-bound resource (compute, db connections, queue depth, storage), current utilization vs. 30-day peak is recorded and any item below safety margin has a scaling action queued.

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Prepare

Achieve the 'prepare' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Execute

Achieve the 'execute' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Verify

Achieve the 'verify' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Document

Achieve the 'document' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Decide

Achieve the 'decide' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/pro/infra/devops-engineer/finops-devops-cost-rightsizing`
- `knowledge/pro/infra/devops-engineer/prometheus-monitoring`
- `knowledge/pro/infra/infrastructure-engineer/aws-monitoring-observability`
- `knowledge/pro/infra/infrastructure-engineer/cloud-run-autoscaling`
- `knowledge/pro/infra/infrastructure-engineer/gce-autoscaling`
- `knowledge/pro/infra/infrastructure-engineer/k8s-limitrange`
- `knowledge/pro/infra/infrastructure-engineer/k8s-resource-quota`
- `knowledge/pro/infra/infrastructure-engineer/k8s-scaling-availability`
