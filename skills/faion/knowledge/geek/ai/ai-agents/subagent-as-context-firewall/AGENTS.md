---
slug: subagent-as-context-firewall
tier: geek
group: ai
domain: ai-agents
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an isolated subagent invocation with a Pydantic output contract returning only a slim summary + refs, so the parent's context grows minimally regardless of the subagent's internal token spend.
content_id: "3661ffa7c1847ecd"
complexity: medium
produces: spec
est_tokens: 3900
tags: [subagents, context-management, memory, architecture]
---
# Subagent as Context Firewall

## Summary

**One-sentence:** Push heavy reading and untrusted input into a subagent and only return a strict slim summary — the parent's context never sees the 100K tokens of evidence.

**One-paragraph:** Produces a subagent invocation (Claude Code Task, Claude Agent SDK, LangGraph subgraph) with a Pydantic / JSON-Schema output contract whose top-level fields are `summary` (≤200 tokens), `refs` (file paths / URLs the parent can pull on demand), `confidence`, and `next_actions`. The subagent does the heavy reading internally; the parent receives the contract output and proceeds. Same pattern is the mandatory wrapper for untrusted input (attacker-controlled docs) because the subagent's prompt-injection blast radius stays inside its own window.

**Ефективно для:** будь-якої задачі, де процес пошуку відповіді набагато важчий за саму відповідь — read corpus / explore codebase / summarize 30 files / parse untrusted doc — і де основний context не повинен платити за весь шлях.

## Applies If (ALL must hold)

- The task needs many tool calls / file reads / heavy reading to produce a small answer.
- The parent context is or will be reused across many turns (every token costs every turn).
- The subagent can express its answer in ≤500 tokens of summary + a list of refs.
- The work is reproducible (parent can re-fetch refs if it needs full detail).

## Skip If (ANY kills it)

- The parent genuinely needs the full evidence pasted into its context (defeats the firewall).
- The work is small enough that 1-2 direct tool calls cost less than the subagent overhead.
- Latency budget cannot absorb a subagent round-trip.
- For TRUE parallelism gains see [[ai-agents/handoff-id-payload]] instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | one paragraph | parent agent prompt |
| Output Pydantic contract | `BaseModel` subclass | `subagent_contracts.py` |
| Allowed tools list | comma-separated | risk-assessment |
| Token budget for the subagent | int | parent runner config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/stream-json-orchestration` | Subagent streams events back; firewall pattern relies on the orchestrator. |
| `geek/ai/ai-agents/semantic-field-naming` | Contract field names matter; rename before shipping. |
| `geek/ai/ai-agents/strict-mode-required-fields` | Output contract must pass strict mode. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: slim contract mandatory, refs over content, fresh window per invoke, untrusted-input wrapping, parent never sees raw subagent thinking | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the slim subagent return: summary ≤200 tokens, refs[], confidence, next_actions[] | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: leaky summary (pastes evidence), no contract (free-form), parent re-reads same files, untrusted input bypassing subagent, nested firewall stack | ~700 |
| `content/04-procedure.xml` | medium | Migrate a heavy task to a firewalled subagent: name the contract → set token budget → invoke → consume | ~700 |
| `content/05-examples.xml` | medium | Bug hunt in 30-file codebase, untrusted doc summarisation, speculative-branch fan-out | ~500 |
| `content/06-decision-tree.xml` | essential | Picks subagent shape from heaviness × trust × parallelism | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Define the slim output contract | opus | Modeling judgement on what the parent needs. |
| Run the subagent itself | sonnet / haiku | Heavy mechanical reading; smaller model is fine inside the firewall. |
| Parent-side consume + dispatch | opus | Strategic decisions on what to do with refs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/claude-agent-sdk.py` | Subagent invocation via Anthropic Claude Agent SDK with `tool_choice` + Pydantic output. |
| `templates/claude-code-task-tool.py` | Claude Code Task-tool invocation pattern returning slim contract. |
| `templates/langgraph-subgraph.py` | LangGraph subgraph with isolated `State` and slim parent-facing output. |
| `templates/parallel-firewalled.py` | Fan-out N subagents; each firewalled; parent gathers final summaries only. |
| `templates/pydantic-contract.py` | Reference Pydantic contract for the firewall output shape. |
| `templates/untrusted-input.py` | Wrapper for attacker-controlled input — never reaches parent context. |
| `templates/failure-mode.py` | Reference anti-example: a leaky subagent that pastes evidence into the parent. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-subagent-as-context-firewall.py` | Validates a subagent return JSON against `02-output-contract.xml`. | After each subagent call, before returning to the parent reasoner. |

## Related

- [[stream-json-orchestration]] — per-subagent stream is the underlying pipe.
- [[handoff-id-payload]] — when the parent needs to hand off, not just summarise.
- [[file-reference-passing]] — refs over content is the same pattern at the tool-result layer.
- [[strict-mode-required-fields]] — contract must pass strict mode.

## Decision tree

The tree at `content/06-decision-tree.xml` picks the firewall shape from three observables: token cost of the underlying work, trust level of the input (trusted / untrusted), and parallelism (single vs fan-out). Heavy + trusted → single subagent + slim contract; heavy + untrusted → subagent + extra sanitisation + no tool execution; many independent branches → parallel firewalled fan-out via asyncio.gather.
