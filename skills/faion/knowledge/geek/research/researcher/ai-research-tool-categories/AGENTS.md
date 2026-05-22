---
slug: ai-research-tool-categories
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A phase-and-budget decision map for selecting research tools across seven categories: exploration, competitor intel, user interviews, survey analysis, sentiment, synthesis, and synthetic research.
content_id: "d557e075aba85165"
tags: [research-tools, decision-tree, budget-tiers, agent-workflow]
---
# AI Research Tool Categories

## Summary

**One-sentence:** A phase-and-budget decision map for selecting research tools across seven categories: exploration, competitor intel, user interviews, survey analysis, sentiment, synthesis, and synthetic research.

**One-paragraph:** A phase-and-budget decision map for selecting research tools across seven categories: exploration, competitor intel, user interviews, survey analysis, sentiment, synthesis, and synthetic research. Agents use this map as a decision tree; given phase and budget, they output a stack recommendation with API availability flags.

## Applies If (ALL must hold)

- Planning a research stack at the start of a new project or research sprint.
- Selecting tools for a specific research phase (discovery → synthesis → validation).
- Budget-scoping a research operation (free vs. mid vs. enterprise).
- Choosing the right tool per research question type before committing to a SaaS contract.

## Skip If (ANY kills it)

- As a substitute for evaluating data privacy requirements — always check data processing agreements.
- When the question is fully addressable with a single tool already in use — avoid tool sprawl.
- For purely qualitative synthesis where Claude alone suffices — no additional tooling needed.

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
