---
slug: post-incident-retro-facilitation
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: For each P0/P1 in the past week, a written retro is published with timeline, contributing factors, action items with owners, and learnings filed into the runbook system.
content_id: 4e0829c413cc2a49
methodology_refs:
  - inc-postmortem-auto-draft-no-publish
  - inc-read-only-investigation-default
  - inc-runbook-as-markdown-tagged-steps
  - api-monitoring-health-checks
  - microservices-observability
  - dora-metrics
---

# Post-incident retro facilitation

**Slug:** `post-incident-retro-facilitation` · **Tier:** pro · **Complexity:** medium

## Context

For each P0/P1 in the past week, a written retro is published with timeline, contributing factors, action items with owners, and learnings filed into the runbook system.

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
- `knowledge/pro/dev/software-developer/api-monitoring-health-checks`
- `knowledge/pro/dev/software-developer/microservices-observability`
- `knowledge/pro/infra/devops-engineer/dora-metrics`
