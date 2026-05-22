---
slug: vui-privacy-security
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Voice interfaces handling personal data require privacy-by-design: transparency before capture, visual plus audio trust indicators, step-up authentication for sensitive actions, and PII redaction at transcript boundaries.
content_id: "1aad2fef0065bca2"
tags: [voice-ui, privacy, security, gdpr, compliance]
---
# VUI Privacy and Security

## Summary

**One-sentence:** Voice interfaces handling personal data require privacy-by-design: transparency before capture, visual plus audio trust indicators, step-up authentication for sensitive actions, and PII redaction at transcript boundaries.

**One-paragraph:** Voice interfaces handling personal data require privacy-by-design: transparency before capture, visual plus audio trust indicators, step-up authentication for sensitive actions, and PII redaction at transcript boundaries. Voice data is legally regulated (GDPR, HIPAA, CCPA, BIPA) and technically leaky; cloud transcripts persist on third-party infrastructure.

## Applies If (ALL must hold)

- Designing a voice agent that handles personal data (banking, health, identity, child profiles).
- Submitting an Alexa/Google Action for certification — privacy disclosures are mandatory and reviewed.
- Operating in regulated jurisdictions: GDPR, HIPAA, CCPA/CPRA, Illinois BIPA, EU AI Act (voice biometrics).
- Building voice flows in customer support that may capture card numbers, OTPs, or account secrets.

## Skip If (ANY kills it)

- Internal-only voice prototypes with synthetic data — full disclosure flows can be deferred until external pilot.
- Non-voice UI forms — apply standard data-minimisation principles instead; voice-specific patterns do not apply.

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
