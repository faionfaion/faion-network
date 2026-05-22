---
slug: procurement-management
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six-step framework for engaging external vendors: make-or-buy decision, Statement of Work (SOW) with explicit acceptance criteria, contract type selection (Fixed Price / T&M / Cost Plus), weighted vendor evaluation, contract negotiation, and ongoing vendor management.
content_id: "c2d78ba7772d57bb"
tags: [procurement, vendor-management, contracts, sow, vendor-evaluation]
---
# Procurement Management Framework

## Summary

**One-sentence:** Six-step framework for engaging external vendors: make-or-buy decision, Statement of Work (SOW) with explicit acceptance criteria, contract type selection (Fixed Price / T&M / Cost Plus), weighted vendor evaluation, contract negotiation, and ongoing vendor management.

**One-paragraph:** Six-step framework for engaging external vendors: make-or-buy decision, Statement of Work (SOW) with explicit acceptance criteria, contract type selection (Fixed Price / T&M / Cost Plus), weighted vendor evaluation, contract negotiation, and ongoing vendor management. Every contract must pass a mandatory clause checklist before signing.

## Applies If (ALL must hold)

- Defining a make-or-buy framework before engaging external vendors
- Drafting SOW, Master Services Agreement (MSA), or Data Processing Addendum (DPA) skeletons
- Running an RFI / RFP / RFQ process: vendor list, evaluation matrix, weighted scoring
- Selecting contract type for a defined scope and risk profile
- Vendor risk and security review (SOC 2, ISO 27001, GDPR DPA) intake
- Ongoing vendor management: SLA tracking, change requests, performance reviews

## Skip If (ANY kills it)

- Spot purchases under a PO threshold (e.g. under $5K) where formal procurement is overhead
- Highly regulated industries with established central procurement and legal teams — defer to org policy
- SaaS tools the engineering team can self-onboard with monthly billing (security review still needed, but not a full RFP)

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

- parent skill: `pro/pm/project-manager/`
