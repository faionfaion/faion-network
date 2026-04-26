# Agent Integration — Function Calling Patterns

## When to use
- Agent must take actions in external systems (APIs, databases, file system).
- Structured data extraction from unstructured text is required (guaranteed JSON schema).
- Orchestrating parallel I/O-bound tool calls to reduce latency.
- Building multi-step agentic loops where the LLM decides what action to take next.
- Replacing prompt-based output parsing with schema-enforced tool use.

## When NOT to use
- Simple Q&A where no external action is needed — tool use adds tokens and latency.
- When all tools have side effects and the task is exploratory; use read-only tools first.
- When the number of tools exceeds ~20 in a single call — model selection accuracy degrades; use routing or tool subsets instead.
- Structured output via tool for purely cosmetic formatting — prefer `response_format` or prefill instead.

## Where it fails / limitations
- LLMs hallucinate tool argument values (especially IDs, enums, dates) — always validate arguments before execution.
- Parallel tool execution masks ordering constraints; tools that modify shared state must run sequentially.
- Infinite agentic loops occur when no termination condition exists — always enforce `max_iterations`.
- Tool error messages fed back to the model can confuse it; provide clear, actionable error text in the `tool` role message.
- Anthropic Claude does not support streaming during tool use turns — plan UI accordingly.
- Large tool result payloads (e.g., full database rows) inflate context rapidly; truncate or summarize results before returning them.

## Agentic workflow
The orchestrator provides Claude with a curated tool set (≤10 per call). Claude emits a `tool_use` block; the executor dispatches the call (parallel if multiple independent calls in the same turn), captures results, and appends them as `tool_result` blocks. The loop continues until Claude emits a text-only response or `max_iterations` is reached. A separate validator subagent checks tool argument schemas before execution to catch hallucinated values.

### Recommended subagents
- `tool-executor` — Dispatches tool calls, handles errors, returns results in the correct message format.
- `arg-validator` — Validates tool arguments against schema before execution; rejects invalid calls with structured error feedback.
- `tool-router` — Given a query, selects the relevant tool subset from a large registry and passes only those to the LLM.

### Prompt pattern
```python
# Claude tool use — Anthropic SDK format
tools = [{
    "name": "get_order",
    "description": "Retrieve order details. Call when user asks about a specific order. Requires order_id.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string", "description": "Numeric order ID, e.g. '12345'"}
        },
        "required": ["order_id"],
        "additionalProperties": False
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Process tool calls
for block in response.content:
    if block.type == "tool_use":
        result = dispatch(block.name, block.input)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": block.id,
                         "content": json.dumps(result)}]
        })
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` Python SDK | Native Claude tool use with `tool_use` blocks | `pip install anthropic` / docs.anthropic.com |
| `openai` Python SDK | OpenAI function calling (parallel tool calls supported) | `pip install openai` / platform.openai.com/docs |
| `instructor` | Structured output via function calling for any provider | `pip install instructor` / python.useinstructor.com |
| `langchain` | Tool registry + agent executor abstractions | `pip install langchain` / python.langchain.com |
| `pydantic` | Schema validation for tool arguments | `pip install pydantic` / docs.pydantic.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Messages API | SaaS | Yes | `tool_use` / `tool_result` blocks; no streaming during tool turns |
| OpenAI API | SaaS | Yes | `tool_calls` in assistant message; supports parallel calls |
| LangSmith | SaaS | Yes | Traces tool call chains; shows argument + result per step |
| Zapier / Make | SaaS | Partial | Expose actions as webhook tools; not type-safe |
| Toolhouse | SaaS | Yes | Hosted tool registry; call tools without managing execution infra |

## Templates & scripts
See `templates.md` for full agentic loop, parallel executor, and tool router templates.

Minimal parallel tool executor (Anthropic format):
```python
import concurrent.futures, json, anthropic

def run_tools_parallel(tool_calls: list, registry: dict) -> list:
    results = []
    with concurrent.futures.ThreadPoolExecutor() as ex:
        futures = {
            ex.submit(registry[tc.name], **tc.input): tc
            for tc in tool_calls if tc.name in registry
        }
        for future, tc in futures.items():
            try:
                result = future.result(timeout=30)
            except Exception as e:
                result = {"error": str(e)}
            results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": json.dumps(result)
            })
    return results
```

## Best practices
- Write tool descriptions from the model's perspective: "Call when X. Do NOT call when Y." — not just what the tool does.
- Use `additionalProperties: false` in tool schemas to prevent the model from inventing extra fields.
- Return structured errors in `tool_result` (e.g., `{"error": "order_id not found", "code": "NOT_FOUND"}`) so the model can reason about next steps.
- For independent tool calls in the same response, execute in parallel — Claude often batches them intentionally.
- Set `tool_choice="any"` when you need the model to call at least one tool; set `tool_choice={"type": "tool", "name": "X"}` to force a specific tool.
- Keep `max_iterations` at 10 or below in production; log and alert when it triggers.
- Truncate large tool results to ≤2000 tokens before returning to context; summarize if needed.

## AI-agent gotchas
- Models hallucinate enum values not in the schema — always validate `input` against the schema before calling the implementation.
- Tool calls with side effects (writes, payments, sends) need a human-in-loop or dry-run mode; never execute destructive tools without confirmation in agentic pipelines.
- `stop_reason == "tool_use"` does not mean the task is complete — the loop must continue until `stop_reason == "end_turn"` or `"max_tokens"`.
- Sending back large tool results inflates the context; after 5+ tool turns, consider summarizing earlier results to avoid hitting context limits.
- Claude does not retry failed tool calls automatically — if a tool returns an error, the next response may ask the user for clarification rather than retrying with different arguments.
- Human-in-loop checkpoint: any tool that sends messages, modifies data, or charges money requires explicit approval before the `tool_use` block is dispatched.

## References
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use — Anthropic Tool Use guide
- https://platform.openai.com/docs/guides/function-calling — OpenAI Function Calling
- https://python.useinstructor.com — Instructor: structured output via function calling
- https://python.langchain.com/docs/modules/agents/ — LangChain Agent Executor
