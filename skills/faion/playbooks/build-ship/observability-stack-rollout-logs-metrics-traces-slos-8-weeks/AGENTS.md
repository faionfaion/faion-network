# Observability stack rollout: logs + metrics + traces + SLOs (8 weeks)

**Slug:** `observability-stack-rollout-logs-metrics-traces-slos-8-weeks` · **Tier:** pro · **Complexity:** deep

## Context

Greenfield or replacement observability platform delivered end-to-end across the org: structured logging, metrics, distributed traces, dashboards-as-code, SLOs with error budgets, sane alert routing. Exit: every prod service emits the three signals, each owns at least one SLO, MTTR drops vs. baseline.

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

- `knowledge/geek/sdlc-ai/gov-conventional-commits-enforced`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/geek/sdlc-ai/inc-tool-tier-approval-gate`
- `knowledge/pro/infra/cicd-engineer/dora-metrics`
- `knowledge/pro/infra/cicd-engineer/elk-stack-logging`
- `knowledge/pro/infra/cicd-engineer/grafana-basics`
- `knowledge/pro/infra/cicd-engineer/grafana-setup`
- `knowledge/pro/infra/cicd-engineer/lb-monitoring`
