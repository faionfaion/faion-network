# Tool Use and Function Calling

## Summary

Function calling enables LLMs to interact with external systems by generating structured JSON specifying which tool to call and with what parameters. The LLM does not execute functions — it produces the call specification; your code executes it. Keep the tool catalogue per call to ≤20; use RAG-over-tools to select the relevant subset for larger catalogues. Always validate LLM-generated arguments before execution.

## Why

Tool calling is the foundation of agentic AI systems. Without it, agents cannot fetch live data, write records, or trigger external workflows. The key risk is argument hallucination — the LLM invents plausible but wrong parameter values (e.g., wrong user IDs). Explicit parameter names and structured error returns mitigate this; raw string passing does not.

## When To Use

- Agent needs to fetch live data (weather, prices, user records) the LLM does not know
- Workflow requires state changes: writing files, sending messages, creating DB records
- Output must be structured JSON consumed downstream — tools enforce the schema
- Building multi-step agentic loops where each step depends on real execution results
- Connecting an LLM to internal APIs or microservices

## When NOT To Use

- Query is pure text reasoning with no external dependency (summarize, translate, brainstorm)
- Tool roundtrip latency is unacceptable and pre-fetched context would suffice
- LLM tool-selection accuracy is low (<70%) — use structured output or hardcoded routing instead
- Single, fully deterministic function is always called — skip LLM selection, call it directly

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts-and-providers.xml` | Function calling flow, tool choice modes, provider format differences (OpenAI/Claude/Gemini), agentic loop |
| `content/02-design-rules.xml` | Tool naming, parameter schema rules, error handling, security, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-dispatch.py` | Validated tool dispatcher with registry decorator and error return |
| `templates/tool-definitions.json` | Example tool definitions in OpenAI and Claude format |
