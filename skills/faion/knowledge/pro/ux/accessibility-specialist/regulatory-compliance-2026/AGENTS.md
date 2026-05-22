---
slug: regulatory-compliance-2026
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Regional accessibility law matrix for 2026: ADA Title II (US government, April 2026 deadline), European Accessibility Act (EU e-commerce + banking, June 2025/2030), Section 508, AODA (Canada), and equivalent frameworks in the UK, Australia, and Asia-Pacific.
content_id: "becb9815e2337741"
tags: [regulatory, compliance, legal, accessibility, wcag]
---
# Regulatory Compliance 2026

## Summary

**One-sentence:** Regional accessibility law matrix for 2026: ADA Title II (US government, April 2026 deadline), European Accessibility Act (EU e-commerce + banking, June 2025/2030), Section 508, AODA (Canada), and equivalent frameworks in the UK, Australia, and Asia-Pacific.

**One-paragraph:** Regional accessibility law matrix for 2026: ADA Title II (US government, April 2026 deadline), European Accessibility Act (EU e-commerce + banking, June 2025/2030), Section 508, AODA (Canada), and equivalent frameworks in the UK, Australia, and Asia-Pacific. Covers deadlines, WCAG standard mappings, documentation requirements (VPAT/ACR, accessibility statements), enforcement penalties, and exemptions.

## Applies If (ALL must hold)

- Determining which accessibility standard (WCAG 2.0/2.1/2.2, EN 301 549) applies to a given product and jurisdiction.
- Writing or auditing accessibility statements, VPATs, and ACRs.
- Setting up ongoing monitoring, training, and procurement standards for ADA/EAA compliance.
- Assessing risk before a product launch in a new region.
- Responding to a DOJ complaint or EU enforcement action.

## Skip If (ANY kills it)

- Technical WCAG implementation — use `wcag-22-compliance` or `a11y-testing`.
- AT runtime testing — use `testing-with-assistive-technology`.
- XR/spatial products — apply WCAG + W3C XAUR; no dedicated regulation yet.
- Internal-only tooling with no public-facing interface — most regulations apply to public-facing services only.

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

- parent skill: `pro/ux/accessibility-specialist/`
