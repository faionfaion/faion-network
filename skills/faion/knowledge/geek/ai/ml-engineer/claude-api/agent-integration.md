# Agent Integration — Claude API

## When to use
- Building any feature that calls Claude for text generation, reasoning, or tool use
- Need structured JSON output from Claude via forced tool use
- Implementing agentic loops where Claude selects and calls tools
- Processing large batches of documents or tasks where 50% cost reduction (Batch API) matters
- High-cost system prompts that repeat across many calls — Prompt Caching cuts input cost by 90%
- Complex reasoning tasks where Extended Thinking (claude-opus-4-5) significantly improves accuracy

## When NOT to use
- Simpler tasks that don't require Claude's full capability — check if a cheaper model (Haiku 3.5) or a different provider (DeepSeek) suffices
- Real-time streaming UI is not needed and response quality > latency — prefer Batch API for cost savings
- The system has an existing multi-provider abstraction (LiteLLM, LangChain) that already handles Claude — use that abstraction rather than calling the API directly

## Where it fails / limitations
- Rate limits: default tier limits (requests/minute, tokens/minute) hit quickly in parallel agentic loops; must implement exponential backoff with jitter
- Prompt Caching TTL is 5 minutes — long gaps between requests invalidate the cache; ineffective for low-traffic applications
- Extended Thinking minimum budget is 1,024 tokens; cannot use thinking for tasks that need very short outputs
- Batch API has a 24-hour processing window — unsuitable for user-facing interactive requests
- Tool use reliability degrades when more than ~10 tools are provided simultaneously — curate tool lists per task
- Streaming reconnection requires tracking the last `text` block index and resuming from it; the SDK does not handle this automatically

## Agentic workflow
An agent calls `client.messages.create()` with a system prompt (cached), a list of tools, and the current conversation. If Claude returns a `tool_use` block, the agent executes the tool, appends the result as a `tool_result` content block, and loops until Claude returns a `text` block as the final response. For Batch API workloads, the agent writes requests to a JSONL file, submits the batch, polls for completion, and streams results back to the caller.

### Recommended subagents
- Tool-use orchestrator subagent — manages the tool-call loop, handles `is_error` on tool results, limits retries to 3 before escalating
- Batch processor subagent — packages tasks into Batch API requests (up to 10,000), polls until done, parses results, returns structured output

### Prompt pattern
```python
# Minimal tool-use loop
MAX_TURNS = 10
messages = [{"role": "user", "content": user_input}]

for _ in range(MAX_TURNS):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        tools=TOOLS,
        messages=messages,
    )
    if response.stop_reason == "end_turn":
        break
    # Process tool calls
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` (Python) | Official Python SDK | `pip install anthropic` — [pypi.org/project/anthropic](https://pypi.org/project/anthropic/) |
| `@anthropic-ai/sdk` (TypeScript) | Official TypeScript SDK | `npm install @anthropic-ai/sdk` |
| `claude` (CLI) | Claude Code CLI | [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) |
| `curl` | Direct API testing | Built-in; `x-api-key: $ANTHROPIC_API_KEY` header |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes — REST + SDK | Core service; Messages, Batch, Streaming |
| Claude.ai | SaaS | No (browser only) | Not for agents — use API |
| LiteLLM | OSS proxy | Yes | Wraps Claude API with unified interface, fallback routing |
| Langfuse | SaaS + OSS | Yes | Tracing Claude calls, cost per request, prompt versioning |
| Helicone | SaaS | Yes — proxy | Claude-specific analytics, caching, rate limit monitoring |
| Portkey | SaaS | Yes — gateway | Multi-provider fallback, semantic caching |

## Templates & scripts
See `templates.md` for full streaming, tool use, and Batch API templates.

Inline: Prompt Caching with tool-use skeleton (< 50 lines):

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = "You are a helpful assistant with access to tools."
TOOLS = [
    {
        "name": "search",
        "description": "Search the knowledge base for relevant information.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    }
]

def agent_turn(user_message: str, context_docs: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=[
            {"type": "text", "text": SYSTEM},
            # Cache large static context (must be >= 1024 tokens)
            {"type": "text", "text": context_docs, "cache_control": {"type": "ephemeral"}},
        ],
        tools=TOOLS,
        messages=[{"role": "user", "content": user_message}],
    )
    # Handle tool calls inline for single-turn example
    for block in response.content:
        if hasattr(block, "text"):
            return block.text
    return ""
```

## Best practices
- Always set `cache_control: {"type": "ephemeral"}` on system prompts or large context blocks that appear in multiple requests — 90% input cost reduction on cache hits
- Use `max_tokens` conservatively per model tier: 512 for Haiku classification tasks, 4096 for Sonnet generation, 8192+ only for Opus extended reasoning
- Implement exponential backoff with jitter for rate limit errors (HTTP 429): `wait = min(2**attempt + random.uniform(0,1), 60)`
- For structured output, use forced tool use (`tool_choice={"type": "tool", "name": "output"}`) rather than prompting for JSON — it's more reliable across model updates
- Streaming: process `content_block_delta` events incrementally; store `input_json_delta` for tool inputs until `input_json` is complete; don't buffer full response before acting
- Batch API: group requests by deadline — interactive tasks never go in a batch; offline enrichment tasks always should

## AI-agent gotchas
- Infinite tool loops: an agent without a `MAX_TURNS` guard can call tools indefinitely if Claude never reaches `end_turn`; always enforce a hard iteration cap and log the loop count
- Tool schema drift: if you update a tool's `input_schema` without updating the agent loop's handler, Claude may generate inputs the handler cannot parse — validate tool inputs against the schema before executing
- Extended Thinking streaming: `thinking` blocks arrive before `text` blocks; the SDK delivers them as `thinking_delta` events — if you only listen for `text_delta`, you silently discard thinking tokens while still paying for them
- Human-in-loop checkpoint: for agentic tasks with write effects (database mutations, API calls, emails), inject a confirmation step before the final tool call — Claude cannot undo executed side effects
- API key rotation: `ANTHROPIC_API_KEY` must be in environment, not hardcoded; rotate keys on a schedule and use a secrets manager (1Password, AWS Secrets Manager) for production

## References
- [Anthropic API documentation](https://docs.anthropic.com/en/api)
- [Messages API reference](https://docs.anthropic.com/en/api/messages)
- [Prompt Caching guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Tool Use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Extended Thinking guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Batch API reference](https://docs.anthropic.com/en/api/creating-message-batches)
- [Streaming guide](https://platform.claude.com/docs/en/build-with-claude/streaming)
