---
slug: weekly-cloud-cost-review
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
summary: Last 7 days of cloud spend reviewed against budget by service / team; top three anomalies have owners + actions; rightsizing candidates queued.
content_id: 542aed04c9b8edd3
methodology_refs:
  - fco-commitment-pricing
  - fco-rightsizing
  - fco-waste-elimination
  - finops-cost-visibility
  - finops-framework
  - finops-governance
  - devops-platform-policy-finops
  - finops-devops-cost-alerts
  - finops-devops-cost-kubernetes
  - finops-devops-cost-rightsizing
  - finops-devops-cost-tagging
  - aws-cost-optimization
---

# Weekly cloud cost review

**Slug:** `weekly-cloud-cost-review` · **Tier:** pro · **Complexity:** light

## Context

Last 7 days of cloud spend reviewed against budget by service / team; top three anomalies have owners + actions; rightsizing candidates queued.

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

- `knowledge/pro/infra/cicd-engineer/fco-commitment-pricing`
- `knowledge/pro/infra/cicd-engineer/fco-rightsizing`
- `knowledge/pro/infra/cicd-engineer/fco-waste-elimination`
- `knowledge/pro/infra/cicd-engineer/finops-cost-visibility`
- `knowledge/pro/infra/cicd-engineer/finops-framework`
- `knowledge/pro/infra/cicd-engineer/finops-governance`
- `knowledge/pro/infra/devops-engineer/devops-platform-policy-finops`
- `knowledge/pro/infra/devops-engineer/finops-devops-cost-alerts`
