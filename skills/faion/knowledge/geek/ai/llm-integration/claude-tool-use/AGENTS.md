---
slug: claude-tool-use
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a working Claude tool-use loop — typed JSON Schema tool definitions, canonical agent loop with parallel tool dispatch, forced-tool structured output, max-iteration guard.
content_id: "0a55c5dba8f761d5"
complexity: medium
produces: code
est_tokens: 4200
tags: [claude, tool-use, function-calling, agent-loop, mcp]
---
# Claude Tool Use

## Summary

**One-sentence:** Produces a working Claude tool-use loop — typed JSON Schema tool definitions, canonical agent loop with parallel tool dispatch, forced-tool structured output, max-iteration guard.

**One-paragraph:** Claude tool use (function calling) is the canonical mechanism for letting Claude call external APIs, databases, and search. The reliable shape: define tools with explicit JSON Schema `input_schema`; detect `stop_reason == "tool_use"` and continue the loop; append the full `response.content` list (text + tool_use blocks) as the assistant turn so conversation history stays parseable; cap iterations at 10-20 to avoid runaways; execute parallel tool_use blocks concurrently and return all results in one user message; use `tool_choice={"type":"tool","name":"X"}` to force typed structured output via the tool-use pathway. MCP exists for Claude Desktop (stdio) — programmatic API users should stay on standard tool use.

**Ефективно для:** agents fetching live data, structured-output extraction, parallel API dispatch, code-execution wrappers, function-call routing.

## Applies If (ALL must hold)

- Claude API is the model under integration (Anthropic SDK).
- Agent needs to call ≥1 external function and incorporate the result.
- Caller can store conversation history and re-send it on each turn.
- A max-iteration cap is acceptable (no genuinely unbounded loops needed).

## Skip If (ANY kills it)

- Pure text completion with no external data.
- Using OpenAI / Gemini SDK — refer to `[[function-calling-patterns]]` or `[[gemini-function-calling]]`.
- Streaming-only UX where the loop cannot wait for `stop_reason`.
- &gt;20 tools — Claude routinely picks wrong; route via a meta-tool selector first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool list with schemas | JSON | tools registry / `tools.json` |
| Anthropic API key | secret | env var `ANTHROPIC_API_KEY` |
| Tool executor function | callable | application code |
| System prompt | string | prompt repo |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[function-calling-patterns]]` | Cross-vendor patterns context. |
| `[[guardrails-implementation]]` | Output guardrails apply to tool-call results. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 8 testable rules: schema flatness, stop_reason check, max-turns, append full content, parallel exec, errors-as-content, force-tool for typed output, MCP scope | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for a tool definition + agent-loop trace format | ~700 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns: deep nesting, append-text-only, blind indexing, infinite loop, strict additionalProperties, MCP-in-server, thinking-blocks-in-tool_result | ~800 |
| `content/04-procedure.xml` | medium | 6-step procedure: design tool schemas → write executor → write agent loop → set max-turns → handle errors → add forced-tool extraction | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "is the model Claude AND ≥1 tool call required?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Write tool schema from spec | sonnet | Mechanical mapping. |
| Implement executor | sonnet | Bounded code generation. |
| Run loop and tool calls | runtime | (not an LLM task) |
| Triage tool-call error | opus | Multi-block reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/tool-definition.json` | One tool definition with JSON Schema input_schema. |
| `templates/agent-loop.py` | Reference Python agent loop with parallel tool dispatch + max-turns guard. |
| `templates/forced-tool-extract.py` | tool_choice extraction pattern for typed JSON output. |
| `templates/_smoke-test.json` | Minimum-valid tool definition for the validator. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-claude-tool-use.py` | Validates tool-definition JSON Schema (flat, additionalProperties allowed, required arrays correct). | Pre-commit on tool definitions. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[function-calling-patterns]]`
- `[[gemini-function-calling]]`
- `[[guardrails-implementation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether to use this Claude-specific pattern: non-Claude models route to `[[function-calling-patterns]]` or vendor-specific siblings; streaming-only UX → use streaming response API directly; ≤1 tool call → bypass the loop and call directly.
