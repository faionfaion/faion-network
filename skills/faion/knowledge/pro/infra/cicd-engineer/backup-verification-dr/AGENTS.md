---
slug: backup-verification-dr
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement automated backup verification (restore-to-temp-target + integrity probe), Prometheus alerting rules for backup age, size anomalies, and duration spikes, and DR runbooks with quarterly full DR drills.
content_id: "ec30ff5c3425573e"
tags: [backup, disaster-recovery, monitoring, prometheus, restore-drill]
---
# Backup Verification, Monitoring, and Disaster Recovery

## Summary

**One-sentence:** Implement automated backup verification (restore-to-temp-target + integrity probe), Prometheus alerting rules for backup age, size anomalies, and duration spikes, and DR runbooks with quarterly full DR drills.

**One-paragraph:** Implement automated backup verification (restore-to-temp-target + integrity probe), Prometheus alerting rules for backup age, size anomalies, and duration spikes, and DR runbooks with quarterly full DR drills. Without scheduled verification, a backup that has never been restored is undefined behavior — not a backup.

## Applies If (ALL must hold)

- Any production backup pipeline — verification is not optional at this tier.
- Setting up Prometheus alerting for backup jobs alongside existing infrastructure monitoring.
- Creating a DR runbook as part of a new service launch or compliance audit.
- Automating weekly restore drills in an isolated test environment.
- Replacing a manual "we check the logs" backup monitoring process with an automated alert pipeline.

## Skip If (ANY kills it)

- Verification in the same target database as production — always restore to an isolated database or namespace to avoid overwriting live data.
- Automated production restore without human approval — restore drills must be isolated; prod restores always require human gate.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
