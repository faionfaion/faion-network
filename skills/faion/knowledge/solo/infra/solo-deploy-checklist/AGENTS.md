---
slug: solo-deploy-checklist
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "e1d41c15db112fbe"
summary: One-page pre/during/post deploy checklist with explicit go/no-go criteria — sized for the solo operator pushing to a single production environment.
---
# Solo Deploy Checklist

## Summary

**One-sentence:** A one-page deploy checklist with three sections (pre, during, post) and explicit go/no-go criteria — the solo operator either passes every line or aborts.

**One-paragraph:** `deploy-scripts` and `vps-first-deploy` cover the mechanics of pushing code. Neither defines the go/no-go gate that catches the recurring solo-founder mistake: deploying on Friday at 6pm with no rollback path, or pushing a migration without backing up the DB. This methodology defines the fixed checklist: nine pre-deploy items (backup, branch, tests green, migration plan, rollback plan, feature flag default, observability ready, customer comms, time of day), four during-deploy items (deploy in transaction-friendly order, watch logs, smoke-test, declare "stable" only after N minutes), four post-deploy items (mark release, update changelog, verify metrics, sleep). Anchored to "Deploy-day staging-to-prod gate" for the solo SaaS builder.

## Applies If (ALL must hold)

- Solo founder pushing to a single live production environment (no staging duplicate, or staging is best-effort).
- Real users will see the change.
- The deploy involves either code, DB migration, infra change, or third-party integration update.
- A rollback path is technically possible.

## Skip If (ANY kills it)

- Internal-only tooling with no user impact and easy revert — overkill, use the simple `daily-ship-rubric` form.
- Static-content micro-update (typo fix, image swap) — overkill.
- Live incident — use the incident-response runbook, not this routine checklist.

## Prerequisites

- Working deploy script or one-command deploy.
- A monitoring surface (Sentry, OpenStatus, or even simple curl-uptime).
- Access to the customer comms channel (status page, email list, Twitter).
- A documented rollback procedure for the current version of the app.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/AGENTS.md` | Parent group context |
| `solo/infra/one-person-rollback-runbook` if present | Sibling — the rollback the checklist points at |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every deploy enforces | ~900 |

## Related

- parent skill: `solo/infra/`
- triggering activity: `p1-solo-saas-builder/Deploy-day staging-to-prod gate`
- adjacent: `solo/infra/one-person-rollback-runbook`, `solo/sdd/solo-blameless-postmortem-template`
