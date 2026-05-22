---
slug: ops-tax-compliance
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An operational checklist for US-based solopreneurs to stay penalty-free: compute quarterly estimated payments using the safe-harbor rule (100% of prior-year tax, 110% if AGI exceeds 150K), pay by the IRS quarterly due dates, maintain a structured record-keeping system, execute year-end deduction sweep (retirement contributions, Section 179, expense acceleration), and file on time or extend.
content_id: "5a0cb2f74ea298fc"
tags: [tax, compliance, quarterly-estimates, record-keeping, filing]
---
# Tax Compliance & Filing

## Summary

**One-sentence:** An operational checklist for US-based solopreneurs to stay penalty-free: compute quarterly estimated payments using the safe-harbor rule (100% of prior-year tax, 110% if AGI exceeds 150K), pay by the IRS quarterly due dates, maintain a structured record-keeping system, execute year-end deduction sweep (retirement contributions, Section 179, expense acceleration), and file on time or extend.

**One-paragraph:** An operational checklist for US-based solopreneurs to stay penalty-free: compute quarterly estimated payments using the safe-harbor rule (100% of prior-year tax, 110% if AGI exceeds 150K), pay by the IRS quarterly due dates, maintain a structured record-keeping system, execute year-end deduction sweep (retirement contributions, Section 179, expense acceleration), and file on time or extend. Non-US jurisdictions require localization.

## Applies If (ALL must hold)

- First profitable year as a solopreneur or LLC: setting up quarterly estimate cadence.
- Multi-state nexus surfaces (SaaS selling into CA/NY/WA, or physical goods crossing thresholds).
- Year-end planning when LLC profit clears the threshold for S-Corp election (approximately 80K SE income).
- International seller hitting EU/UK VAT thresholds or Stripe Tax onboarding.

## Skip If (ANY kills it)

- Novel situations: equity comp, R&D credits, multi-entity structures, ERC, audit defense — require a CPA.
- Determining nexus liability in previously unserved jurisdictions — LLM nexus reasoning is frequently wrong.
- When an IRS or state notice has already arrived — go directly to a tax professional.
- Real-time tax calculations on customer transactions — use Stripe Tax / Avalara / TaxJar APIs, not an LLM.

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
