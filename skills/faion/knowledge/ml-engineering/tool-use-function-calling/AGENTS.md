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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tool-definitions.json`

```json
{
  "_header": [
    "purpose: tool definitions in OpenAI tools[] + Anthropic tool_use formats",
    "consumes: tool-author intent",
    "produces: config (provider-specific tools array)",
    "depends-on: provider SDK (OpenAI v1.40+ OR Anthropic v0.30+)",
    "token-budget-impact: ~200 tokens loaded into provider call per request"
  ],
  "_comment": "Example tool definitions in OpenAI and Claude formats. Replace properties schemas with real parameter definitions.",
  "openai_format": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a location. Use when the user asks about weather, temperature, or forecast.",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City and country, e.g. 'Tokyo, Japan' or 'Paris, France'"
            },
            "unit": {
              "type": "string",
              "enum": [
                "celsius",
                "fahrenheit"
              ],
              "description": "Temperature unit. Default: celsius"
            }
          },
          "required": [
            "location"
          ],
          "additionalProperties": false
        },
        "strict": true
      }
    },
    {
      "type": "function",
      "function": {
        "name": "search_knowledge_base",
        "description": "Search internal knowledge base for information. Use when user asks factual questions not answerable from context.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Natural language search query"
            },
            "limit": {
              "type": "integer",
              "description": "Maximum number of results to return. Default: 5, max: 20",
              "minimum": 1,
              "maximum": 20
            },
            "category": {
              "type": "string",
              "enum": [
                "docs",
                "faq",
                "policies",
                "products"
              ],
              "description": "Optional category filter"
            }
          },
          "required": [
            "query"
          ],
          "additionalProperties": false
        },
        "strict": true
      }
    },
    {
      "type": "function",
      "function": {
        "name": "create_ticket",
        "description": "Create a support ticket. Use when user reports a problem that needs human follow-up.",
        "parameters": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string",
              "description": "Short ticket title, max 100 characters"
            },
            "description": {
              "type": "string",
              "description": "Detailed description of the issue"
            },
            "priority": {
              "type": "string",
              "enum": [
                "low",
                "medium",
                "high",
                "critical"
              ],
              "description": "Ticket priority: low=cosmetic, medium=degraded, high=blocked, critical=down"
            },
            "user_email": {
              "type": "string",
              "description": "Requester email address"
            }
          },
          "required": [
            "title",
            "description",
            "priority",
            "user_email"
          ],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  ],
  "claude_format": [
    {
      "name": "get_weather",
      "description": "Get current weather for a location. Use when the user asks about weather, temperature, or forecast.",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City and country, e.g. 'Tokyo, Japan' or 'Paris, France'"
          },
          "unit": {
            "type": "string",
            "enum": [
              "celsius",
              "fahrenheit"
            ],
            "description": "Temperature unit. Default: celsius"
          }
        },
        "required": [
          "location"
        ]
      }
    },
    {
      "name": "search_knowledge_base",
      "description": "Search internal knowledge base for information. Use when user asks factual questions not answerable from context.",
      "input_schema": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Natural language search query"
          },
          "limit": {
            "type": "integer",
            "description": "Maximum results. Default: 5, max: 20"
          },
          "category": {
            "type": "string",
            "enum": [
              "docs",
              "faq",
              "policies",
              "products"
            ],
            "description": "Optional category filter"
          }
        },
        "required": [
          "query"
        ]
      }
    },
    {
      "name": "create_ticket",
      "description": "Create a support ticket. Use when user reports a problem that needs human follow-up.",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "description": "Short ticket title, max 100 characters"
          },
          "description": {
            "type": "string",
            "description": "Detailed description of the issue"
          },
          "priority": {
            "type": "string",
            "enum": [
              "low",
              "medium",
              "high",
              "critical"
            ],
            "description": "low=cosmetic, medium=degraded, high=blocked, critical=down"
          },
          "user_email": {
            "type": "string",
            "description": "Requester email address"
          }
        },
        "required": [
          "title",
          "description",
          "priority",
          "user_email"
        ]
      }
    }
  ]
}
```

### `templates/tool-dispatch.py`

```python
"""
Validated tool dispatcher with registry decorator and structured error return.
Drop-in for any provider: OpenAI, Claude, Gemini.

Usage:
    @tool_registry.register
    def get_weather(location: str, unit: str = "celsius") -> dict:
        ...

    result = tool_registry.dispatch("get_weather", {"location": "Paris"})
"""

from __future__ import annotations

