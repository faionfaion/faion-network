---
slug: tool-description-as-prompt
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A tool's description field is part of the prompt the model sees on every turn.
content_id: "beb199d91245264f"
tags: [tool-use, prompting, agents, evaluation]
---
# Tool Description as Prompt

## Summary

**One-sentence:** A tool's description field is part of the prompt the model sees on every turn.

**One-paragraph:** A tool's description field is part of the prompt the model sees on every turn. Treat tool descriptions as zero-shot teaching: state when to call this tool, what inputs are required, what output to expect, and when NOT to call it. Tool description quality moves benchmark scores more than swapping the model.

## Applies If (ALL must hold)

- Always. But most teams under-invest in tool descriptions. The bar is: write your tool descriptions as if they were the system prompt of a junior engineer being asked to use this for the first time.

## Skip If (ANY kills it)

- Skipping tool descriptions altogether (very common and very wrong)
- Copying the function docstring verbatim — function docs target humans, tool descriptions target the LLM. Different audiences, different priorities.
- Tool descriptions that contradict the input_schema (e.g., describing pagination but no page parameter exists)

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

- parent skill: `geek/ai/ai-agents/`
