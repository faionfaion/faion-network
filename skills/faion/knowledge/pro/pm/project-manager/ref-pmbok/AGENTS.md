---
slug: ref-pmbok
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Quick-reference tables for PMBoK 7 (8 performance domains, 12 principles) and PMBoK 8 (7 domains, 6 principles), plus EVM formulae, estimation accuracy bands, risk response strategies, and RAG status thresholds.
content_id: "7e1c02a1a578c843"
tags: [pmbok, reference, evm, pmp, risk-management]
---
# PMBoK 7 and 8 Reference

## Summary

**One-sentence:** Quick-reference tables for PMBoK 7 (8 performance domains, 12 principles) and PMBoK 8 (7 domains, 6 principles), plus EVM formulae, estimation accuracy bands, risk response strategies, and RAG status thresholds.

**One-paragraph:** Quick-reference tables for PMBoK 7 (8 performance domains, 12 principles) and PMBoK 8 (7 domains, 6 principles), plus EVM formulae, estimation accuracy bands, risk response strategies, and RAG status thresholds. This is a constants module for agent system prompts — inject the relevant table to anchor terminology. Not a methodology for doing anything; pair with operational methodologies (WBS, risk register, stakeholder engagement).

## Applies If (ALL must hold)

- Ground-truthing PMBoK terminology in system prompts, sponsor decks, or certification content.
- Quick-lookup of EVM formulae, risk strategies, estimation accuracy, RAG thresholds during status report generation.
- Disambiguating PMBoK 6 vs 7 vs 8 vocabulary before generating any PM content.
- Building a translation layer for teams migrating from one edition to another.

## Skip If (ANY kills it)

- As a standalone methodology to do anything — it is a reference; pair with operational methodologies.
- For non-PMI frameworks (PRINCE2, IPMA, ISO 21500) — vocabulary overlaps but differs; a pure PMBoK lens distorts those frameworks.
- For agile-only environments that have no baseline — EVM formulae are meaningless without a scope and cost baseline.

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

- parent skill: `pro/pm/project-manager/`
