---
slug: kubernetes-major-version-upgrade-3-weeks
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
summary: "Move one or more clusters one minor (or major) version forward with zero customer-facing downtime: addons compatible, deprecated APIs removed, node images refreshed, rollback path proven."
content_id: ef79d6ef540fd5bc
methodology_refs:
  - inc-postmortem-auto-draft-no-publish
  - inc-runbook-as-markdown-tagged-steps
  - argocd-gitops
  - gitops-progressive-delivery
  - lb-kubernetes-ingress
  - prometheus-monitoring
  - devops-platform-golden-paths
  - helm-charts
  - helm-advanced
  - helm-basics
  - k8s-basics
  - k8s-canary-progressive
  - k8s-deployment-workloads
  - k8s-rolling-update
  - k8s-scaling-availability
---

# Kubernetes major-version upgrade (3 weeks)

**Slug:** `kubernetes-major-version-upgrade-3-weeks` · **Tier:** pro · **Complexity:** deep

## Context

Move one or more clusters one minor (or major) version forward with zero customer-facing downtime: addons compatible, deprecated APIs removed, node images refreshed, rollback path proven. Exit: control plane + node pools on target version, smoke tests pass, deprecation backlog empty.

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

- `knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/infra/cicd-engineer/argocd-gitops`
- `knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery`
- `knowledge/pro/infra/cicd-engineer/lb-kubernetes-ingress`
- `knowledge/pro/infra/cicd-engineer/prometheus-monitoring`
- `knowledge/pro/infra/devops-engineer/devops-platform-golden-paths`
- `knowledge/pro/infra/devops-engineer/helm-charts`
