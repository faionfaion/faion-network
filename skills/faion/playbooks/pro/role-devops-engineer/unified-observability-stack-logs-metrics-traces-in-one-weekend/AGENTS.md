---
slug: unified-observability-stack-logs-metrics-traces-in-one-weekend
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: build-ship
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Greenfield obs stack chosen, deployed, and instrumented for one reference service; cardinality/cost guardrails set; team can answer 'what broke and where' from a single Grafana entry point."
content_id: 83218688cd4ad546
methodology_refs:
  - microservices-observability
  - devops-elk-architecture
  - grafana-dashboards
  - cardinality-and-cost-guardrails
  - observability-stack-decision-matrix
  - opentelemetry-collector-architecture
  - opentelemetry-instrumentation-playbook
  - trace-sampling-tail-vs-head
---

# Unified observability stack (logs + metrics + traces) in one weekend

**Slug:** `unified-observability-stack-logs-metrics-traces-in-one-weekend` · **Tier:** pro · **Complexity:** deep

## Context

Greenfield obs stack chosen, deployed, and instrumented for one reference service; cardinality/cost guardrails set; team can answer 'what broke and where' from a single Grafana entry point.

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

- `knowledge/pro/dev/software-developer/microservices-observability`
- `knowledge/pro/infra/devops-engineer/devops-elk-architecture`
- `knowledge/pro/infra/devops-engineer/grafana-dashboards`
