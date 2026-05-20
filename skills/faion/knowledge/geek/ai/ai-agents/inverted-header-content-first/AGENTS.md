---
slug: inverted-header-content-first
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When one structured-output call must produce both a long-form body and metadata about that body (title, slug, summary, tags, sentiment), declare the body field FIRST in the schema and every metadata field AFTER it.
content_id: "216c022a2cb673bd"
tags: [structured-output, schema-design, json, pydantic, quality]
---
# Inverted Header — Content First, Metadata Last

## Summary

**One-sentence:** When one structured-output call must produce both a long-form body and metadata about that body (title, slug, summary, tags, sentiment), declare the body field FIRST in the schema and every metadata field AFTER it.

**One-paragraph:** When one structured-output call must produce both a long-form body and metadata about that body (title, slug, summary, tags, sentiment), declare the body field FIRST in the schema and every metadata field AFTER it. The autoregressive model can only condition the title on tokens that already exist; if title is generated before body, the body is forced to fit a blind title; if body comes first, the title becomes a faithful summary of what was actually written.

## Applies If (ALL must hold)

- Article, blog post, email, social-media post generation in one SO call.
- Product description plus tags, slug, SEO title.
- Code generation followed by an explanation summary.
- Image caption with both long alt-text and short title.
- Any single-call output where short metadata fields summarize a long content field.

## Skip If (ANY kills it)

- The title is a hard input constraint provided by the user — pass it in the prompt, omit from schema.
- Streaming UI must show a title before the body finishes — split into two calls instead.
- Metadata is fully deterministic from the prompt (e.g., lang="en" from a known input) — order does not matter.
- The "metadata" field is in fact a routing decision the user already gave you — keep that out of generated output.

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
