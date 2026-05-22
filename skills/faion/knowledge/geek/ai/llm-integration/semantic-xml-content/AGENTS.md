---
slug: semantic-xml-content
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A convention for authoring methodology content as semantic XML — not as XML for formatting, but as a tag vocabulary where each tag carries meaning the agent can act on.
content_id: "1025869626d4c73e"
tags: [xml, semantic, agents, content]
---
# Semantic XML Content for Agents

## Summary

**One-sentence:** A convention for authoring methodology content as semantic XML — not as XML for formatting, but as a tag vocabulary where each tag carries meaning the agent can act on.

**One-paragraph:** A convention for authoring methodology content as semantic XML — not as XML for formatting, but as a tag vocabulary where each tag carries meaning the agent can act on. Replaces free-form Markdown ...

## Applies If (ALL must hold)

- Authoring content/*.xml
- Writing agent-facing docs
- Migrating Markdown
- Tool-use prompts

## Skip If (ANY kills it)

- Routing docs
- Human READMEs
- Code files
- One-off prompts

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

- parent skill: `geek/ai/llm-integration/`
