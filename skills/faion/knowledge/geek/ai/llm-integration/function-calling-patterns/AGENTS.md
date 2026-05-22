---
slug: function-calling-patterns
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a cross-vendor function-calling design — parallel tool dispatch, tool router, agentic loop with bounded iterations, argument validation, schema-enforced output extraction.
content_id: "927ab42d24484c9c"
complexity: medium
produces: code
est_tokens: 3800
tags: [function-calling, tool-use, agent-loop, schema-validation, cross-vendor]
---
# Function Calling Patterns

## Summary

**One-sentence:** Produces a cross-vendor function-calling design — parallel tool dispatch, tool router, agentic loop with bounded iterations, argument validation, schema-enforced output extraction.

**One-paragraph:** Function calling is the canonical mechanism for letting an LLM take actions in external systems. Production patterns generalise across Anthropic (`tool_use`/`tool_result` blocks) and OpenAI (`tool_calls` in assistant message): keep individual tool count ≤20 per request and use a tool router when more exist; validate arguments against the JSON Schema BEFORE execution; cap the agent loop at 10-20 iterations; execute parallel tool_use blocks concurrently; return errors as content for recoverable failures so the model can self-correct. Prefer this pattern over prompt-based JSON parsing for any task where schema correctness matters.

**Ефективно для:** agents calling APIs/DB/filesystem, structured-output extraction, parallel I/O dispatch, multi-step agentic plans, vendor-portable AI features.

## Applies If (ALL must hold)

- Agent must take ≥1 action in an external system OR produce schema-validated structured output.
- Tool count is finite and enumerable (not dynamic per-request).
- Caller can store conversation state across turns.
- Either Anthropic or OpenAI SDK is the integration target.

## Skip If (ANY kills it)

- Pure Q&A with no external action and no schema needs.
- Streaming-first UX where every token must surface immediately.
- Tool set is dynamic and changes per request — invest in a registry first.
- Specifically Claude — use `[[claude-tool-use]]` for the Claude-specific shape.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tool registry | JSON Schema per tool | application code |
| Vendor SDK keys | secrets | env / secrets manager |
| Argument validator | jsonschema or pydantic | dependencies |
| Conversation store | dict / DB | session layer |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[claude-tool-use]]` | Claude-specific subset. |
| `[[guardrails-implementation]]` | Output guardrails layer on top of tool returns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 rules: ≤20 tools, validate args before exec, bounded loop, parallel dispatch, errors-as-content, single-vendor format per call, schema-versioned tools | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for tool registry entry + agent-loop trace | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: 50-tool dump, no arg validation, sequential dispatch, infinite loop, vendor mixing, schema-versionless | ~700 |
| `content/04-procedure.xml` | medium | 6-step: design tools → wire validator → write router → write loop → handle errors → eval | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "vendor in {Anthropic, OpenAI} AND ≥1 tool call?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Author tool schemas | sonnet | Mechanical from API specs. |
| Implement router | sonnet | Pattern code. |
| Write agent loop | sonnet | Recipe code. |
| Debug tool-call error | opus | Multi-step reasoning. |

## Templates

| File | Purpose |
|---|---|
| `templates/tool-registry.schema.json` | JSON Schema for one registry entry. |
| `templates/agent-loop.py` | Cross-vendor reference loop (dispatch via adapter). |
| `templates/argument-validator.py` | Pre-execution arg validator using jsonschema. |
| `templates/tool-router.py` | Two-stage router: category selection → tool dispatch. |
| `templates/_smoke-test.json` | Minimum valid tool registry entry. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-function-calling-patterns.py` | Validates tool-registry entries against schema; asserts each tool has version + schema. | Pre-commit on registry files. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[claude-tool-use]]`
- `[[gemini-function-calling]]`
- `[[guardrails-implementation]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` selects scope: Claude-only → use `[[claude-tool-use]]`; Gemini-only → `[[gemini-function-calling]]`; cross-vendor or OpenAI → run this methodology.
