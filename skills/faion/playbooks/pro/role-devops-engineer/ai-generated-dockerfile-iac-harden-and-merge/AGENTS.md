---
slug: ai-generated-dockerfile-iac-harden-and-merge
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
summary: An AI-authored Dockerfile, GHA workflow, or Terraform module passes hardening review (non-root user, pinned digests, no secrets in env, healthcheck, minimal layers) before it enters main.
content_id: d3c742525b17e8ca
methodology_refs:
  - lint-shellcheck-hadolint-iac-floor
  - mr-graph-vs-diff-reviewer
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - docker-optimization
  - gha-deployment-patterns
  - security-container-scanning
  - security-supply-chain
  - docker
  - docker-image-optimization
  - docker-language-templates
  - docker-security-hardening
---

# AI-generated Dockerfile / IaC harden-and-merge

**Slug:** `ai-generated-dockerfile-iac-harden-and-merge` · **Tier:** pro · **Complexity:** medium

## Context

An AI-authored Dockerfile, GHA workflow, or Terraform module passes hardening review (non-root user, pinned digests, no secrets in env, healthcheck, minimal layers) before it enters main.

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

- `knowledge/geek/sdlc-ai/lint-shellcheck-hadolint-iac-floor`
- `knowledge/geek/sdlc-ai/mr-graph-vs-diff-reviewer`
- `knowledge/geek/sdlc-ai/sec-secrets-defense-in-depth`
- `knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `knowledge/pro/infra/cicd-engineer/docker-optimization`
- `knowledge/pro/infra/cicd-engineer/gha-deployment-patterns`
- `knowledge/pro/infra/cicd-engineer/security-container-scanning`
- `knowledge/pro/infra/cicd-engineer/security-supply-chain`
