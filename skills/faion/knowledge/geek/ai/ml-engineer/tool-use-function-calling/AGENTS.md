---
slug: tool-use-function-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "231043d936033385"
summary: Designs a tool-using LLM workflow — declare typed tool schemas, dispatch model JSON to real functions, validate args, sandbox dangerous tools, and gate irreversible actions behind human review.
complexity: medium
produces: code
est_tokens: 3600
tags: [function-calling, tool-use, agents, structured-output, openai, claude, gemini]
---

# Tool Use and Function Calling

## Summary

**One-sentence:** Ship a tool-using LLM by declaring typed tool schemas (OpenAI tools, Anthropic tool_use, Gemini function_call), validating model-emitted args, dispatching to real functions, and gating side-effecting tools behind a human-review or scoped-permission layer.

**One-paragraph:** Tool-use lets an LLM call code paths (DB queries, API requests, file writes) via structured `{tool_name, args}` JSON. The contract: declare each tool with a strict JSON Schema, register the dispatcher, validate args before execution (LLMs hallucinate plausible-but-wrong args), separate `read-only` from `side-effecting` tools, gate irreversible side effects behind a human review. Production additions: tool-use eval (does the model pick the right tool?), rate-limit per tool, audit log of every call. Output: a typed dispatcher module + a `tools.yaml` manifest.

**Ефективно для:**

- Agent flows які мають викликати external APIs (CRM, email, calendar) — typed tools уникають парс-помилок і дають audit trail.
- RAG із search tools — model сам вирішує коли робити retrieval і з яким filter.
- Code-execution loops — sandbox tool + human gate на повзучі дії.
- Multi-step planning — tool-call sequence показує план у diff-ready форматі.

## Applies If (ALL must hold)

- LLM provider supports native tool use (OpenAI, Anthropic, Gemini, Mistral)
- ≥2 distinct functions the LLM should choose between
- Argument validation possible (each tool has a defined schema)
- Side-effecting tools have a kill-switch / rollback path

## Skip If (ANY kills it)

- Only one possible action — direct call is simpler than tool indirection
- Tool args are fully free-form text — structured output (not tool use) is the right primitive
- No audit / observability infrastructure — tool calls without logs are unauditable

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `tools.yaml` | YAML | tool catalog with schema + safety class per tool |
| `dispatcher.py` | Python | maps tool name → callable |
| `audit-sink.yaml` | YAML | log destination (DB / file / S3) |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `structured-output` | Sibling pattern; tool_use is constrained decoding |
| `reasoning-first-architectures` | Reasoning models often gate tool decisions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typed schema, validate-before-execute, side-effect class, human gate on irreversible, audit every call | 1100 |
| `content/02-output-contract.xml` | essential | `tools.yaml` schema | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: free-form args, no sandbox, hallucinated tool name, infinite tool loop, no audit | 900 |
| `content/04-procedure.xml` | essential | 5 steps: catalog → schema → dispatch+validate → safety class → ship+audit | 700 |
| `content/05-examples.xml` | essential | Worked example: support agent with `lookup_customer`, `send_email`, `escalate_to_human` | 500 |
| `content/06-decision-tree.xml` | essential | Routes by side-effect class to safe-execute / human-gated / refuse | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tool_choice_at_scale` | sonnet | Pick which tool to call; bounded judgement |
| `tool_arg_synthesis` | sonnet | Compose args; constrained decoding |
| `tools_yaml_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/tool-definitions.json` | OpenAI tools array example |
| `templates/tool-dispatch.py` | Dispatcher with validate-before-execute + audit |
| `templates/tools.schema.yaml` | Schema for tools.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable tools.yaml |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-use-function-calling.py` | Lint tools.yaml | Pre-commit |

## Related

- [[structured-output]] — same primitive
- [[reasoning-first-architectures]] — reasoning models often gate tool decisions
- external: [OpenAI tool use](https://platform.openai.com/docs/guides/function-calling) · [Anthropic tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) · [MCP](https://modelcontextprotocol.io/)

## Decision tree

See `content/06-decision-tree.xml`. Routes by side-effect class (read-only / mutating / destructive) to safe-execute / human-gated / refuse.
