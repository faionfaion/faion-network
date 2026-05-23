---
slug: vui-privacy-security
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a voice privacy + security spec enforcing transparency-before-capture, visual + audio trust indicators, step-up authentication for sensitive actions, and PII redaction at transcript boundaries — across GDPR / HIPAA / CCPA / BIPA.
content_id: "1aad2fef0065bca2"
complexity: medium
produces: spec
est_tokens: 4200
tags: [voice-ui, privacy, security, gdpr, compliance]
---
# VUI Privacy and Security

## Summary

**One-sentence:** Produces a voice privacy + security spec enforcing transparency-before-capture, visual + audio trust indicators, step-up authentication for sensitive actions, and PII redaction at transcript boundaries — across GDPR / HIPAA / CCPA / BIPA.

**One-paragraph:** Voice interfaces handle personal data; legal regimes (GDPR, HIPAA, CCPA, BIPA) require transparency before capture and explicit consent; users need visual + audio trust indicators (e.g., recording light + chime); sensitive actions (payment, account changes) require step-up authentication; and PII MUST be redacted at transcript boundaries before logging. Cloud transcripts persist on 3rd-party infrastructure unless explicitly mitigated. This methodology emits a privacy/security spec consumed by legal review + engineering.

**Ефективно для:**

- Pre-launch privacy + security audit для voice product handling PII.
- GDPR / HIPAA / CCPA / BIPA compliance перевірка для voice flows.
- Step-up authentication для sensitive actions (payment, password reset).
- PII redaction policy для transcript logging.

## Applies If (ALL must hold)

- Voice product captures, stores, or transmits PII / health data / financial data.
- Users include EU, US, or California residents.
- Cloud ASR or LLM pipeline persists transcripts even briefly.

## Skip If (ANY kills it)

- Internal voice prototype with no real PII.
- Pure dictation tool with user-controlled storage.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Data inventory | list of fields per intent | PM / legal |
| Jurisdiction list | list | GTM / legal |
| ASR / LLM provider | vendor | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[voice-ui]] | intent + slot vocabulary upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: transparency-before-capture, trust-indicators-required, step-up-auth-sensitive, pii-redact-at-boundary, retention-and-deletion, minor-extra-protection | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `data-inventory` | haiku | Mechanical listing. |
| `draft-notices` | sonnet | Jurisdictional language. |
| `redaction-design` | sonnet | NER + regex coverage. |
| `legal-review` | opus | Cross-jurisdiction risk. |

## Templates

| File | Purpose |
|------|---------|
| `templates/privacy-spec.json` | Skeleton spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-privacy-security.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-conversation-design]]
- [[vui-accessibility-inclusivity]]
- [[regulatory-compliance-2026]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by data sensitivity + jurisdiction; enforces redaction, consent, step-up, and retention rules. Each leaf cites a rule from `01-core-rules.xml`.
