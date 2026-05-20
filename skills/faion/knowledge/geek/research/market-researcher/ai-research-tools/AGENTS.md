---
slug: ai-research-tools
tier: geek
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A two-layer agent structure for AI-driven market research pipelines: an orchestrator (Sonnet) selects the right tool for each research stage based on task type and available credentials, then dispatches sub-queries to stage-specific tools.
content_id: "e7431974126f3854"
tags: [research, pipeline, ai-tools, orchestration, multi-stage]
---
# AI Research Tools

## Summary

**One-sentence:** A two-layer agent structure for AI-driven market research pipelines: an orchestrator (Sonnet) selects the right tool for each research stage based on task type and available credentials, then dispatches sub-queries to stage-specific tools.

**One-paragraph:** A two-layer agent structure for AI-driven market research pipelines: an orchestrator (Sonnet) selects the right tool for each research stage based on task type and available credentials, then dispatches sub-queries to stage-specific tools. The orchestrator merges outputs, flags gaps where no tool produced coverage, and signals a human checkpoint before synthesis. Each stage gets exactly one primary tool.

## Applies If (ALL must hold)

- Building or auditing the tool stack for a market research pipeline
- Deciding which AI tool handles which stage of a multi-step project
- Replacing manual research workflows with agent-driven equivalents
- Onboarding a new agent to an existing research pipeline

## Skip If (ANY kills it)

- When a single tool already covers the full research scope
- Proprietary or regulated research contexts requiring auditable, non-AI sources
- When the research team lacks API credentials for candidate tools
- One-off ad hoc queries where tool overhead exceeds research value

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

- parent skill: `geek/research/market-researcher/`
