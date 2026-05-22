---
slug: procurement-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured vendor engagement: make-or-buy decisions, Statement of Work authoring, contract type selection, vendor evaluation scoring, and ongoing performance monitoring.
content_id: "c2d78ba7772d57bb"
tags: [procurement, vendor-management, contracts, sow, sourcing]
---
# Procurement Management

## Summary

**One-sentence:** Structured vendor engagement: make-or-buy decisions, Statement of Work authoring, contract type selection, vendor evaluation scoring, and ongoing performance monitoring.

**One-paragraph:** Structured vendor engagement: make-or-buy decisions, Statement of Work authoring, contract type selection, vendor evaluation scoring, and ongoing performance monitoring. Every external engagement needs a written SOW with testable acceptance criteria before a contract is signed.

## Applies If (ALL must hold)

- Engaging external vendors, agencies, or contractors for work worth more than a minor purchase
- Choosing between building internally versus buying a service or product
- Preparing RFI / RFP / RFQ packages and vendor evaluation matrices
- Selecting contract type given scope clarity and risk tolerance
- Monitoring vendor deliverables against signed SOW milestones

## Skip If (ANY kills it)

- Sub-$1k one-off SaaS purchases — overhead exceeds value; use a credit card and receipt
- Open-source dependencies with no vendor relationship — treat as supply-chain risk, not procurement
- Internal cross-charging between business units — uses transfer pricing rules, not procurement contracts
- Highly regulated public-sector procurements (FAR/DFARS/EU directives) — methodology omits mandatory regulatory clauses

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

- parent skill: `pro/pm/pm-traditional/`
