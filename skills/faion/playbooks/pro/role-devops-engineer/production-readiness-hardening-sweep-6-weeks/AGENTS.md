---
slug: production-readiness-hardening-sweep-6-weeks
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
summary: "Pre-existing system promoted from staging-quality to true production: SLOs defined, alerts deduped, secrets rotated, backups verified, security gates blocking, capacity headroom proven, runbooks pu..."
content_id: c9383b9cdd42ad37
methodology_refs:
  - gov-conventional-commits-enforced
  - inc-postmortem-auto-draft-no-publish
  - inc-read-only-investigation-default
  - inc-runbook-as-markdown-tagged-steps
  - inc-tool-tier-approval-gate
  - sec-codeql-autofix-on-pr
  - sec-secrets-defense-in-depth
  - sec-trivy-pinned-supply-chain-scan
  - task-plan-mode-locked-execution
  - backup-basics
  - backup-cloud-aws
  - backup-database-mysql-mongo
  - backup-database-postgres
  - backup-filesystem-restic
  - backup-kubernetes-velero
  - backup-verification-dr
  - dora-metrics
  - lb-health-checks
  - lb-high-availability
  - prometheus-monitoring
  - secrets-management
  - security-container-scanning
  - security-dast
  - security-sast
  - security-supply-chain
  - aws-well-architected-checklists
  - backup-strategies
  - devops-elk-queries-alerting
  - docker-security-hardening
  - grafana-dashboards
  - aws-well-architected-framework
  - k8s-canary-progressive
  - k8s-limitrange
  - k8s-resource-quota
  - k8s-resource-requests-limits
  - k8s-scaling-availability
  - k8s-security-hardening
---

# Production-readiness hardening sweep (6 weeks)

**Slug:** `production-readiness-hardening-sweep-6-weeks` · **Tier:** pro · **Complexity:** deep

## Context

Pre-existing system promoted from staging-quality to true production: SLOs defined, alerts deduped, secrets rotated, backups verified, security gates blocking, capacity headroom proven, runbooks published. Exit: a documented production-readiness review (PRR) passes with no Sev-1 open items.

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
- `knowledge/geek/sdlc-ai/inc-postmortem-auto-draft-no-publish`
- `knowledge/geek/sdlc-ai/inc-read-only-investigation-default`
- `knowledge/geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps`
- `knowledge/geek/sdlc-ai/inc-tool-tier-approval-gate`
- `knowledge/geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `knowledge/geek/sdlc-ai/sec-secrets-defense-in-depth`
- `knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
