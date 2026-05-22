---
slug: architecture-fitness-function-check-weekly
tier: geek
group: role-software-architect
persona: role-software-architect
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Done = the codified fitness functions (perf budget, layering rules, dependency direction, error-budget burn) are run; any newly red signal has an owner and a fix-or-relax decision logged.
content_id: 7747009de1630e9b
methodology_refs:
  - quality-attributes-analysis
  - architecture-decision-records
  - performance-architecture
  - trade-off-decision-methods
  - trade-off-stakeholder-communication
  - living-documentation
---

# Architecture fitness-function check (weekly)

**Slug:** `architecture-fitness-function-check-weekly` · **Tier:** geek · **Complexity:** medium

## Context

Done = the codified fitness functions (perf budget, layering rules, dependency direction, error-budget burn) are run; any newly red signal has an owner and a fix-or-relax decision logged.

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

- `knowledge/pro/dev/software-architect/quality-attributes-analysis`
- `knowledge/solo/dev/software-architect/architecture-decision-records`
- `knowledge/solo/dev/software-architect/performance-architecture`
- `knowledge/solo/dev/software-architect/trade-off-decision-methods`
- `knowledge/solo/dev/software-architect/trade-off-stakeholder-communication`
- `knowledge/solo/sdd/sdd/living-documentation`
