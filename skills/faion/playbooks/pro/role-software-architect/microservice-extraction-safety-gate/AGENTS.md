---
slug: microservice-extraction-safety-gate
tier: pro
group: role-software-architect
persona: role-software-architect
goal: TBD
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Decide whether to extract a service from a modular monolith, with reversibility + bulkhead criteria, BEFORE writing the extraction PR.
content_id: 2f490a677bd417d6
methodology_refs:
  - domain-driven-design
  - distributed-patterns
  - event-driven-architecture
  - microservices-architecture
  - reliability-architecture
  - modular-monolith
---

# Microservice extraction safety gate

**Slug:** `microservice-extraction-safety-gate` · **Tier:** pro · **Complexity:** medium

## Context

Decide whether to extract a service from a modular monolith, with reversibility + bulkhead criteria, BEFORE writing the extraction PR

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

- `knowledge/pro/dev/code-quality/domain-driven-design`
- `knowledge/pro/dev/software-architect/distributed-patterns`
- `knowledge/pro/dev/software-architect/event-driven-architecture`
- `knowledge/pro/dev/software-architect/microservices-architecture`
- `knowledge/pro/dev/software-architect/reliability-architecture`
- `knowledge/solo/dev/software-architect/modular-monolith`
