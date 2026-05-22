---
slug: design-slos-error-budgets-before-first-deploy
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: A team has a service ready to ship; output is a documented SLI/SLO sheet, error-budget policy, burn-rate alert rules wired into Prometheus/Grafana, and a runbook link per alert.
content_id: a0a39f048dceccf2
methodology_refs:
  - inc-runbook-as-markdown-tagged-steps
  - observability-architecture
  - grafana-dashboards
  - prometheus-monitoring
  - burn-rate-multi-window-alerting
  - error-budget-policy-and-freeze-rules
  - slo-design-from-user-journeys
  - slo-quarterly-review-cadence
---

# Design SLOs + error budgets before first deploy

**Slug:** `design-slos-error-budgets-before-first-deploy` · **Tier:** pro · **Complexity:** deep

## Context

A team has a service ready to ship; output is a documented SLI/SLO sheet, error-budget policy, burn-rate alert rules wired into Prometheus/Grafana, and a runbook link per alert.

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

- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/dev/software-architect/observability-architecture`
- `knowledge/pro/infra/devops-engineer/grafana-dashboards`
- `knowledge/pro/infra/devops-engineer/prometheus-monitoring`
