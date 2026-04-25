# Agent Integration — Gemini API Basics

## When to use
- Starting a new project that will use Gemini and needs auth, model selection, and generation config established
- Exploring Gemini model capabilities (Flash vs. Pro vs. Thinking) before committing to an architecture
- Building a simple text generation or chat pipeline that does not yet need multimodal or function calling
- The team needs a working reference implementation of streaming, async, and JSON output modes

## When NOT to use
- The task requires function calling or tool use — see `gemini-api-integration` methodology for that
- You need file uploads (audio/video/large docs) — use the Files API from `gemini-api-integration`
- The context window needed exceeds what Flash supports and you have not benchmarked Pro vs. Flash trade-offs yet
- You are integrating with Google Cloud enterprise infra — start with Vertex AI patterns, not AI Studio keys

## Where it fails / limitations
- The free tier (AI Studio API key) is not suitable for production; it has low RPM limits and no SLA
- `generate_content_async` uses a different underlying event loop than the sync SDK; mixing sync and async calls in the same script causes `RuntimeError: This event loop is already running`
- `response_mime_type: "application/json"` without `response_schema` returns valid JSON but with arbitrary structure that drifts between calls
- Gemini 2.0 Flash Thinking exposes reasoning tokens in `response.candidates[0].content.parts` as a separate part — agents that only read `.text` miss the reasoning chain
- Safety block on the prompt (not the output) returns an empty `candidates` list; agents that index `candidates[0]` without checking will raise `IndexError`

## Agentic workflow
A subagent setting up Gemini basics should configure API key from env, select the model based on task complexity (Flash for speed, Pro for long context, Thinking for math/reasoning), set `generation_config` with explicit `max_output_tokens` and `temperature`, and wrap the call with safety check + retry logic. For chat sessions, the subagent should persist the `chat.history` object across turns, not rebuild it from scratch each call.

### Recommended subagents
- `faion-sdd-executor-agent` — implement Gemini service class with config dataclass and retry as an SDD task
- General-purpose subagent — use `gemini-2.0-flash` for fast intermediate steps in multi-stage pipelines

### Prompt pattern
```
Initialize a Gemini 2.0 Flash model with temperature=0.3, max_output_tokens=2048.
Request JSON output using response_mime_type="application/json" with schema: {schema}.
Handle BlockedPromptException and ResourceExhausted with exponential backoff (max 3 retries).
```

```
Start a Gemini chat session with system_instruction: "{system}".
Send the following messages in sequence: {messages}.
After each response, log usage_metadata.prompt_token_count and candidates_token_count.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install google-generativeai` | SDK install | [pypi](https://pypi.org/project/google-generativeai/) |
| `pip install google-genai` | New SDK (v0.8+, preferred for new projects) | [pypi](https://pypi.org/project/google-genai/) |
| `gcloud auth application-default login` | Vertex AI auth without API key | [gcloud docs](https://cloud.google.com/sdk/gcloud) |
| `python -m pytest` | Test generation config + safety settings | system |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google AI Studio | SaaS | Yes | Browser playground + API key; use for prototyping only |
| Vertex AI | SaaS | Yes | Production; IAM auth, no API key; use for regulated apps |
| LiteLLM | OSS | Yes | Provider-agnostic wrapper; switch between Gemini/OpenAI/Claude with one config change |
| aisuite (PyPI) | OSS | Yes | Minimal multi-provider SDK; simpler than LiteLLM for basic use |

## Templates & scripts
See `templates.md` for a GeminiService class template with config dataclass, retry, and usage logging.

Inline async streaming example (≤20 lines):
```python
import asyncio
import google.generativeai as genai

async def stream_async(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    model = genai.GenerativeModel(model_name)
    response = await model.generate_content_async(prompt, stream=True)
    parts = []
    async for chunk in response:
        if chunk.text:
            parts.append(chunk.text)
    return "".join(parts)
```

## Best practices
- Use `gemini-2.0-flash` as default for agent pipeline steps; only escalate to Pro when context >128K or quality is clearly insufficient
- Set `max_output_tokens` in every `GenerationConfig`; omitting it means the model can produce arbitrarily long responses
- Always check `response.prompt_feedback.block_reason` before `response.text`; wrap in a helper that returns `None` on block
- For context caching: only cache when the same prompt prefix (system prompt + large document) appears in >5 requests per session; below that threshold the caching overhead is not worth it
- Store API keys in environment variables, never in code; for Vertex AI use workload identity federation, not service account JSON files checked into git

## AI-agent gotchas
- Model name drift: `gemini-1.5-pro-latest` resolves to different model versions over time; pin to a specific version slug (e.g., `gemini-1.5-pro-002`) in production pipelines
- `chat.history` is mutable; if an agent appends to it after a blocked response the history becomes inconsistent — always validate the last response before appending
- Thinking models (`gemini-2.0-flash-thinking-exp`) return reasoning in a separate content part; agents that concat all parts may expose internal chain-of-thought to end users unintentionally
- Human checkpoint needed before switching from free tier (AI Studio) to Vertex AI in production; billing setup requires manual GCP project configuration that cannot be automated safely
- Rate limit errors (`ResourceExhausted`) on the free tier are not transient at low RPM — they indicate you have hit the daily quota, not a temporary spike; exponential backoff will not help

## References
- [Gemini API docs](https://ai.google.dev/docs)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)
- [Google AI Studio](https://aistudio.google.com/)
- [Model versions and naming](https://ai.google.dev/gemini-api/docs/models/gemini)
- [Context caching guide](https://ai.google.dev/gemini-api/docs/caching)
