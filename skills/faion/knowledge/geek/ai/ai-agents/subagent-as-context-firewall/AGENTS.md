---
slug: subagent-as-context-firewall
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use subagents as isolated context windows for heavy work, with strict output contracts returning only slim summaries and references.
content_id: "f7d182c070b854c4"
tags: [subagents, context-management, memory, architecture]
---
# Subagent as Context Firewall

## Summary

**One-sentence:** Use subagents as isolated context windows for heavy work, with strict output contracts returning only slim summaries and references.

**One-paragraph:** Use subagents as isolated context windows for heavy work, with strict output contracts returning only slim summaries and references. The parent's context grows minimally regardless of how much the subagent processes internally.

## Applies If (ALL must hold)

- Heavy reading: scanning many files, summarizing a corpus, exploring a codebase
- Task that needs many tool calls but produces a small answer
- Anywhere the process of finding the answer is much heavier than the answer itself
- Speculative branches: send a subagent to try approach A; main keeps approach B alive
- Untrusted content: subagent reads attacker-controlled doc, returns sanitized summary

## Skip If (ANY kills it)

- When the parent needs the FULL details of what the subagent saw defeats the firewall
- When the work is small enough that main can do it directly 1-2 file reads
- When subagent latency matters subagents add round-trip overhead
- For TRUE parallelism gains that is a different pattern multiple subagents in parallel, each firewalled

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
