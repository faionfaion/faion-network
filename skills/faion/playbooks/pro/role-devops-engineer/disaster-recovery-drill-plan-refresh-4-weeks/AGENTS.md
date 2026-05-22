---
slug: disaster-recovery-drill-plan-refresh-4-weeks
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
summary: "Real (not paper) DR exercise: pick scenarios, drill recovery against backups + IaC, measure actual RTO/RPO, fix gaps, publish refreshed plan."
content_id: 545b6b924cc2e855
methodology_refs:
  - inc-postmortem-auto-draft-no-publish
  - inc-read-only-investigation-default
  - inc-runbook-as-markdown-tagged-steps
  - inc-tool-tier-approval-gate
  - backup-cloud-aws
  - backup-database-mysql-mongo
  - backup-database-postgres
  - backup-filesystem-restic
  - backup-kubernetes-velero
  - backup-verification-dr
  - backup-strategies
  - devops-aws-monitoring-dr
  - devops-platform-golden-paths
  - iac-patterns-testing
  - terraform-state
---

# Disaster-recovery drill + plan refresh (4 weeks)

**Slug:** `disaster-recovery-drill-plan-refresh-4-weeks` · **Tier:** pro · **Complexity:** medium

## Context

Real (not paper) DR exercise: pick scenarios, drill recovery against backups + IaC, measure actual RTO/RPO, fix gaps, publish refreshed plan. Exit: passing drill report, updated DR plan, scheduled cadence.

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

- `knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `knowledge/geek/sdlc-ai/inc-read-only-investigation-default`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/geek/sdlc-ai/inc-tool-tier-approval-gate`
- `knowledge/pro/infra/cicd-engineer/backup-cloud-aws`
- `knowledge/pro/infra/cicd-engineer/backup-database-mysql-mongo`
- `knowledge/pro/infra/cicd-engineer/backup-database-postgres`
- `knowledge/pro/infra/cicd-engineer/backup-filesystem-restic`
