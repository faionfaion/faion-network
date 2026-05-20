---
slug: ai-governance-compliance
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: EU AI Act and regulations require compliance frameworks for high-risk AI systems.
content_id: "2f7186694b8481f5"
tags: [governance, compliance, bias-detection, explainability, audit-logging]
---
# AI Governance and Compliance

## Summary

**One-sentence:** EU AI Act and regulations require compliance frameworks for high-risk AI systems.

**One-paragraph:** EU AI Act and regulations require compliance frameworks for high-risk AI systems. Implement governance through model cards, bias monitoring, explainability reporting (SHAP/LIME), human oversight mechanisms, and data governance documentation to meet regulatory requirements for risk classification, transparency, and bias mitigation.

## Applies If (ALL must hold)

- Deploying AI systems in EU markets where the AI Act applies (effective August 2024, tiered enforcement through 2027).
- Building high-risk AI applications: recruitment, credit scoring, biometric ID, medical diagnostics, law enforcement tools.
- Any product that makes consequential automated decisions affecting natural persons.
- When organizational policies require documented model cards, bias audits, or explainability reports.
- Preparing for enterprise sales where buyers require SOC 2 / ISO 42001 compliance evidence.
- Audit trail requirements: financial services, healthcare, public sector AI deployments.

## Skip If (ANY kills it)

- Internal developer tooling with no external user impact — overhead exceeds benefit.
- Pure B2B APIs where the downstream customer handles their own compliance.
- Low-risk AI (EU AI Act Annex III exclusions): spam filters, AI-powered search on public content, simple recommendation engines with no legal/financial effect.
- Prototype / research phase — implement governance before production launch, not before first demo.

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

- parent skill: `geek/ai/ai-agents/`
