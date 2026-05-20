---
slug: prompt-engineering-production
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production prompts require versioning, retry logic, structured output validation, and tool-use scaffolding.
content_id: "3f555c8a3a1470b6"
tags: [prompt-engineering, production, function-calling, react, structured-output]
---
# Prompt Engineering — Production Patterns

## Summary

**One-sentence:** Production prompts require versioning, retry logic, structured output validation, and tool-use scaffolding.

**One-paragraph:** Production prompts require versioning, retry logic, structured output validation, and tool-use scaffolding. This methodology covers: prompt versioning in code, retry-with-escalation, the PromptTemplate and PromptManager classes, Pydantic-based structured output handling, ReAct agent scaffolding, function calling templates, and agentic workflow design patterns.

## Applies If (ALL must hold)

- Any LLM call in a production pipeline where reliability matters.
- Structured output use cases where the downstream system depends on schema correctness.
- Tool-use and agent architectures where the model selects and calls external functions.
- Multi-turn agentic workflows where intermediate prompts are generated programmatically.
- Pipelines where prompt changes must be reviewed via git diff and rolled back if needed.

## Skip If (ANY kills it)

- Exploratory one-off prompts — versioning overhead is not justified.
- Prompts that are user-authored at runtime — manage as user content, not code artifacts.

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

- parent skill: `geek/ai/ml-engineer/`
