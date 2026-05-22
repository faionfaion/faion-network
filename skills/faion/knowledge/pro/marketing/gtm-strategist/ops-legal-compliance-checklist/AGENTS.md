---
slug: ops-legal-compliance-checklist
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A stage-gated compliance tracker for online businesses: Day 1 (entity, EIN, bank account, core policies), Month 1 (website legal pages, data protection, payment processing, IP), Year 1 (tax compliance, employment/contractor law, marketing law, industry-specific, insurance), and Ongoing (policy update cycle, data management, audits, legal counsel).
content_id: "762652b2b1d98c0d"
tags: [compliance, checklist, implementation, audit, legal]
---
# Legal Compliance Checklist - Stage-by-Stage Implementation

## Summary

**One-sentence:** A stage-gated compliance tracker for online businesses: Day 1 (entity, EIN, bank account, core policies), Month 1 (website legal pages, data protection, payment processing, IP), Year 1 (tax compliance, employment/contractor law, marketing law, industry-specific, insurance), and Ongoing (policy update cycle, data management, audits, legal counsel).

**One-paragraph:** A stage-gated compliance tracker for online businesses: Day 1 (entity, EIN, bank account, core policies), Month 1 (website legal pages, data protection, payment processing, IP), Year 1 (tax compliance, employment/contractor law, marketing law, industry-specific, insurance), and Ongoing (policy update cycle, data management, audits, legal counsel). The checklist verifies presence and process - it does not verify that policy text is accurate or legally sufficient, which requires attorney review.

## Applies If (ALL must hold)

- Pre-launch: confirm all Day 1 items are in place before going live
- Post-launch (Month 1): complete data protection, payment, and IP items
- Quarterly audit: detect drift between policies and actual data flows/vendors
- After adding a new third-party integration (analytics, payments, AI provider)
- Producing compliance status snapshot for investor/acquirer due diligence

## Skip If (ANY kills it)

- Drafting policy text from scratch - use a generator (Termly, Iubenda) or counsel; this checklist verifies coverage, not wording
- Industry-regulated sectors (HIPAA, FINRA, FERPA, PCI-DSS) - baseline only; need vertical-specific checklists and legal review
- M&A or fundraising legal due diligence - broader scope (cap table, IP chain, employment, contracts)
- Disputes, takedowns, demand letters - adversarial process, not checklist-driven

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

- parent skill: `pro/marketing/gtm-strategist/`
