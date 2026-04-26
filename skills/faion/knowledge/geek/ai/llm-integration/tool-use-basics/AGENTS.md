# Tool Use Basics

## Summary

Enables LLMs to call external functions, APIs, and code by defining a tool registry (name → callable), converting it to provider-specific JSON schema, and running a request-execute-respond loop with a hard iteration cap. Covers OpenAI function calling and Anthropic tool use patterns.

## Why

LLMs hallucinate when performing real-time lookups, precise calculations, or stateful operations. Tool use grounds responses in authoritative external data and enables autonomous multi-step workflows. Description quality is the #1 reliability lever — vague descriptions cause wrong tool selection even with correct implementations.

## When To Use

- Accessing real-time or external data (weather, stocks, database records, web search)
- Precise computation required (math, date arithmetic, aggregation) where LLMs hallucinate
- Autonomous agents taking actions (file writes, API calls, messages) in multi-step workflows
- ReAct-style (Reason + Act) loops where the model iterates until a goal is achieved

## When NOT To Use

- Task solvable with a single in-context prompt — tool calling adds latency and complexity
- All required information is already in the prompt context
- Destructive tools (delete, send emails, charge money) with no human approval gate
- Small/fast models (Haiku, gpt-4o-mini) with complex schemas (>5 tools, nested params) — selection accuracy degrades

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-loop.xml` | Request-execute-respond loop pattern, iteration cap rule, provider schema differences |
| `content/02-tool-design.xml` | Tool definition quality rules, error handling, security (sandbox, destructive tool gates) |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-loop.py` | Iteration-capped tool loop for OpenAI (≤35 lines) |
| `templates/tool-definition.json` | JSON schema template for a single tool definition |
