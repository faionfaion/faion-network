# Canary deploy promote/rollback decision

**Slug:** `canary-deploy-promoterollback-decision` · **Tier:** pro · **Complexity:** medium

## Context

Within an active canary window, the operator has a defensible decision (promote / hold / rollback) based on SLO burn, error-rate delta, and latency p99 against control, and the decision is logged.

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

- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/dev/software-architect/observability-architecture`
- `knowledge/pro/dev/software-developer/api-monitoring-alerting`
- `knowledge/pro/dev/software-developer/api-monitoring-metrics`
- `knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery`
- `knowledge/pro/infra/devops-engineer/dora-metrics`
- `knowledge/pro/infra/infrastructure-engineer/k8s-canary-progressive`
