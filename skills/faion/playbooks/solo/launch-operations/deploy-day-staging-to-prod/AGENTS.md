---
slug: deploy-day-staging-to-prod
tier: solo
group: launch-operations
persona: P1
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Feature lives on staging → safe push to prod with rollback ready and post-deploy verified.
content_id: 7a2cb4009bfc5c46
methodology_refs:
  - e2e-testing
  - cd-basics
  - cd-pipelines
  - quality-gates-confidence
  - feature-flags-rollout-targeting
  - feature-flags
  - deploy-scripts
  - release-planning
  - health-checks-autoheal
  - monitoring-logging
  - logging-patterns
---

# Deploy-day staging-to-prod gate

**Playbook slug:** `deploy-day-staging-to-prod`  
**Tier:** solo  
**Complexity:** medium  
**Persona:** P1 — Solo SaaS Builder

## Intent

Feature lives on staging → safe push to prod with rollback ready and post-deploy verified.

## Scope

Solo founder pushes to prod safely: CI green, smoke pass on staging, feature-flagged where risky, deploy script run, post-deploy health verified, rollback path proven. Exit artifact is healthy prod + verified rollback path.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- Multi-region deployments — single-region only here
- Blue-green orchestration — flag-based rollouts only

### Prerequisites

- CI pipeline configured (cd-basics complete)
- Staging environment live
- Monitoring + logging configured

## Success criteria

The playbook is done when:
- CI green on PR + main
- Staging smoke test passed
- Feature behind flag if risky
- Deploy executed via script (not manual)
- Post-deploy health checks pass within 5 minutes
- Rollback path tested in staging

## Stages

### Stage 1: Pre-flight

**Intent:** CI green + staging smoke + flag plan confirmed.

**Tasks:**
- Verify CI green on main
- Run staging smoke test
- Confirm feature flag plan

**Methodologies in chain:**
- `e2e-testing` → `free/dev/testing-developer/e2e-testing`
- `cd-basics` → `solo/dev/automation-tooling/cd-basics`
- `cd-pipelines` → `solo/dev/automation-tooling/cd-pipelines`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`

**Outputs:**
- Pre-flight checklist complete

**Decision gate:**
> Advance when all 3 checks pass. Refuse to deploy with red CI or untested staging.

### Stage 2: Deploy

**Intent:** Run deploy script. Never manual.

**Tasks:**
- Execute deploy script
- Watch deploy logs
- Verify deploy version on prod

**Methodologies in chain:**
- `feature-flags-rollout-targeting` → `solo/dev/automation-tooling/feature-flags-rollout-targeting`
- `feature-flags` → `solo/dev/software-developer/feature-flags`
- `deploy-scripts` → `solo/infra/server-craft/deploy-scripts`
- `release-planning` → `solo/product/product-planning/release-planning`

**Outputs:**
- Deploy log
- Prod version confirmed

**Decision gate:**
> Advance when prod runs new version. Stay if deploy errors.

### Stage 3: Verify

**Intent:** Health checks + key flows + flag rollout.

**Tasks:**
- Run health checks
- Walk through 3 critical user flows
- Roll flag 5% → 25% → 50% → 100%

**Methodologies in chain:**
- `health-checks-autoheal` → `solo/infra/server-craft/health-checks-autoheal`
- `monitoring-logging` → `solo/infra/server-craft/monitoring-logging`
- `logging-patterns` → `solo/dev/automation-tooling/logging-patterns`

**Outputs:**
- Health-check pass log
- Flag rollout log

**Decision gate:**
> Advance when health green + flows work. Hot-rollback flag if any flow breaks.

### Stage 4: Rollback drill

**Intent:** Prove the rollback path works (test in staging post-deploy).

**Tasks:**
- Trigger rollback in staging
- Verify rollback completes <5min
- Document rollback command

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- Rollback runbook entry

**Decision gate:**
> Required output: rollback proven in staging this deploy. Without it, next incident is fatal.

## Common pitfalls

- Deploying without flag because 'it's a small change' — small changes break prod most often
- Skipping rollback drill — first time you need it is the worst time to discover it doesn't work

## Quality checklist (self-review)

- Can I roll this back in under 5 minutes if I'm on a phone at 3am?
- Did I actually walk the critical flows, or just check that the homepage loads?

## Related playbooks

- `daily-sdd-spec-code-review`
- `solo-prod-incident-response`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **solo-deploy-checklist** (tier `solo`, blocks stage 1) — Pre-flight stage needs explicit checklist tailored to one operator
- **one-person-rollback-runbook** (tier `solo`, blocks stage 4) — Rollback-drill stage needs runbook that works without team

## CLI usage

```
faion get-content deploy-day-staging-to-prod --format md       # human-readable rendering
faion get-content deploy-day-staging-to-prod --format context  # agent-optimised context bundle
faion get-content deploy-day-staging-to-prod --format json     # raw structured form
```
