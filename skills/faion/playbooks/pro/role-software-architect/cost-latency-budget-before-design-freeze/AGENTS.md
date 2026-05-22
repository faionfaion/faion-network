---
slug: cost-latency-budget-before-design-freeze
tier: pro
group: role-software-architect
persona: role-software-architect
goal: plan-design
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Architect produces a per-component cost-per-1M-requests and p95 latency budget that gates the design review.
content_id: b076881476e19478
methodology_refs:
  - observability-architecture
  - quality-attributes-analysis
  - reliability-architecture
  - architecture-decision-records
  - decision-tree-build-vs-buy
  - performance-architecture
  - serverless-cost-optimization
  - trade-off-build-vs-buy
---

# Cost + latency budget BEFORE design freeze

**Slug:** `cost-latency-budget-before-design-freeze` · **Tier:** pro · **Complexity:** deep

## Context

Architect produces a per-component cost-per-1M-requests and p95 latency budget that gates the design review

## Outcome

The playbook is done when each stage below has produced its artifact, the decision gate has been passed in writing, and the operator can show a teammate a clean evidence trail across the entire chain.

## Steps

### Step 1: Plan & frame

Achieve the 'plan & frame' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 2: Inventory & baseline

Achieve the 'inventory & baseline' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 3: Design choices

Achieve the 'design choices' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 4: Pilot / dry-run

Achieve the 'pilot / dry-run' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 5: Roll-out

Achieve the 'roll-out' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 6: Verify & measure

Achieve the 'verify & measure' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 7: Document & handoff

Achieve the 'document & handoff' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

### Step 8: Decide / lock-in

Achieve the 'decide / lock-in' outcome by working through the tasks listed in `playbook.yaml`. Capture the named outputs and resolve open questions before moving on.

## Decision points

Each stage in `playbook.yaml` carries an explicit `decision_gate`. Treat them as hard exits — do not advance on vibes. The two highest-stakes gates in this playbook:

- **Entry gate** — confirm prerequisites are real, not assumed. If a prerequisite is missing, stop and resolve it before starting Step 1.
- **Final gate** — the playbook closes with a written decision artifact. No 'see how it goes'.

## References

- `knowledge/pro/dev/software-architect/observability-architecture`
- `knowledge/pro/dev/software-architect/quality-attributes-analysis`
- `knowledge/pro/dev/software-architect/reliability-architecture`
- `knowledge/solo/dev/software-architect/architecture-decision-records`
- `knowledge/solo/dev/software-architect/decision-tree-build-vs-buy`
- `knowledge/solo/dev/software-architect/performance-architecture`
- `knowledge/solo/dev/software-architect/serverless-cost-optimization`
- `knowledge/solo/dev/software-architect/trade-off-build-vs-buy`
