---
slug: architecture-review-meeting-facilitation
tier: pro
group: role-software-architect
persona: role-software-architect
goal: TBD
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Run an ATAM-lite review of a proposed design with stakeholders, exiting with sensitivity points, risks, and trade-offs documented as ADRs.
content_id: 562411241b2982ea
methodology_refs:
  - quality-attributes-analysis
  - architecture-decision-records
  - c4-model
  - trade-off-decision-methods
  - trade-off-quality-attributes
  - trade-off-stakeholder-communication
---

# Architecture review meeting facilitation

**Slug:** `architecture-review-meeting-facilitation` · **Tier:** pro · **Complexity:** light

## Context

Run an ATAM-lite review of a proposed design with stakeholders, exiting with sensitivity points, risks, and trade-offs documented as ADRs

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

- `knowledge/pro/dev/software-architect/quality-attributes-analysis`
- `knowledge/solo/dev/software-architect/architecture-decision-records`
- `knowledge/solo/dev/software-architect/c4-model`
- `knowledge/solo/dev/software-architect/trade-off-decision-methods`
- `knowledge/solo/dev/software-architect/trade-off-quality-attributes`
- `knowledge/solo/dev/software-architect/trade-off-stakeholder-communication`
