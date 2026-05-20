---
slug: feature-flag-cleanup-discipline
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "8c84f9b4c01a377b"
summary: "Retirement-side discipline for feature flags: every flag is born with an expiry, a removal owner, and a 'kill' definition so multi-month migrations and greenfield rollouts don't leave a sediment of stale toggles that quietly metastasize into tech debt."
tags: [dev, solo, feature-flags, tech-debt, retirement, cleanup]
---
# Feature Flag Cleanup Discipline

## Summary

Faion's dev corpus covers feature-flag rollout well but is silent on retirement, and the solo developer running a multi-month migration or a greenfield service from scaffold to production is exactly the operator who accumulates stale flags fastest. This methodology imposes a retirement-side contract: every flag is born with an expiry date, a named removal owner, and a measurable "ready to kill" definition; every sprint a cleanup pass runs against that ledger; flags that miss their kill date escalate before they become silent forks. It closes the loop that turns rollout discipline into the hidden tech-debt of un-removed toggles.

## Applies If

- The codebase uses feature flags (LaunchDarkly, Unleash, Statsig, ConfigCat, or an in-house toggle map).
- The current workstream is longer than four weeks and will create more than one new flag (greenfield rollout, major migration).
- The operator can write to the flag store and to the codebase that reads it.
- A code-side flag-ledger file (or remote equivalent) is reachable and editable.

## Skip If

- The project uses zero feature flags (no toggle layer to retire).
- Flags are exclusively kill-switches that must remain forever (operational, not release).
- The flag is regulator-imposed and may not be removed without compliance sign-off.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules for flag birth, expiry, sprint sweep, kill criteria, and stale-flag escalation |

## Related

- parent skill: `solo/dev/`
- triggering activity: `Greenfield service from scaffold to first production deploy (8 weeks)`, `Major framework / language migration (3 months)`
- neighbouring: `pro/dev/flag-killswitch-decision-criteria`, `pro/dev/feature-flag-weekly-review-template`
