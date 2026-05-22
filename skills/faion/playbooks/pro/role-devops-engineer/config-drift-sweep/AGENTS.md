---
slug: config-drift-sweep
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Across IaC-managed resources, `terraform plan` (or equivalent) returns clean or every drift item has a documented reason + remediation path."
content_id: fa1eeac1cbbca869
methodology_refs:
  - security-policy-as-code
  - argocd-gitops
  - gitops
  - security-as-code
  - terraform
  - terraform-iac
  - iac-patterns-testing
  - terraform-state
---

# Config drift sweep

**Slug:** `config-drift-sweep` · **Tier:** pro · **Complexity:** medium

## Context

Across IaC-managed resources, `terraform plan` (or equivalent) returns clean or every drift item has a documented reason + remediation path.

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Prepare

Achieve the 'prepare' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Inventory

Achieve the 'inventory' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Decide approach

Achieve the 'decide approach' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Execute

Achieve the 'execute' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Verify

Achieve the 'verify' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 6: Document & decide

Achieve the 'document & decide' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/pro/infra/cicd-engineer/security-policy-as-code`
- `knowledge/pro/infra/devops-engineer/argocd-gitops`
- `knowledge/pro/infra/devops-engineer/gitops`
- `knowledge/pro/infra/devops-engineer/security-as-code`
- `knowledge/pro/infra/devops-engineer/terraform`
- `knowledge/pro/infra/devops-engineer/terraform-iac`
- `knowledge/pro/infra/infrastructure-engineer/iac-patterns-testing`
- `knowledge/pro/infra/infrastructure-engineer/terraform-state`
