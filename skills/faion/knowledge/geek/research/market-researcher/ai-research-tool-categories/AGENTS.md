---
slug: ai-research-tool-categories
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A phase-to-tool classification for AI research pipelines: map each research task to its phase (exploration, competitor intel, interview analysis, survey, sentiment, synthesis, synthetic research), then select the appropriate tool from the approved category map.
content_id: "d557e075aba85165"
tags: [research, tool-selection, ai-research, market-analysis, agent-workflow]
---
# AI Research Tool Categories

## Summary

**One-sentence:** A phase-to-tool classification for AI research pipelines: map each research task to its phase (exploration, competitor intel, interview analysis, survey, sentiment, synthesis, synthetic research), then select the appropriate tool from the approved category map.

**One-paragraph:** A phase-to-tool classification for AI research pipelines: map each research task to its phase (exploration, competitor intel, interview analysis, survey, sentiment, synthesis, synthetic research), then select the appropriate tool from the approved category map. Lock tool selection per project at planning time, not per query.

## Applies If (ALL must hold)

- Selecting the right research tool before starting a multi-stage project
- Building a reusable tool-selection decision tree for recurring research workflows
- Auditing an existing research stack against coverage gaps by phase
- Onboarding a new agent to a research pipeline by mapping tasks to approved tools

## Skip If (ANY kills it)

- When you already know the tool for the job — skip categorization overhead
- When the research budget is fixed and only one or two tools are available
- During execution of an already-designed pipeline — this methodology is for planning, not running
- When tool categories are stable and budget is locked — most valuable at procurement / pipeline design time

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
