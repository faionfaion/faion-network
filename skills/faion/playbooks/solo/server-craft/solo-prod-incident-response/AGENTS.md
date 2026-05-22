---
slug: solo-prod-incident-response
tier: solo
group: server-craft
persona: P1
goal: fix-incident
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Alert at 3am → root-caused, mitigated, postmortem-documented incident for one person without SRE rotation.
content_id: b450ea4deff8240a
methodology_refs:
  - monitoring-logging
  - health-checks-autoheal
  - cd-pipelines
  - feature-flags-rollout-targeting
  - mistake-memory
  - reflexion-learning
---

# Solo prod incident response (no team safety net)

**Playbook slug:** `solo-prod-incident-response`  
**Tier:** solo  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

Alert at 3am → root-caused, mitigated, postmortem-documented incident for one person without SRE rotation.

## Scope

Solo founder runs incident response designed for one person: alert to mitigation to postmortem, without an SRE rotation. Exit artifact is a green prod + blameless postmortem + followup backlog entry.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-team incident command — single operator only
- PR / public status comms — separate stakeholder-communication playbook

### Prerequisites

- Monitoring + alerting configured (monitoring-logging complete)
- Sentry / equivalent error tracking live
- Deploy + rollback path proven (deploy-day playbook done)

## Success criteria

The playbook is done when:
- Alert acknowledged within 5 minutes
- Stop-the-bleed action shipped (rollback or flag-off)
- Root cause identified and documented
- Postmortem written within 48h
- Followup action added to backlog

## Stages

### Stage 1: Triage

**Intent:** Acknowledge, scope impact, decide stop-the-bleed action.

**Tasks:**
- Acknowledge alert
- Open incident channel / note
- Decide: rollback / flag-off / patch

**Methodologies in chain:**
- `monitoring-logging` → `solo/infra/server-craft/monitoring-logging`
- `health-checks-autoheal` → `solo/infra/server-craft/health-checks-autoheal`

**Outputs:**
- Triage note with decision

**Decision gate:**
> Advance when stop-the-bleed action is chosen. Refuse to investigate before bleeding stops.

### Stage 2: Mitigate

**Intent:** Stop the bleed. Diagnosis comes later.

**Tasks:**
- Execute rollback / flag-off / hot-patch
- Verify mitigation via health checks
- Communicate ETA to customers if needed

**Methodologies in chain:**
- `cd-pipelines` → `solo/dev/automation-tooling/cd-pipelines`
- `feature-flags-rollout-targeting` → `solo/dev/automation-tooling/feature-flags-rollout-targeting`

**Outputs:**
- Mitigated prod

**Decision gate:**
> Advance when monitoring is green again. Stay if mitigation incomplete.

### Stage 3: Investigate

**Intent:** Find root cause. Don't guess.

**Tasks:**
- Pull logs around incident window
- Identify trigger + contributing factors
- Document timeline

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- Root-cause notes

**Decision gate:**
> Advance when root cause is named. Refuse to write postmortem with 'cause unknown'.

### Stage 4: Postmortem

**Intent:** Blameless. What happened, why, what changes.

**Tasks:**
- Write blameless postmortem
- List followup actions
- Update mistake-memory

**Methodologies in chain:**
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Outputs:**
- Postmortem doc
- Mistake-memory entry

**Decision gate:**
> Required output: postmortem within 48h. Without it, the same incident recurs.

## Common pitfalls

- Investigating before mitigating — extends bleeding for diagnosis purity
- Skipping postmortem because incident felt small — small ones recur fastest

## Quality checklist (self-review)

- If I get paged for the same root cause next month, will I find this postmortem?
- Is the followup actually in the backlog, or only mentioned in the postmortem?

## Related playbooks

- `deploy-day-staging-to-prod`
- `pre-launch-hardening-mvp`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-alerting-noise-budget** (tier `solo`, blocks stage 1) — Triage stage needs noise budget so alerts at 3am are signal
- **sentry-supabase-vercel-wiring** (tier `solo`, blocks stage 1) — Triage stage needs concrete wiring for solo-popular stack
- **solo-incident-triage-checklist** (tier `solo`, blocks stage 1) — Triage stage needs checklist tailored to single operator
- **stop-the-bleed-playbook** (tier `solo`, blocks stage 2) — Mitigate stage needs decision tree for rollback/flag/patch
- **solo-blameless-postmortem-template** (tier `solo`, blocks stage 4) — Postmortem stage needs blameless template scoped to one author
- **incident-followup-backlog-policy** (tier `solo`, blocks stage 4) — Postmortem stage needs policy on what becomes backlog vs accepted risk

## CLI usage

```
faion get-content solo-prod-incident-response --format md       # human-readable rendering
faion get-content solo-prod-incident-response --format context  # agent-optimised context bundle
faion get-content solo-prod-incident-response --format json     # raw structured form
```
