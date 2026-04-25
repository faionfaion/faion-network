# Agent Integration — Tool Use and Function Calling

## When to use
- Agent needs to fetch live data (weather, prices, user records) that the LLM does not know
- Workflow requires state changes: writing files, sending messages, creating DB records
- Output must be structured JSON consumed downstream — tools enforce the schema
- Building multi-step agentic loops where each step depends on real execution results
- Connecting an LLM to internal APIs or microservices

## When NOT to use
- Query is pure text reasoning with no external dependency (summarize, translate, brainstorm)
- Tool roundtrip latency is unacceptable and a pre-fetched context would suffice
- LLM accuracy on tool selection is low (<70%) — use structured output or hardcoded routing instead
- Single, fully deterministic function is always called — skip LLM selection, call it directly

## Where it fails / limitations
- Tool schema token cost: 64-128 tools consume thousands of tokens per call; prune aggressively
- Argument hallucination: LLM invents plausible but wrong parameter values (e.g., wrong user IDs)
- Infinite agentic loops: without a max-iterations guard the loop never terminates
- Provider-specific formats: OpenAI `tool_calls`, Claude `tool_use`, Gemini `function_call` are incompatible — abstraction layer required for multi-provider apps
- Parallel tool calls can trigger race conditions if tools share mutable state
- Streaming tool calls are partially supported; avoid for tools with long-running side effects

## Agentic workflow
A Claude subagent receives a task description plus a curated set of tool definitions (≤20 for focused tasks). It runs an agentic loop: call LLM → parse tool_use blocks → execute function → feed `tool_result` back → repeat until `stop_reason == end_turn`. The executor layer (Python/TypeScript) owns validation, error handling, and circuit breaking — never the LLM. Use a router subagent when the full tool catalogue is large: it selects the relevant subset before handing off to a specialist subagent.

### Recommended subagents
- `faion-sdd-executor-agent` — general-purpose executor that can be given tool definitions alongside its task context

### Prompt pattern
```
<tools>
  <tool name="search_knowledge_base">
    <description>Search internal knowledge base. Returns top-K passages.</description>
    <parameters>{"query": "string", "top_k": "integer"}</parameters>
  </tool>
</tools>
<task>
  Answer the user's question using only knowledge_base results. Call the tool first.
</task>
```

```python
# Minimal agentic loop (provider-agnostic pseudocode)
MAX_ITER = 10
for _ in range(MAX_ITER):
    response = llm.call(messages=messages, tools=tools)
    if response.stop_reason == "end_turn":
        break
    for call in response.tool_calls:
        result = dispatch(call.name, call.arguments)  # validate + execute
        messages.append(tool_result(call.id, result))
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` CLI | Test function-calling endpoints interactively | `pip install openai` / [docs](https://platform.openai.com/docs/guides/function-calling) |
| `anthropic` CLI | Debug Claude tool_use responses | `pip install anthropic` / [docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) |
| `litellm` | Unified proxy normalizing all provider tool formats | `pip install litellm` / [github](https://github.com/BerriAI/litellm) |
| `instructor` | Enforce Pydantic schemas via tool calling | `pip install instructor` / [docs](https://python.useinstructor.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI API | SaaS | Yes | `tools` param, parallel calls, streaming; 128 tools max |
| Anthropic API | SaaS | Yes | `tools` param, `tool_use`/`tool_result` format; 64 tools max |
| Gemini API | SaaS | Yes | `function_declarations`; 128 tools max; best for multimodal |
| LiteLLM | OSS proxy | Yes | Normalizes all provider formats behind OpenAI-compatible interface |
| Ollama | OSS local | Partial | Tool support varies by model; llama3.1+ works |
| Portkey | SaaS gateway | Yes | Multi-provider routing + tool call logging |

## Templates & scripts
```python
# tool_dispatch.py — validated executor with error return (≤50 lines)
import json
from typing import Any, Callable

REGISTRY: dict[str, Callable] = {}

def tool(name: str):
    def decorator(fn: Callable):
        REGISTRY[name] = fn
        return fn
    return decorator

def dispatch(name: str, arguments: str | dict) -> dict:
    if name not in REGISTRY:
        return {"error": f"Unknown tool: {name}"}
    args = json.loads(arguments) if isinstance(arguments, str) else arguments
    try:
        result = REGISTRY[name](**args)
        return {"result": result}
    except TypeError as e:
        return {"error": f"Bad arguments: {e}"}
    except Exception as e:
        return {"error": str(e)}

# Usage:
# @tool("get_weather")
# def get_weather(location: str, unit: str = "celsius") -> str:
#     return f"22{unit[0].upper()} in {location}"
```

## Best practices
- Keep tool count per call ≤20; use RAG-over-tools to select the relevant subset for each query
- Write descriptions as imperative sentences: "Returns current weather for a city." Not "weather tool"
- Mark all parameters as required unless the default is safe and obvious; the LLM often skips optional params
- Return structured error dicts (`{"error": "..."}`) instead of raising — lets the LLM retry intelligently
- Cache pure read tools (weather, DB lookups) with a short TTL to cut API costs on repeated calls
- Log every dispatch: `{tool, args, result_summary, latency_ms}` — essential for debugging loops
- For destructive tools (delete, send email), add a human-in-loop checkpoint or a `dry_run` parameter
- Validate argument types before execution — never pass LLM-generated args directly to shell or SQL

## AI-agent gotchas
- Argument hallucination peaks with vague parameter names: `id` hallucinated vs `user_uuid` less so — be explicit
- The LLM may call the same tool twice with identical args when it does not see a result — always echo the result back
- Infinite loop guard: set `MAX_ITER` and return a sentinel message to the user if reached
- Multi-provider normalization: Claude returns `tool_use` content blocks, not a top-level `tool_calls` array — handle both shapes or use LiteLLM
- Extended thinking (Claude) interleaves thinking blocks with tool_use; strip thinking blocks before logging
- Streaming tool calls: arguments arrive as partial JSON fragments — buffer until `stop` before parsing
- Tool definitions are injected into every context window; rotate or trim when switching tasks

## References
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Google Gemini Function Calling](https://ai.google.dev/docs/function_calling)
- [LiteLLM Tool Calling](https://docs.litellm.ai/docs/completion/function_call)
- [Instructor (Pydantic enforcement)](https://python.useinstructor.com/)
- [Function Calling Best Practices — Prompt Engineering Guide](https://www.promptingguide.ai/applications/function_calling)
