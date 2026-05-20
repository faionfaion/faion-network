---
slug: terse-default-tool-output
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Tools default to compact, semantic output (one-line summary, Markdown table of IDs, count + top-N) and accept an explicit format or verbosity parameter so the agent can opt into raw/full payloads only when reasoning needs the detail.
content_id: "8feb439b098c5147"
tags: [tool-design, output-format, context-efficiency, agent-loops]
---
# Terse Default Tool Output, Verbosity Opt-In

## Summary

**One-sentence:** Tools default to compact, semantic output (one-line summary, Markdown table of IDs, count + top-N) and accept an explicit format or verbosity parameter so the agent can opt into raw/full payloads only when reasoning needs the detail.

**One-paragraph:** Tools default to compact, semantic output (one-line summary, Markdown table of IDs, count + top-N) and accept an explicit format or verbosity parameter so the agent can opt into raw/full payloads only when reasoning needs the detail. Verbose-by-default tool outputs are the most common cause of context blowup in long agent loops — they bury the signal the model actually uses for the next step. SkillReducer reported 48% description / 39% body compression IMPROVED downstream task quality by 2.8% — verbose context is distraction, not help.

## Applies If (ALL must hold)

- Any tool that can return more than ~500 tokens at the upper bound: list_*, search_*, query_*, log queries, file listings, DB selects.
- Tools chained inside a long-running agent loop where context budget is finite.
- Tools whose output the model uses to plan a next action (only IDs + a hint matter).

## Skip If (ANY kills it)

- Tools whose every field is load-bearing for the agent's reasoning (e.g., get_payment_invoice for an audit task) — terseness drops audit-critical data.
- Tools that return small, fixed-shape responses (get_user(id) returning 5 fields) — adding a verbosity knob is overhead with no win.
- Final-result tools at the end of the loop where the user wants the full answer.

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
