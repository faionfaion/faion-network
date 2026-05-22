---
slug: greenfield-infra-bootstrap-k8s-cicd-observability-secrets-4-weeks
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
summary: "Day-0 production platform stood up for a new product line: VPC + k8s cluster, GitOps-driven CI/CD, baseline observability (logs/metrics), centralized secrets, on-call rotation in place."
content_id: 90bd80cd4122e5dd
methodology_refs:
  - inc-read-only-investigation-default
  - inc-runbook-as-markdown-tagged-steps
  - argocd-gitops
  - dora-metrics
  - elk-stack-logging
  - gha-caching-artifacts
  - gha-deployment-patterns
  - gha-security-hardening
  - gha-workflow-structure
  - gitops-core-principles
  - gitops-progressive-delivery
  - gitops-repository-structure
  - gitops-secrets-security
  - grafana-basics
  - grafana-setup
  - lb-kubernetes-ingress
  - lb-technology-selection
  - prometheus-monitoring
  - secrets-management
  - security-container-scanning
  - security-policy-as-code
  - security-sast
  - security-supply-chain
  - devops-aws-three-tier
  - devops-elk-architecture
  - devops-elk-beats-collection
  - devops-platform-backstage
  - devops-platform-golden-paths
  - devops-platform-idp-core
  - grafana-dashboards
  - security-as-code
  - aws-architecture-services
  - aws-monitoring-observability
  - aws-multi-account-landing-zone
  - aws-vpc-design
  - aws-vpc-three-tier
  - aws-well-architected-framework
  - gcp-landing-zone
  - gcp-networking-vpc
  - iac-basics
  - iac-patterns-cicd
  - k8s-basics
  - k8s-canary-progressive
  - k8s-deployment-workloads
  - k8s-resource-quota
  - k8s-rolling-update
  - k8s-scaling-availability
  - k8s-security-hardening
  - terraform-basics
  - terraform-modules-composition
  - terraform-modules-structure
  - terraform-state
---

# Greenfield infra bootstrap: k8s + CI/CD + observability + secrets (4 weeks)

**Slug:** `greenfield-infra-bootstrap-k8s-cicd-observability-secrets-4-weeks` · **Tier:** pro · **Complexity:** deep

## Context

Day-0 production platform stood up for a new product line: VPC + k8s cluster, GitOps-driven CI/CD, baseline observability (logs/metrics), centralized secrets, on-call rotation in place. Exit: first service deployed via the platform, alerts firing to a real channel, runbook drafted.

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

- `knowledge/geek/sdlc-ai/inc-read-only-investigation-default`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/pro/infra/cicd-engineer/argocd-gitops`
- `knowledge/pro/infra/cicd-engineer/dora-metrics`
- `knowledge/pro/infra/cicd-engineer/elk-stack-logging`
- `knowledge/pro/infra/cicd-engineer/gha-caching-artifacts`
- `knowledge/pro/infra/cicd-engineer/gha-deployment-patterns`
- `knowledge/pro/infra/cicd-engineer/gha-security-hardening`
