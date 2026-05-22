---
slug: multi-agent-orchestration-decision-tree
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: When single-agent + tools beats multi-agent, when hierarchical beats collaborative, when handoff-id-payload beats stream-json — the decision framework six 'multi-agent-*' entries lack.
content_id: "d82ec4a9394a3f98"
tags: [multi-agent-orchestration-decision-tree, ai, geek]
---

# Multi-Agent Orchestration Decision Tree

## Summary

**One-sentence:** When single-agent + tools beats multi-agent, when hierarchical beats collaborative, when handoff-id-payload beats stream-json — the decision framework six 'multi-agent-*' entries lack.

**One-paragraph:** multi-agent-basics/-collaborative/-conversational/-hierarchical/-production-bus/-design-patterns exist but P7 lacks the decision framework. Six methodologies, no chooser. Output: decision table + chosen pattern + revisit triggers.

## Applies If (ALL must hold)

- agent system with ≥2 specialized components OR planning need
- team considering multi-agent architecture
- eval set or production data to test against

## Skip If (ANY kills it)

- single-task agent with no orchestration need
- purely sequential pipeline with no agent autonomy
- research with no production constraint

## Prerequisites

- list of sub-tasks the system must handle
- eval set ≥30 representative cases
- infrastructure budget (multi-agent costs more)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/multi-agent-basics` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/multi-agent-collaborative` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `geek/ai/multi-agent-basics`
- peer methodology: `geek/ai/multi-agent-collaborative`
- peer methodology: `geek/ai/multi-agent-hierarchical`
- external: https://www.anthropic.com/research/building-effective-agents; https://arxiv.org/abs/2308.08155 (AutoGen)
