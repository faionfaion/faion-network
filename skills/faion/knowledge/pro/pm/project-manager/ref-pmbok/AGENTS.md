---
slug: ref-pmbok
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Quick-reference for PMBoK 7/8 domains, principles, EVM formulae, estimation accuracy bands, risk strategies, RAG thresholds — used as constants table in agent system prompts.
content_id: "27e93158b2b9366d"
complexity: light
produces: rubric
est_tokens: 3200
tags: [pmbok, reference, evm, pmp, risk-management]
---
# PMBoK 7 and 8 Reference

## Summary

**One-sentence:** Quick-reference for PMBoK 7/8 domains, principles, EVM formulae, estimation accuracy bands, risk strategies, RAG thresholds — used as constants table in agent system prompts.

**One-paragraph:** Quick-reference tables for PMBoK 7 (8 performance domains, 12 principles) and PMBoK 8 (7 domains, 6 principles), plus EVM formulae, estimation accuracy bands, risk response strategies, and RAG status thresholds. Constants module for agent system prompts — inject the relevant table to anchor terminology. Not a methodology to do anything; pair with operational methodologies (WBS, risk register, stakeholder engagement). EVM arithmetic always computed in code; LLMs drift on multi-row arithmetic.

**Ефективно для:**

- Grounding PMBoK terminology in system prompts and sponsor decks
- EVM formula lookup during status reporting
- Disambiguating PMBoK 6 vs 7 vs 8 vocabulary before generating PM content
- Translation layer for teams migrating editions

## Applies If (ALL must hold)

- Ground-truthing PMBoK terminology in system prompts or sponsor decks
- Quick-lookup of EVM formulae, risk strategies, estimation accuracy, RAG thresholds during status report generation
- Disambiguating PMBoK 6 vs 7 vs 8 vocabulary before generating any PM content
- Building a translation layer for teams migrating between editions

## Skip If (ANY kills it)

- As a standalone methodology to do anything — pair with operational methodologies
- Non-PMI frameworks (PRINCE2, IPMA, ISO 21500) — vocabulary overlaps but differs
- Agile-only environments with no baseline — EVM formulae are meaningless

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PMBoK edition | string | pin in system prompt — '7' or '8' |
| Baseline data | YAML | BAC, PV, EV, AC for EVM lookups |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[seven-performance-domains]] | PMBoK 7/8 domain vocabulary |
| [[six-core-principles]] | PMBoK 8 principle vocabulary |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: show-formula-and-result, clamp-zero-denominators, name-estimation-technique, one-strategy-per-risk, rag-recalibration | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the artefact + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-evm` | haiku | Pure arithmetic in script — no LLM |
| `ground-vocab` | haiku | Template substitution from constants |
| `edition-drift-audit` | sonnet | Pattern-match agent output for PMBoK 6 vocab |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-table.md` | EVM constants table for system prompt injection |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/evm-calculator.py` | EVM calculator: SV, CV, SPI, CPI, EAC, ETC, VAC, RAG from BAC/PV/EV/AC | On every status report generation |
| `scripts/validate-ref-pmbok.py` | Validate edition-pinned output: domain list length 7 or 8, vocabulary compliance | Pre-commit on system-prompt files |

## Related

- parent skill: `pro/pm/project-manager/`
- [[seven-performance-domains]]
- [[six-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
