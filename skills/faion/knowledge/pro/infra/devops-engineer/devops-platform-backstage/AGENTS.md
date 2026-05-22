---
slug: devops-platform-backstage
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Backstage is the CNCF-donated open-source developer portal (originally from Spotify) that combines a service catalog, TechDocs, and a golden path scaffolder (Software Templates) in one plugin-extensible platform.
content_id: "edcf8eb68dc4e477"
tags: [backstage, service-catalog, developer-portal, platform-engineering, cncf]
---
# Backstage: CNCF Developer Portal and Service Catalog

## Summary

**One-sentence:** Backstage is the CNCF-donated open-source developer portal (originally from Spotify) that combines a service catalog, TechDocs, and a golden path scaffolder (Software Templates) in one plugin-extensible platform.

**One-paragraph:** Backstage is the CNCF-donated open-source developer portal (originally from Spotify) that combines a service catalog, TechDocs, and a golden path scaffolder (Software Templates) in one plugin-extensible platform. It is the most common open-source foundation for enterprise IDPs in 2026. Backstage must be treated as a product, not a deployment — it requires dedicated engineering to maintain plugins and keep the catalog data accurate.

## Applies If (ALL must hold)

- Engineering org needing a unified portal to discover services, documentation, and self-service workflows.
- Teams spending significant time searching for service ownership, dependency information, or runbooks.
- Platform team that wants a plugin-extensible portal rather than building a custom web app from scratch.
- Orgs adopting golden paths who want a managed scaffolding UI rather than CLI-only templates.

## Skip If (ANY kills it)

- Teams without dedicated Backstage engineering capacity — an unmaintained catalog goes stale within weeks and loses developer trust permanently.
- Orgs under 50 engineers where a shared wiki and a Slack channel provide equivalent discoverability at zero maintenance cost.
- Orgs whose primary IDP requirement is infrastructure orchestration rather than service discovery — Backstage excels at the catalog layer, not the infrastructure layer (use Crossplane for that).

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
