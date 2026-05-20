---
slug: multi-agent-conversational
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Agents take sequential turns in a free-form conversation.
content_id: "21f04674d277377f"
tags: [multi-agent, conversational, autogen, turn-taking, termination]
---
# AutoGen-Style Conversational Multi-Agent Pattern

## Summary

**One-sentence:** Agents take sequential turns in a free-form conversation.

**One-paragraph:** Agents take sequential turns in a free-form conversation. Each agent receives a sliding window of recent conversation context and the last message, produces a response, and the conversation continues until either a termination phrase appears in the output or the max-turn cap is reached. The pattern follows the AutoGen conversation model where agents dynamically negotiate the approach rather than following a pre-defined plan.

## Applies If (ALL must hold)

- Dynamic tasks where the approach cannot be decomposed upfront: interactive debugging, negotiation, Socratic questioning.
- Adversarial verification: one agent proposes, another critiques, the conversation converges on a validated answer.
- Open-ended exploration where the conversation path itself is the output: design whiteboarding, brainstorming under constraints.
- Scenarios where agents need to negotiate a shared understanding before acting — the conversation is the planning step.

## Skip If (ANY kills it)

- Tasks with a known sequential pipeline — hierarchical or sequential execution is simpler and cheaper.
- Production systems requiring auditability of every decision: conversational turn logs are harder to parse than structured assignment logs.
- Tight latency budgets: free-form conversations have no natural early exit except the termination phrase; worst case = max_turns LLM calls.
- Tasks where agents need a shared mutable state beyond the conversation history — the only inter-agent channel here is message content.

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
