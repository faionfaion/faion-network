---
slug: tool-call-schema-design-checklist
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Single 'design-this-tool-correctly' checklist linking the 7 detailed methodologies (verb-object-naming, description-as-prompt, bundle-vs-split, idempotent-write, structured-errors, enum-constraints, terse-default-output).
content_id: "036fa6c1e47dcbff"
tags: [tool-call-schema-design-checklist, ai, geek]
---

# Tool-Call Schema Design Checklist

## Summary

**One-sentence:** Single 'design-this-tool-correctly' checklist linking the 7 detailed methodologies (verb-object-naming, description-as-prompt, bundle-vs-split, idempotent-write, structured-errors, enum-constraints, terse-default-output).

**One-paragraph:** Scattered hints in verb-object-tool-naming, tool-description-as-prompt, bundle-vs-split-tools, idempotent-write-tools, structured-tool-errors, enum-constraints-closed-vocabularies, terse-default-tool-output. P7 needs a single checklist linking the 7. Output: schema-design checklist + per-axis decisions.

## Applies If (ALL must hold)

- designing a new tool/function for an LLM agent
- team has access to model providers' tool-call schemas
- agent uses the tool ≥10 times/day OR critical-path

## Skip If (ANY kills it)

- one-off prompt with no tool calls
- tool inherited from framework with no flexibility
- exploration phase with no production constraint

## Prerequisites

- tool's intended job statement (1 sentence)
- list of inputs + expected outputs
- existing tool list to check naming + bundle decisions

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/verb-object-tool-naming` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/tool-description-as-prompt` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `geek/ai/verb-object-tool-naming`
- peer methodology: `geek/ai/tool-description-as-prompt`
- peer methodology: `geek/ai/bundle-vs-split-tools`
- peer methodology: `geek/ai/idempotent-write-tools`
- peer methodology: `geek/ai/structured-tool-errors`
- peer methodology: `geek/ai/enum-constraints-closed-vocabularies`
- peer methodology: `geek/ai/terse-default-tool-output`
- external: https://www.anthropic.com/research/building-effective-agents; https://platform.openai.com/docs/guides/function-calling
