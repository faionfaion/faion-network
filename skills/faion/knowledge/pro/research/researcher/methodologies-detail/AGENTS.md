---
slug: methodologies-detail
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A flat reference page bundling 20 research methodologies as a human-readable cheat sheet and an agent routing index.
content_id: "08965794d2b2c245"
tags: [reference, methodology-index, research-methods, cheat-sheet, routing]
---
# Methodologies Detail Reference

## Summary

**One-sentence:** A flat reference page bundling 20 research methodologies as a human-readable cheat sheet and an agent routing index.

**One-paragraph:** A flat reference page bundling 20 research methodologies as a human-readable cheat sheet and an agent routing index. Each entry lists framework keywords, scoring thresholds, and the agent mode that activates the canonical methodology folder under pro/research/researcher/, pro/research/market-researcher/, or pro/research/user-researcher/.

## Applies If (ALL must hold)

- Human wants a quick overview of all 20 research methodologies and their agent modes in one place
- Agent received an ambiguous research request and needs to map keywords to a mode before loading the canonical folder
- Generating a TOC, sidebar, or cross-reference for documentation
- Sanity-checking that a methodology exists in the suite before referencing it
- Composing a multi-method research plan (e.g. mode=ideas then mode=validate then mode=market)

## Skip If (ANY kills it)

- As the execution reference for any specific methodology — open the methodology's own folder for full content
- For prompt templates, full scoring rubrics, or agent integration code — those live in per-methodology files
- For mode routing inside an orchestrator at runtime — use the Research Modes table in the parent CLAUDE.md, not this page
- To copy abridged scoring thresholds into production decisions — always verify against the canonical methodology

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

- parent skill: `pro/research/researcher/`
