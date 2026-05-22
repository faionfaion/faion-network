---
slug: cron-scheduled-job-audit-monthly
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: All cron and scheduled jobs (k8s CronJob, GHA scheduled, Airflow / cloud scheduler) are inventoried; orphan / failing / silently-skipping jobs are flagged and assigned owners.
content_id: fa2618c857e867b2
methodology_refs:
  - api-monitoring-alerting
  - cloud-run-jobs
  - k8s-deployment-workloads
  - cron-automation
---

# Cron / scheduled-job audit (monthly)

**Slug:** `cron-scheduled-job-audit-monthly` · **Tier:** pro · **Complexity:** light

## Context

All cron and scheduled jobs (k8s CronJob, GHA scheduled, Airflow / cloud scheduler) are inventoried; orphan / failing / silently-skipping jobs are flagged and assigned owners.

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

- `knowledge/pro/dev/software-developer/api-monitoring-alerting`
- `knowledge/pro/infra/infrastructure-engineer/cloud-run-jobs`
- `knowledge/pro/infra/infrastructure-engineer/k8s-deployment-workloads`
- `knowledge/solo/infra/server-craft/cron-automation`
