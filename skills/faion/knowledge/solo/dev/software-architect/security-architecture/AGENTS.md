---
slug: security-architecture
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Designing secure systems with defense in depth, Zero Trust principles, and modern authentication/authorization patterns.
content_id: "fcfb7118c08f2a5a"
tags: [security, zero-trust, authentication, authorization, threat-modeling]
---
# Security Architecture

## Summary

**One-sentence:** Designing secure systems with defense in depth, Zero Trust principles, and modern authentication/authorization patterns.

**One-paragraph:** Designing secure systems with defense in depth, Zero Trust principles, and modern authentication/authorization patterns. Security architecture is the systematic approach to protecting systems, data, and users through layered defenses. Modern security architecture follows the principle of "never trust, always verify" (Zero Trust) while implementing defense in depth across all layers.

## Applies If (ALL must hold)

- Designing authentication, authorization, and identity flows for a new product or new tenant model.
- Threat modeling a new feature, integration, or third-party dependency before code freeze.
- Compliance-driven design (SOC 2, HIPAA, GDPR, PCI-DSS, ISO 27001) that requires documented controls and evidence.
- Reviewing existing architecture for Zero Trust gaps, secret-handling failures, or perimeter-only assumptions.
- Hardening an LLM-augmented system — prompt-injection surface, tool-permission scope, exfiltration paths.

## Skip If (ANY kills it)

- Fixing a single CVE in a dependency — use SCA tooling, not a full architecture loop.
- Pure secret rotation operational tasks — use Vault/KMS runbooks.
- UI form validation hygiene only — covered by application-developer methodologies.

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

- parent skill: `solo/dev/software-architect/`
