---
slug: ops-legal-compliance
tier: pro
group: marketing
domain: gtm-strategist
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: An index and routing methodology for online-business legal compliance.
content_id: "eb59174771230382"
tags: [legal, compliance, gdpr, ccpa, business-structure]
---
# Legal Compliance — Routing and Overview

## Summary

**One-sentence:** An index and routing methodology for online-business legal compliance.

**One-paragraph:** An index and routing methodology for online-business legal compliance. Covers business structure selection, essential policies (Terms, Privacy, Cookie, Refund), key regulations (GDPR, CCPA, CAN-SPAM, COPPA, ADA, PCI-DSS), intellectual property protection, and contractor/vendor contracts. The actual content is split into two focused sub-methodologies: ops-legal-basics (foundation and policy framework) and ops-legal-compliance-checklist (stage-by-stage implementation tracker).

## Applies If (ALL must hold)

- Setting up legal foundation for a new business (entity, EIN, policies)
- Choosing business structure (LLC vs S-Corp vs sole prop)
- Drafting or auditing policies (Terms, Privacy, Cookie, Refund)
- Pre-launch compliance review
- Routing an agent to the right sub-methodology (basics vs checklist)

## Skip If (ANY kills it)

- Final production policy generation — LLM drafts require attorney review; this methodology provides structure, not approved legal text
- Jurisdiction-specific advice (non-US: UK GDPR, LGPD, India DPDP) — US-centric framing; localize with counsel
- Incident response / breach notification — legal counsel + privacy officer own this; agent role is logistics only
- Regulatory filings or correspondence with government bodies — human-only

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
