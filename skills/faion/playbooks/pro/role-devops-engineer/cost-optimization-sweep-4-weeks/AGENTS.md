---
slug: cost-optimization-sweep-4-weeks
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: optimize-tune
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Cloud bill cut by a measurable target (e.
content_id: 3e549983a9e92689
methodology_refs:
  - fco-commitment-pricing
  - fco-cost-allocation
  - fco-rightsizing
  - fco-spot-instances
  - fco-waste-elimination
  - finops-agentic-workflow
  - finops-ai-ml-costs
  - finops-cost-visibility
  - finops-framework
  - finops-governance
  - devops-platform-policy-finops
  - finops
  - finops-devops-cost-alerts
  - finops-devops-cost-commitments
  - finops-devops-cost-kubernetes
  - finops-devops-cost-rightsizing
  - finops-devops-cost-tagging
  - aws-cost-optimization
  - cloud-run-autoscaling
  - gce-autoscaling
  - gce-spot-vms
  - gcp-billing-cost
  - k8s-resource-requests-limits
---

# Cost optimization sweep (4 weeks)

**Slug:** `cost-optimization-sweep-4-weeks` · **Tier:** pro · **Complexity:** deep

## Context

Cloud bill cut by a measurable target (e.g. 25%) without breaking SLOs: rightsize compute, kill waste, adopt commitments / spot where safe, install cost guardrails. Exit: monthly run-rate down vs. baseline, FinOps dashboards live, cost alerts wired.

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Plan & frame

Achieve the 'plan & frame' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Inventory & baseline

Achieve the 'inventory & baseline' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Design choices

Achieve the 'design choices' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Pilot / dry-run

Achieve the 'pilot / dry-run' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Roll-out

Achieve the 'roll-out' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 6: Verify & measure

Achieve the 'verify & measure' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 7: Document & handoff

Achieve the 'document & handoff' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 8: Decide / lock-in

Achieve the 'decide / lock-in' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/pro/infra/cicd-engineer/fco-commitment-pricing`
- `knowledge/pro/infra/cicd-engineer/fco-cost-allocation`
- `knowledge/pro/infra/cicd-engineer/fco-rightsizing`
- `knowledge/pro/infra/cicd-engineer/fco-spot-instances`
- `knowledge/pro/infra/cicd-engineer/fco-waste-elimination`
- `knowledge/pro/infra/cicd-engineer/finops-agentic-workflow`
- `knowledge/pro/infra/cicd-engineer/finops-ai-ml-costs`
- `knowledge/pro/infra/cicd-engineer/finops-cost-visibility`
