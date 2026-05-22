---
slug: backup-strategies
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern backup strategy follows the 3-2-1-1-0 rule: 3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 verified recovery errors.
content_id: "7cbe26077cc595d2"
tags: [backup, disaster-recovery, 3-2-1-1-0, immutable-storage, ransomware-protection]
---
# Backup Strategies

## Summary

**One-sentence:** Modern backup strategy follows the 3-2-1-1-0 rule: 3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 verified recovery errors.

**One-paragraph:** Modern backup strategy follows the 3-2-1-1-0 rule: 3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 verified recovery errors. Implement automated restore verification after every backup job.

## Applies If (ALL must hold)

- Any production database, file system, or Kubernetes cluster requires DR capability
- Compliance requirements mandate data retention (GDPR, HIPAA, SOC2, PCI-DSS)
- RPO < 24 hours is a business requirement
- Ransomware protection is part of the security posture

## Skip If (ANY kills it)

- Ephemeral environments (CI runners, short-lived review apps) — backup overhead exceeds value; rely on infrastructure-as-code rebuild instead
- Data that can be fully regenerated from source (build artifacts, CDN caches) — store source, not derivatives
- Development databases with no production data — use database seeding scripts instead of backups

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

- parent skill: `pro/infra/devops-engineer/`
