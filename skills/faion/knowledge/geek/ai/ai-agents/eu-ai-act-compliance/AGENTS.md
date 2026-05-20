---
slug: eu-ai-act-compliance
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: August 2026 marks a major enforcement milestone for AI regulation in the EU.
content_id: "5d4bc55fe9e1f497"
tags: [eu-ai-act, compliance, governance, risk-management, regulation]
---
# EU AI Act Compliance (2026)

## Summary

**One-sentence:** August 2026 marks a major enforcement milestone for AI regulation in the EU.

**One-paragraph:** August 2026 marks a major enforcement milestone for AI regulation in the EU. Implement a comprehensive compliance framework covering risk classification, model cards, bias detection, explainability, human oversight mechanisms, and regulatory documentation. This methodology covers the key dates, requirements, risk classifications, penalties, and agentic workflows needed to meet August 2026 deadlines.

## Applies If (ALL must hold)

- Deploying any AI system that operates in or serves users in the EU (regardless of where the provider is incorporated)
- Building chatbots, recommendation engines, or automated decision systems marketed in the EU
- Creating agent systems that touch biometrics, employment, credit, education, or critical infrastructure
- Conducting a GPAI (General-Purpose AI Model) integration where the model's training data or outputs are subject to copyright and transparency obligations
- Establishing a compliance audit pipeline before an August 2026 enforcement deadline

## Skip If (ANY kills it)

- Purely internal R&D tools with no user-facing deployment
- AI systems deployed exclusively outside EU jurisdictions with no EU data subjects
- Spam filters, games, or scientific research tools that fall in the "minimal risk" category and require no documentation beyond ordinary engineering practice
- Prototypes under active development not yet in production

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
