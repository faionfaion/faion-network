---
slug: pre-launch-hardening-mvp
tier: solo
group: launch-operations
persona: P1
goal: TBD
complexity: deep
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: MVP that works on localhost → MVP that survives paying customers without a co-founder/SRE.
content_id: 2d89fba1573b1b14
methodology_refs:
  - security-testing
  - secrets-management
  - backup-recovery
  - ops-customer-support
  - feedback-management
---

# Pre-launch hardening: vibe-coded MVP to safe-to-bill production

**Playbook slug:** `pre-launch-hardening-mvp`  
**Tier:** solo  
**Complexity:** deep  
**Persona:** P1 — Solo SaaS Builder

## Intent

MVP that works on localhost → MVP that survives paying customers without a co-founder/SRE.

## Scope

Solo founder takes an MVP that works on localhost and makes it survive paying customers without a co-founder or SRE. End state: Stripe live, RLS audited, backups proven, legal docs live, support inbox routed. Exit artifact is a hardening checklist with every row checked or explicitly accepted-risk.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a single-operator SaaS founder. It assumes no team, no SRE rotation, no co-founder. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill — solo founders drift fastest where stages don't end cleanly.

### Non-goals

- SOC2 / ISO compliance — overkill at pre-launch
- Multi-region failover — single-region only

### Prerequisites

- MVP works end-to-end on localhost
- Stripe test mode integrated

## Success criteria

The playbook is done when:
- Stripe live mode tested with real $1 charge + refund
- Row-level security (or equivalent) audited per table
- Secrets management: no secrets in git, vault in use
- Backups: restore drill performed once before launch
- Legal docs live: ToS, Privacy, Refund
- Support inbox routed + first-reply SLA documented

## Stages

### Stage 1: Security audit

**Intent:** Catch the vibe-coded security debt before paying customers do.

**Tasks:**
- Audit RLS / authz per table
- Scan git history for secret leaks
- Run security tests

**Methodologies in chain:**
- `security-testing` → `solo/dev/testing-developer/security-testing`
- `secrets-management` → `solo/infra/server-craft/secrets-management`

**Outputs:**
- Security audit report

**Decision gate:**
> Advance when zero P0/P1 findings open. Refuse launch with any open P0.

### Stage 2: Payments hardening

**Intent:** Stripe live + webhooks + refund flow tested.

**Tasks:**
- Switch Stripe to live keys
- Harden webhooks (idempotency, signature)
- Test $1 charge + refund end-to-end

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- Stripe live test log

**Decision gate:**
> Advance when $1 charge + refund cycle works clean. Stay if webhooks miss events.

### Stage 3: Backups

**Intent:** Prove restore, don't just enable backups.

**Tasks:**
- Configure backups (or verify)
- Run a restore drill on staging
- Document restore command

**Methodologies in chain:**
- `backup-recovery` → `solo/infra/server-craft/backup-recovery`

**Outputs:**
- Restore drill log

**Decision gate:**
> Advance when restore completed successfully. Refuse launch without proven restore.

### Stage 4: Legal

**Intent:** ToS / Privacy / Refund live and linked from footer.

**Tasks:**
- Draft ToS / Privacy / Refund (template + edits)
- Publish at /legal/*
- Link from footer + checkout

**Methodologies in chain:**
- (no resolved methodologies — see gaps below)

**Outputs:**
- 3 published legal docs

**Decision gate:**
> Advance when all 3 are live. Stay if any missing.

### Stage 5: Support

**Intent:** Inbox routed. Customer can reach you.

**Tasks:**
- Route support inbox (email / Crisp)
- Set first-reply SLA
- Set up FAQ baseline

**Methodologies in chain:**
- `ops-customer-support` → `solo/marketing/gtm-strategist/ops-customer-support`
- `feedback-management` → `solo/product/product-operations/feedback-management`

**Outputs:**
- Support routing config

**Decision gate:**
> Required output: live inbox + documented SLA. No invisible founders post-launch.

## Common pitfalls

- Going live with backups enabled but never restored — discovering it doesn't work mid-incident
- Skipping legal docs because 'just MVP' — refund disputes get expensive fast

## Quality checklist (self-review)

- Could I restore prod tonight from yesterday's backup without panic?
- Did the $1 charge + refund cycle actually settle, or just look successful in the UI?

## Related playbooks

- `solo-prod-incident-response`
- `deploy-day-staging-to-prod`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **supabase-rls-audit-checklist** (tier `solo`, blocks stage 1) — Security-audit stage needs RLS checklist for Supabase stack
- **vibe-coded-mvp-security-audit** (tier `solo`, blocks stage 1) — Security-audit stage needs holistic audit specific to AI-generated MVPs
- **secret-leak-git-history-scan** (tier `solo`, blocks stage 1) — Security-audit stage needs concrete scan procedure
- **stripe-webhook-hardening** (tier `solo`, blocks stage 2) — Payments-hardening stage needs explicit hardening checklist
- **solo-saas-legal-docs-pack** (tier `solo`, blocks stage 4) — Legal stage needs solo-scale ToS/Privacy/Refund pack
- **gdpr-for-solo-saas** (tier `solo`, blocks stage 4) — Legal stage needs GDPR essentials at solo-scale
- **subscription-lifecycle-edge-cases** (tier `solo`, blocks stage 2) — Payments stage needs edge-case catalogue (trial, dunning, etc.)
- **supabase-backup-and-restore-drill** (tier `solo`, blocks stage 3) — Backups stage needs Supabase-specific drill
- **postgres-pitr-for-solos** (tier `solo`, blocks stage 3) — Backups stage needs PITR setup for solo-scale Postgres
- **solo-support-sla-template** (tier `solo`, blocks stage 5) — Support stage needs SLA template scoped to one operator
- **first-100-tickets-playbook** (tier `solo`, blocks stage 5) — Support stage needs playbook for early-stage ticket volume

## CLI usage

```
faion get-content pre-launch-hardening-mvp --format md       # human-readable rendering
faion get-content pre-launch-hardening-mvp --format context  # agent-optimised context bundle
faion get-content pre-launch-hardening-mvp --format json     # raw structured form
```
