---
slug: gcp-storage-cdn
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Storage provides four storage classes (STANDARD, NEARLINE, COLDLINE, ARCHIVE) with lifecycle rules to automate class transitions.
content_id: "ee5d802ae705b420"
tags: [gcp, cloud-storage, cdn, terraform, static-hosting]
---
# GCP Cloud Storage and CDN Architecture

## Summary

**One-sentence:** Cloud Storage provides four storage classes (STANDARD, NEARLINE, COLDLINE, ARCHIVE) with lifecycle rules to automate class transitions.

**One-paragraph:** Cloud Storage provides four storage classes (STANDARD, NEARLINE, COLDLINE, ARCHIVE) with lifecycle rules to automate class transitions. Cloud CDN sits in front of a backend bucket to cache static content globally, reduce origin load, and serve while stale for high availability.

## Applies If (ALL must hold)

- Hosting static assets (JS/CSS/images) served to global users — pair with CDN.
- Long-term archive storage for backups, logs, or compliance data — use COLDLINE/ARCHIVE.
- Infrequently accessed datasets (reports, exports) — use NEARLINE or COLDLINE with lifecycle rules.
- Serving a SPA or Gatsby/Hugo/Next.js static build via HTTPS with managed SSL — use backend bucket + Cloud CDN + HTTPS proxy.

## Skip If (ANY kills it)

- Storing database files or application state — use Cloud SQL, Firestore, or Bigtable instead.
- Dynamic server-rendered content — CDN caching is counterproductive for uncacheable responses.

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
