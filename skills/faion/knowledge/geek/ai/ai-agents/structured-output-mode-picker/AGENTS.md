# Structured Output Mode — JSON-Mode vs SO vs Tool-Call vs Grammar

## Summary

Four constrained-decoding modes ship in 2026 SDKs and they are NOT interchangeable. JSON mode guarantees only valid JSON; Structured Outputs (`response_format: json_schema, strict: true`) guarantees full schema compliance; tool calls guarantee schema-compliant arguments and dispatch to a function; grammar-mode (XGrammar / Outlines / GBNF) constrains generation to any context-free grammar including non-JSON DSLs. Picking by use case — extraction → SO, action → tool call, custom DSL/SQL → grammar, legacy fallback → json mode — saves tokens and prevents silent constraint violations.

## Why

JSON mode in 2024 was the only constrained option, so codebases defaulted to it for everything. By 2026 every major provider ships strict SO, native tool calls, and (for local models) full grammar libraries. Using `json_object` mode for a task that needs a schema produces valid-but-wrong outputs that pass `json.loads()` and fail downstream typing; using SO for an action-dispatch task wastes the routing affordance the tool-call ecosystem already provides; using tool calls for a SQL DSL forces a JSON detour. The match between mode and use case is now the single biggest correctness lever in SO design.

## When To Use

- Choosing constrained decoding for a new agent or pipeline stage
- Migrating a legacy `response_format={"type": "json_object"}` codebase
- Adding a constrained-output step on a local open-source model (vLLM/Ollama)
- Designing an agent that mixes data extraction and action dispatch in one loop

## When NOT To Use

- Free-form chat where structure is undesirable — keep plain text
- One-off scripts where downstream parsing tolerates failure — `json_object` is acceptable
- Pure transformation tasks fully solved by regex / deterministic code — skip the LLM
- When the chosen provider does not support the mode you picked — fall back to closest peer

## Content

| File | What's inside |
|------|---------------|
| `content/01-mode-picker.xml` | Decision rule mapping use case → mode with empirical anchor and mode-comparison table. |
| `content/02-anti-patterns.xml` | Common misuses: json-mode for typed extraction, SO for action dispatch, tool calls for DSLs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mode_examples.py` | One minimal call per mode (json-mode, SO, tool-call, grammar) for side-by-side comparison. |

## References

- [JSON Mode vs Function Calling vs Structured Output: 2026 Guide — BuildMVPFast](https://www.buildmvpfast.com/blog/structured-output-llm-json-mode-function-calling-production-guide-2026)
- [When should I use function calling, structured outputs or JSON mode? — Vellum](https://www.vellum.ai/blog/when-should-i-use-function-calling-structured-outputs-or-json-mode)
- [XGrammar — Flexible and Efficient Structured Generation](https://arxiv.org/abs/2411.15100)
