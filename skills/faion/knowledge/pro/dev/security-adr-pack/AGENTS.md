---
slug: security-adr-pack
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Pre-authored bundle of canonical security ADR stubs (auth, encryption, secrets, isolation, residency) that accelerates security-by-design audits."
content_id: "22a2ede7000f4f48"
tags: [security-adr-pack, dev, pro]
---
# Security ADR Pack

## Summary

**One-sentence:** A canonical bundle of five pre-authored Architecture Decision Record stubs covering the questions every security audit must answer.

**One-paragraph:** The standalone ADR methodology covers the format ("how to write an ADR"), but security-by-design audits demand answers to the same five questions every time: auth model, encryption-at-rest/in-transit, secrets management, isolation tier, data residency. Architects rediscover this set each audit, often missing one. This methodology ships the canonical pack — five ADR stubs with required prompts, decision-options matrix, and a sign-off block — so the audit reduces to filling in choices, not writing from scratch.

## Applies If (ALL must hold)

- a new service / product is entering security-by-design review
- the org maintains ADRs (or is willing to start) as a decision log
- output (filled ADRs) will be reviewed by a security lead or auditor
- tier == pro or higher

## Skip If (ANY kills it)

- the system is a prototype with no production users and no PII (defer)
- a parent system already owns these decisions and the new service inherits (link, do not duplicate)
- regulatory regime mandates a different ADR template (defer to that regime)

## Prerequisites

- the ADR methodology (format / sequencing) is already adopted by the team
- a security lead or threat-modelling owner exists
- the service scope is well-defined enough to answer the five questions

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/architecture-proposal-document-template` | parent ADR format |
| `pro/dev/software-architect` | role/operating context |
| `pro/dev/stride-threat-model-template` | sibling — threat-model inputs feed the auth/isolation ADRs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — one per canonical ADR — plus a worked auth-ADR example | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fill_adr_prompts` | sonnet | per-ADR free-form answers from architect input |
| `validate_pack_completeness` | haiku | structural check |
| `synthesize_audit_brief` | opus | cross-ADR synthesis when stakes are high |

## Related

- parent skill: `pro/dev/`
- `pro/dev/stride-threat-model-template`
- `pro/dev/architecture-proposal-document-template`
- upstream playbook: `role-software-architect/Security-by-design audit + threat-modelling cycle`
