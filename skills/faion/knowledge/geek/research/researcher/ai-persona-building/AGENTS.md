---
slug: ai-persona-building
tier: geek
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Fully automated end-to-end persona generation for large user datasets (1,000+ users): Haiku ingests behavioral event exports via API, Opus validates cluster separability, Sonnet transforms clusters into JSON persona documents consumable by downstream agents.
content_id: "2550b232685227d3"
tags: [personas, clustering, automation, agent-workflow]
---
# AI Persona Building (Automated Pipeline)

## Summary

**One-sentence:** Fully automated end-to-end persona generation for large user datasets (1,000+ users): Haiku ingests behavioral event exports via API, Opus validates cluster separability, Sonnet transforms clusters into JSON persona documents consumable by downstream agents.

**One-paragraph:** Fully automated end-to-end persona generation for large user datasets (1,000+ users): Haiku ingests behavioral event exports via API, Opus validates cluster separability, Sonnet transforms clusters into JSON persona documents consumable by downstream agents. Human approval gate sits between Opus and Sonnet.

## Applies If (ALL must hold)

- Automating persona generation as part of a recurring research pipeline (monthly cohort refresh).
- Building personas programmatically from large datasets where manual review of clustering is infeasible.
- Running JTBD map generation at scale across multiple product areas simultaneously.
- Integrating persona data into a downstream agent (copywriting, feature-priority) via stable JSON schema.

## Skip If (ANY kills it)

- One-off persona creation for a single product decision — use ai-assisted-persona-building with direct team involvement.
- When data quality is unknown — run a data audit before feeding into the pipeline.
- When personas will be presented to external stakeholders without human review of the narrative layer.

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

- parent skill: `geek/research/researcher/`
