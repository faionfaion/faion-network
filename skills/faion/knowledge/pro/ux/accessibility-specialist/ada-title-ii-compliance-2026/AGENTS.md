---
slug: ada-title-ii-compliance-2026
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Compliance methodology for US state and local government entities required to meet WCAG 2.
content_id: "bb08276adc5356a0"
tags: [ada, title-ii, compliance, wcag, government]
---
# ADA Title II Compliance 2026

## Summary

**One-sentence:** Compliance methodology for US state and local government entities required to meet WCAG 2.

**One-paragraph:** Compliance methodology for US state and local government entities required to meet WCAG 2.1 Level AA under the DOJ ADA Title II final rule: large entities (50K+ population) by April 24, 2026; smaller entities by April 24, 2027. Covers full scope (web, mobile apps, multimedia, PDFs, third-party content), the six-step remediation roadmap, accessibility statement requirements, VPAT/ACR documentation, training, and procurement standards.

## Applies If (ALL must hold)

- US state/local government entity or federal-funded program building or auditing public-facing digital services.
- Vendor responding to government RFP requiring VPAT/ACR and remediation plan.
- Procurement officer evaluating third-party SaaS for accessibility risk before contract award.
- Pre-litigation triage after a DOJ complaint or Title II demand letter.
- Drafting or reviewing accessibility statements, procurement clauses, or staff training plans.

## Skip If (ANY kills it)

- Private commercial sites unrelated to government funding — ADA Title III and WCAG 2.2 AA apply; different case law.
- EU-only products — use regulatory-compliance-2026 for EAA + EN 301 549.
- Internal-only tools not used by the public — Section 504/508 may apply instead of the Title II web rule.
- Greenfield design — apply accessibility-first-design from day one to avoid remediation cost.

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
