---
slug: interface-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identifies and documents all boundaries and connections between a solution and external systems, users, hardware, and communication channels, then specifies data elements, protocols, frequency, volume, security, and error handling for each.
content_id: "2cf51d161bc39848"
tags: [interface-analysis, system-integration, data-flows, enterprise-architecture, governance]
---
# Interface Analysis

## Summary

**One-sentence:** Identifies and documents all boundaries and connections between a solution and external systems, users, hardware, and communication channels, then specifies data elements, protocols, frequency, volume, security, and error handling for each.

**One-paragraph:** Identifies and documents all boundaries and connections between a solution and external systems, users, hardware, and communication channels, then specifies data elements, protocols, frequency, volume, security, and error handling for each. At enterprise scale, a portfolio-level integration landscape register (one row per source-target pair, with criticality tier, sensitivity classification, and owner) precedes per-interface specification and feeds SOC2/ISO 27001/GDPR Art. 30 compliance evidence. Systems built in isolation fail at integration time; interface requirements discovered during development are the most expensive to fix.

## Applies If (ALL must hold)

- Pre-discovery for an enterprise-wide programme (ERP migration, M&A, core-system replacement) requiring a portfolio-level interface inventory.
- Drafting an integration target operating model: which team owns which interface, approval process, single source of truth.
- Building a cross-system traceability matrix (capability → process → system → interface) to scope SOWs and impact analyses.
- API contract governance: naming, versioning, deprecation, SLA, security baseline standards for all internal/external interfaces.
- Vendor/partner onboarding with 20+ interfaces requiring a criticality-rated register with renewal dates.
- Producing IT general controls evidence (SOC2, ISO 27001, GDPR Art. 30) listing every system-to-system data flow with PII classification.

## Skip If (ANY kills it)

- Single feature with one external API call — use the per-interface spec in ba-modeling/interface-analysis.
- Greenfield startup with fewer than five systems — a one-page integration diagram is enough.
- Pure technical refactor (bumping protobuf version) where business capability mapping adds no decision value.
- Organisation lacks a system-of-record for applications (no APM/CMDB) — build that first.

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

- parent skill: `pro/ba/business-analyst/`
