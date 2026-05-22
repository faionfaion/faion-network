---
slug: ai-research-tools
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Stage-to-tool mapping for AI-augmented research pipelines with orchestrator pattern: Haiku for dispatch, Sonnet for synthesis, Opus for validation.
content_id: "e7431974126f3854"
tags: [research-tools, multi-stage-pipeline, agent-orchestration, source-attribution]
---
# AI Research Tools (geek/researcher)

## Summary

**One-sentence:** Stage-to-tool mapping for AI-augmented research pipelines with orchestrator pattern: Haiku for dispatch, Sonnet for synthesis, Opus for validation.

**One-paragraph:** Stage-to-tool mapping for AI-augmented research pipelines with orchestrator pattern: Haiku for dispatch, Sonnet for synthesis, Opus for validation.

## Applies If (ALL must hold)

- Building or instrumenting a multi-stage research pipeline for a geek/agent project
- Selecting the right tool before starting any structured literature or market sweep
- Producing synthesis reports from heterogeneous sources (news, academic, market data)
- Citation tracking and source verification is required

## Skip If (ANY kills it)

- Primary source collection requiring human judgment (expert interviews, observation)
- Legally sensitive research where AI hallucination risk is unacceptable
- Real-time data requiring live API access beyond what exposed tools support
- Tasks where source provenance must be court-admissible or regulatory-grade

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
