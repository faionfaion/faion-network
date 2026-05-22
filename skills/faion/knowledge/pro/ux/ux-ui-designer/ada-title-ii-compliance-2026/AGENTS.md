---
slug: ada-title-ii-compliance-2026
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A compliance methodology for US state and local government digital services required to meet WCAG 2.
content_id: "bb08276adc5356a0"
tags: [compliance, ada, government, wcag, legal]
---
# ADA Title II Compliance 2026

## Summary

**One-sentence:** A compliance methodology for US state and local government digital services required to meet WCAG 2.

**One-paragraph:** A compliance methodology for US state and local government digital services required to meet WCAG 2.1 Level AA under the DOJ final rule (28 CFR Part 35, effective April 24 2024), with large-entity deadline April 24 2026 and smaller-entity deadline April 26 2027. Non-compliant government digital services expose entities to DOJ enforcement, private litigation, and remediation costs that multiply when retrofitted post-launch.

## Applies If (ALL must hold)

- US state, local, or territorial government digital services covered by 28 CFR Part 35.
- Public universities, transit systems, libraries, courts, agency portals.
- SaaS vendors whose product is delivered to a covered entity under contract.
- Deadline planning: large entities (population 50K+) by April 24 2026; smaller by April 26 2027.

## Skip If (ANY kills it)

- Private-sector commercial sites — ADA Title III applies (different standard and remediation triggers).
- Federal government — Section 508 / ICT Refresh applies instead.
- Employee-facing internal tools at private employers — Title I applies.
- Non-covered entity marketing sites — out of scope for Title II.

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

- parent skill: `pro/ux/ux-ui-designer/`
