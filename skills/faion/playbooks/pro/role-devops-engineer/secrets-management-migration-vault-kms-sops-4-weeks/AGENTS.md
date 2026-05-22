---
slug: secrets-management-migration-vault-kms-sops-4-weeks
tier: pro
group: role-devops-engineer
persona: role-devops-engineer
goal: migrate-rebuild
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: All long-lived secrets moved off ad-hoc storage (env files, plaintext k8s Secrets, Jenkins creds) onto a centralized backend with short-lived tokens, rotation policy, audit trail, and CI/CD wiring.
content_id: 018a0b8972e27825
methodology_refs:
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - cicd-cert-rotation-pipeline
  - cicd-mtls-deployment
  - cicd-tls-renewal-automation
  - cicd-tls-validation-gate
  - gha-security-hardening
  - gitlab-cicd
  - gitops-secrets-security
  - secrets-management
  - security-policy-as-code
  - security-supply-chain
  - github-actions-cicd
  - security-as-code
  - aws-iam-practical-patterns
  - aws-iam-security-foundations
  - gcp-iam-design
  - gcp-security-iam
  - k8s-security-hardening
---

# Secrets-management migration: Vault / KMS / SOPS (4 weeks)

**Slug:** `secrets-management-migration-vault-kms-sops-4-weeks` · **Tier:** pro · **Complexity:** deep

## Context

All long-lived secrets moved off ad-hoc storage (env files, plaintext k8s Secrets, Jenkins creds) onto a centralized backend with short-lived tokens, rotation policy, audit trail, and CI/CD wiring. Exit: zero secrets in repos, leaked-secret scan green, rotation drill passes.

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

- `knowledge/geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `knowledge/geek/sdlc-ai/sec-secrets-defense-in-depth`
- `knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `knowledge/pro/infra/cicd-engineer/cicd-cert-rotation-pipeline`
- `knowledge/pro/infra/cicd-engineer/cicd-mtls-deployment`
- `knowledge/pro/infra/cicd-engineer/cicd-tls-renewal-automation`
- `knowledge/pro/infra/cicd-engineer/cicd-tls-validation-gate`
- `knowledge/pro/infra/cicd-engineer/gha-security-hardening`
