---
slug: stakeholder-analysis
tier: pro
group: ba
domain: ba-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identify parties affected by change initiatives, classify by influence and impact, document needs, and plan engagement.
content_id: "42ba2d9d896f76bf"
tags: [stakeholder, analysis, engagement, bakok, salience]
---
# Stakeholder Analysis

## Summary

**One-sentence:** Identify parties affected by change initiatives, classify by influence and impact, document needs, and plan engagement.

**One-paragraph:** Identify parties affected by change initiatives, classify by influence and impact, document needs, and plan engagement. Uses Mendelow grid for cadence and Mitchell-Agle-Wood salience model for prioritization. Definitions must be frozen before any classification begins.

## Applies If (ALL must hold)

- Starting any initiative: identify stakeholders before the first interview or workshop
- Regulated / audited programs (SOX, MDR, ISO 13485, GDPR Art. 35 DPIA) needing BAKOK-aligned artifacts
- Onboarding a new BA or agent to an existing program to ensure reproducible classification
- Choosing a responsibility model (RACI vs RASCI vs DACI vs RAPID) for a specific decision class
- Disambiguating "stakeholder" from "user", "persona", "actor", "customer" across Confluence/Notion pages

## Skip If (ANY kills it)

- Solo / pre-PMF work where ceremony exceeds value — use direct customer discovery
- Pure code refactor with zero business-stakeholder change
- One-shot decisions with a single accountable owner — a one-line ADR is enough
- Open-source community projects with pseudonymous identities (salience axes cannot be measured)

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

- parent skill: `pro/ba/ba-core/`
