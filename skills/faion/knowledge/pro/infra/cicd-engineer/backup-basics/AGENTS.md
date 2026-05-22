---
slug: backup-basics
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: # Backup Basics ## Overview Backup strategies ensure data protection, business continuity, and disaster recovery capabilities.
content_id: "0c11e3fd23c7387f"
tags: [[]]
---
# Backup Basics

## Summary

**One-sentence:** # Backup Basics ## Overview Backup strategies ensure data protection, business continuity, and disaster recovery capabilities.

**One-paragraph:** # Backup Basics ## Overview Backup strategies ensure data protection, business continuity, and disaster recovery capabilities. This methodology covers backup fundamentals, types, core principles, and modern best practices for 2025-2026. ## When to Use - Setting up data protection for applications - Implementing disaster recovery (DR) plans - Meeting compliance requirements (GDPR, HIPAA, SOC2) - Protecting against ransomware and data loss - Planning infrastructure migrations - Configuring SaaS backup strategies ## Backup Types | Type | Description | Pros | Cons | Frequency | |------|-------------|------|------|-----------| | Full | Complete copy of all data | Fast recovery, self-contained | Storage intensive, time consuming | Weekly/monthly | | Incremental | Changes since last backup | Fast, storage efficient | Slower recovery, chain dependency | Daily/hourly | | Differential | Changes since last full backup | Faster than full, easier recovery | Growing size over time | Daily | | Snapshot | Point-in-time copy (COW) | Instant, space efficient | Same storage system risk | Hourly/on-demand | | Continuous | Real-time data sync | Near-zero RPO | Complex, expensive | Continuous | ## The 3-2-1 Backup Rule The foundational backup strategy: ``` 3 copies of data 1 primary (production) 1 local backup 1 offsite backup 2 different media types Disk storage Object storage / tape / cloud 1 offsite copy Different geographic location ``` ## Modern Enhanced Strategies (2025-2026) ### 3-2-1-1-0 Strategy Enhanced for ransomware protection: | Component | Meaning | |-----------|---------| | 3 | Three copies of data | | 2 | Two different media types | | 1 | One offsite copy | | 1 | One immutable or air-gapped copy | | 0 | Zero errors after verification | ### 4-3-2 Strategy For high-compliance, high-uptime environments: | Component | Meaning | |-----------|---------| | 4 | Four copies of data | | 3 | Three separate locations | | 2 | Two offsite locations | ## Recovery Objectives ### RTO (Recovery Time Objective) Time to restore operations after disaster: | RTO Target | Backup Strategy | Cost | |------------|-----------------|------| | < 1 hour | Hot standby, continuous replication | High | | 1-4 hours | Automated restore, frequent backups | Medium | | 4-24 hours | Standard backup/restore process | Low | | > 24 hours | Manual restore, tape backups | Very low | ### RPO (Recovery Point Objective) Maximum acceptable data loss: | RPO Target | Backup Frequency | Cost | |------------|------------------|------| | < 1 hour | Continuous replication, WAL | High | | 1-4 hours | Hourly incremental backups | Medium | | 4-24 hours | Daily backups | Low | | > 24 hours | Weekly backups | Very low | ## Key Concepts ### Immutability Immutable backups cannot be modified or deleted during retention periods: - Object lock (S3, GCS, Azure Blob) - WORM storage (Write Once Read Many) - Air-gapped copies - Critical for ransomware protection ### Retention Policies Balance recoverability, storage co

## Applies If (ALL must hold)

- TBD — populate from v1 when-to-use list

## Skip If (ANY kills it)

- TBD — populate from v1 when-not-to-use list

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