import functools
import json
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry with validated dispatch and structured error returns."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable] = {}

    def register(self, fn: Callable) -> Callable:
        """Decorator: register a function as a dispatchable tool."""
        self._tools[fn.__name__] = fn

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)

        return wrapper

    def dispatch(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Dispatch a tool call by name with validated arguments.

        Returns a structured result dict — never raises.
        On error returns {"error": CODE, "message": "..."}.
        """
        if name not in self._tools:
            known = list(self._tools)
            return {
                "error": "TOOL_NOT_FOUND",
                "message": f"Unknown tool {name!r}. Available: {known}",
            }

        fn = self._tools[name]

        # Validate argument types against annotations
        hints = fn.__annotations__
        for param, value in arguments.items():
            expected = hints.get(param)
            if expected and not isinstance(value, expected):
                return {
                    "error": "INVALID_ARGUMENT",
                    "message": (
                        f"Parameter {param!r} expected {expected.__name__}, "
                        f"got {type(value).__name__}"
                    ),
                }

        try:
            result = fn(**arguments)
            logger.info("tool=%s args=%s result_type=%s", name, arguments, type(result).__name__)
            return result
        except TypeError as exc:
            return {"error": "MISSING_ARGUMENT", "message": str(exc)}
        except Exception as exc:
            logger.exception("tool=%s raised unexpected error", name)
            return {"error": "EXECUTION_ERROR", "message": str(exc)}

    def definitions_openai(self) -> list[dict]:
        """Return tool definitions in OpenAI format (uses docstring as description)."""
        tools = []
        for name, fn in self._tools.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": (fn.__doc__ or "").strip().splitlines()[0],
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            })
        return tools

    def definitions_claude(self) -> list[dict]:
        """Return tool definitions in Claude/Anthropic format."""
        tools = []
        for name, fn in self._tools.items():
            tools.append({
                "name": name,
                "description": (fn.__doc__ or "").strip().splitlines()[0],
                "input_schema": {"type": "object", "properties": {}, "required": []},
            })
        return tools


# Module-level singleton
tool_registry = ToolRegistry()


# ── Example tools ──────────────────────────────────────────────────────────────

@tool_registry.register
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a city. Use when user asks about weather conditions."""
    # Replace with real API call
    return {"location": location, "temperature": 22, "unit": unit, "condition": "sunny"}


@tool_registry.register
def search_records(query: str, limit: int = 10) -> dict:
    """Search internal records by keyword. Returns ranked list of matching items."""
    # Replace with real search
    return {"results": [], "total": 0, "query": query}


# ── Agentic loop helper ────────────────────────────────────────────────────────

def run_tool_loop(client, model: str, messages: list, tools: list, max_iter: int = 15) -> str:
    """
    Provider-agnostic agentic loop (OpenAI SDK shape).
    Calls tool_registry.dispatch for each tool_call returned by the LLM.
    """
    for iteration in range(max_iter):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content or ""

        messages.append(msg)

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = tool_registry.dispatch(tc.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })

    return f"[max_iterations={max_iter} reached]"
```

### `templates/tools.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [version, tools, audit_sink]
properties:
  version: {type: string, pattern: "^\\d+\\.\\d+\\.\\d+$"}
  audit_sink:
    type: object
    required: [kind, location]
    properties:
      kind: {type: string, enum: [clickhouse, bigquery, s3, file, sqlite]}
      location: {type: string}
  tools:
    type: array
    minItems: 1
    items:
      type: object
      required: [name, description, args_schema, safety_class, rate_limit_per_minute]
      properties:
        name: {type: string, pattern: "^[a-z][a-z0-9_]+$"}
        description: {type: string, minLength: 20}
        args_schema:
          type: object
          required: [type, properties]
        safety_class: {type: string, enum: [read-only, mutating, destructive]}
        human_gate: {type: boolean}
        rate_limit_per_minute: {type: integer, minimum: 1}
```

### `templates/_smoke-test.yaml`

```yaml
version: 1.0.0
audit_sink:
  kind: clickhouse
  location: ch://audit/agent_tools
tools:
  - name: lookup_customer
    description: "Returns customer record by ID. No side effects."
    safety_class: read-only
    rate_limit_per_minute: 60
    args_schema:
      type: object
      required: [customer_id]
      properties:
        customer_id: {type: string, pattern: "^c-[a-f0-9]{16}$"}
  - name: send_email
    description: "Send one email to the customer. Idempotent within 5 min."
    safety_class: mutating
    rate_limit_per_minute: 5
    args_schema:
      type: object
      required: [to, subject, body]
      properties:
        to: {type: string, format: email}
        subject: {type: string, minLength: 5}
        body: {type: string, minLength: 20}
```
