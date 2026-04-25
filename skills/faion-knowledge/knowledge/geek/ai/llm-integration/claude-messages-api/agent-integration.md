# Agent Integration — Claude Messages API

## When to use
- All direct Claude API calls — Messages is the primary (and only) completion endpoint
- Streaming responses to a user interface or a pipeline sink that consumes partial text
- Multi-turn agent conversations where the agent must maintain message history explicitly
- Vision tasks: screenshot analysis, document OCR, UI inspection, PDF summarization
- When the agent needs to detect `stop_reason` to branch logic (tool_use vs end_turn vs max_tokens)

## When NOT to use
- When persistent thread storage is needed across sessions (Anthropic has no Threads equivalent — build your own)
- When you need guaranteed schema compliance without retry loops (use OpenAI `beta.parse` or `instructor`)
- High-volume batch jobs — prefer the Batch API (50% cost reduction) over per-call Messages API
- Computer Use or Extended Thinking inside a stateless lambda/function — those features need multi-turn conversation state

## Where it fails / limitations
- No native session/thread persistence — message history is caller's responsibility
- `max_tokens` is required and cannot be omitted — easy to truncate unexpectedly if set too low
- `temperature` range is 0–1 (not 0–2 like OpenAI) — prompts tuned for OpenAI may behave differently
- PDF support has a 100-page / 32MB limit; large PDFs must be chunked before sending
- Streaming + tool use requires parsing `input_json_delta` events incrementally — non-trivial to implement correctly
- `top_k` and `top_p` interact with `temperature`; setting all three simultaneously is usually wrong
- SSE streaming format differs from OpenAI — not interchangeable without an adapter layer

## Agentic workflow
The Messages API is the single integration point for all Claude calls in an agent system. A subagent constructs the message array (system + alternating user/assistant), calls `client.messages.create` or `client.messages.stream`, inspects `stop_reason`, and routes to the appropriate next step. For long-running pipelines, stream responses to a queue and process in a consumer. For multi-turn, append the assistant response to the message array before sending the next user turn.

### Recommended subagents
- `faion-sdd-executor-agent` — uses Messages API for all Claude calls; explicit stop_reason handling per phase
- `nero-sdd-executor-agent` — multi-turn conversation with accumulated message history for context

### Prompt pattern
```python
# Multi-turn agent loop — explicit history management
import anthropic

client = anthropic.Anthropic()

def agent_loop(system: str, initial_prompt: str, max_turns=10) -> str:
    messages = [{"role": "user", "content": initial_prompt}]
    for _ in range(max_turns):
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=messages
        )
        assistant_content = resp.content
        messages.append({"role": "assistant", "content": assistant_content})

        if resp.stop_reason == "end_turn":
            return resp.content[0].text
        elif resp.stop_reason == "max_tokens":
            raise RuntimeError("Response truncated")
        elif resp.stop_reason == "tool_use":
            # handle tool calls, append tool_result, continue loop
            messages.append({"role": "user", "content": handle_tools(assistant_content)})
        else:
            break
    return resp.content[0].text
```

```python
# Vision: analyze screenshot from local file
import base64

def analyze_screenshot(path: str, question: str) -> str:
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}},
            {"type": "text", "text": question}
        ]}]
    )
    return resp.content[0].text
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` SDK | Messages API Python client | `pip install anthropic` |
| `httpx` | Raw HTTP debugging of SSE streams | `pip install httpx` |
| `tenacity` | Retry on RateLimitError / APIConnectionError | `pip install tenacity` |
| `rich` | Pretty-print streaming output in terminal | `pip install rich` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Primary endpoint; all models, batch, caching, streaming |
| AWS Bedrock | SaaS | Yes | Messages API compatible; enterprise IAM integration |
| LiteLLM | OSS proxy | Yes | Translates OpenAI-format calls to Anthropic Messages API |
| Helicone | SaaS | Yes | Proxy with logging; tracks streaming token usage |
| Portkey | SaaS | Yes | Fallback from Claude to GPT-4o on 5xx; useful for SLA |

## Templates & scripts
See `templates.md` for full streaming and event-based patterns. Minimal streaming consumer:

```python
def stream_to_string(system: str, prompt: str) -> str:
    """Stream Claude response and return full text."""
    parts = []
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            parts.append(text)
    return "".join(parts)
```

## Best practices
- Always check `resp.stop_reason` before accessing `resp.content[0].text` — tool_use blocks are not text
- Append the full `resp.content` list (not just text) as the assistant turn in multi-turn history — tool_use blocks must be preserved
- Use `stream.get_final_message()` when you need usage stats from a streaming call
- Place image content before text content in multi-modal messages — model processes images better when they come first
- Use `metadata={"user_id": "..."}` to tag calls for abuse detection and cost attribution
- For PDF analysis, check page count first; split at 50 pages if near the 100-page limit
- Keep `system` prompt stable across calls in a session to enable Prompt Caching benefits

## AI-agent gotchas
- `resp.content` is a `list[ContentBlock]` — content blocks can be `text`, `tool_use`, or `thinking`; always type-check before accessing `.text`
- Streaming with tools: `input_json_delta` events carry partial JSON — you must accumulate and parse after `content_block_stop`, not inline
- Multi-turn history must alternate user/assistant roles strictly — consecutive same-role messages raise a 400 error
- `stop_sequences` match on the next token boundary — if the model generates a stop sequence mid-sentence, the sentence is cut off without warning
- Image URLs in messages are fetched at inference time — if the URL returns a 403 at that moment, the call fails silently with a content error block
- PDF pages exceeding 100 produce an API error, not a truncation — validate before sending

## References
- https://docs.anthropic.com/en/api/messages
- https://docs.anthropic.com/en/api/messages-streaming
- https://docs.anthropic.com/en/docs/build-with-claude/vision
- https://docs.anthropic.com/en/docs/build-with-claude/pdf-support
- https://github.com/anthropics/anthropic-sdk-python
