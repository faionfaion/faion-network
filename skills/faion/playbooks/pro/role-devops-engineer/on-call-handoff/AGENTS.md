---
slug: on-call-handoff
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
summary: Outgoing on-call has zeroed the alert inbox, documented open incidents + watch-items, and walked the incoming on-call through the queue.
content_id: c11b04b17bdf0492
methodology_refs:
  - inc-postmortem-auto-draft-no-publish
  - inc-runbook-as-markdown-tagged-steps
  - observability-architecture
  - api-monitoring-alerting
  - devops-elk-queries-alerting
---

# On-call handoff

**Slug:** `on-call-handoff` · **Tier:** pro · **Complexity:** light

## Context

Outgoing on-call has zeroed the alert inbox, documented open incidents + watch-items, and walked the incoming on-call through the queue. Handoff doc is in shared location and acknowledged.

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

- `knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/dev/software-architect/observability-architecture`
- `knowledge/pro/dev/software-developer/api-monitoring-alerting`
- `knowledge/pro/infra/devops-engineer/devops-elk-queries-alerting`
