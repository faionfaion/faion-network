---
slug: helm-chart-bump-for-new-release
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
summary: A service is shipped from a vetted image tag to staging then production via Helm with values diff reviewed, image SBOM verified, and rollback command pre-staged.
content_id: 1eb87d9baed2d4c3
methodology_refs:
  - sec-trivy-pinned-supply-chain-scan
  - gitops-progressive-delivery
  - argocd-gitops
  - helm-charts
  - helm-advanced
  - helm-basics
  - k8s-canary-progressive
  - k8s-deployment-workloads
  - k8s-resource-requests-limits
  - k8s-rolling-update
---

# Helm chart bump for new release

**Slug:** `helm-chart-bump-for-new-release` · **Tier:** pro · **Complexity:** medium

## Context

A service is shipped from a vetted image tag to staging then production via Helm with values diff reviewed, image SBOM verified, and rollback command pre-staged.

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

- `knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `knowledge/pro/infra/cicd-engineer/gitops-progressive-delivery`
- `knowledge/pro/infra/devops-engineer/argocd-gitops`
- `knowledge/pro/infra/devops-engineer/helm-charts`
- `knowledge/pro/infra/infrastructure-engineer/helm-advanced`
- `knowledge/pro/infra/infrastructure-engineer/helm-basics`
- `knowledge/pro/infra/infrastructure-engineer/k8s-canary-progressive`
- `knowledge/pro/infra/infrastructure-engineer/k8s-deployment-workloads`
