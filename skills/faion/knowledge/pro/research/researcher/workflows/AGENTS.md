---
slug: workflows
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Sequential research state machines for Idea Discovery, Product Research, and Project Naming.
content_id: "5855a9b1517a6537"
tags: [research, workflows, orchestration, sequential, idea-validation]
---
# Research Workflows

## Summary

**One-sentence:** Sequential research state machines for Idea Discovery, Product Research, and Project Naming.

**One-paragraph:** Sequential research state machines for Idea Discovery, Product Research, and Project Naming. Each workflow runs research agents one by one, writes outputs to .aidocs/product_docs/, and advances only after verifying non-empty output files.

## Applies If (ALL must hold)

- Pre-spec stage where market-research.md, competitive-analysis.md, or idea-validation.md are missing
- Solopreneur flow where an LLM acts as the entire research team
- Naming and domain validation before reserving a brand and writing constitution.md
- Refresh of stale research artifacts over 6 months old before a major roadmap revision

## Skip If (ANY kills it)

- Inside an active SDD task — research belongs in backlog discovery, not execution
- When the team has signed enterprise market data contracts (Gartner, IDC, Statista paid) — feed those reports directly to faion-sdd instead
- Tactical decisions inside a 30-minute window — sequential execution makes this multi-minute work
- After spec freeze — findings contradicting signed-off spec must go through change management

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
