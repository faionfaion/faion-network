# Function Calling Patterns

## Summary

Production patterns for LLM tool use: parallel execution of independent tool calls, a tool router that dispatches queries to the correct tool subset, an agentic loop with bounded iteration count, and argument validation before execution. Covers both Anthropic (`tool_use` / `tool_result` blocks) and OpenAI (`tool_calls` in assistant message) formats.

## Why

LLMs hallucinate tool argument values and can enter infinite loops if no termination condition exists. Parallel tool execution masks ordering constraints for stateful operations. Returning raw large tool results inflates context rapidly. These patterns address each failure mode with concrete, testable implementations: schema validation before dispatch, `max_iterations` guard, result truncation, and structured error messages that let the model reason about next steps.

## When To Use

- Agent must take actions in external systems (APIs, databases, file system).
- Structured data extraction from unstructured text with guaranteed JSON schema.
- Orchestrating parallel I/O-bound tool calls to reduce latency.
- Building multi-step agentic loops where the LLM decides the next action.
- Replacing prompt-based output parsing with schema-enforced tool use.

## When NOT To Use

- Simple Q&A where no external action is needed — tool use adds tokens and latency.
- When all tools have side effects and the task is exploratory — use read-only tools first.
- More than ~20 tools in a single call — model selection accuracy degrades; use routing or subsets.
- Structured output purely for cosmetic formatting — prefer `response_format` or prefill.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-execution.xml` | Parallel executor, sequential executor, argument validation rules, result truncation rule. |
| `content/02-agentic-loop.xml` | Loop termination rules, max_iterations enforcement, error feedback format, stop_reason handling. |

## Templates

| File | Purpose |
|------|---------|
| `templates/parallel-executor.py` | Anthropic-format parallel tool executor with ThreadPoolExecutor and timeout. |
| `templates/tool-router.py` | ToolRouter class: register tools, get definitions, dispatch query. |
