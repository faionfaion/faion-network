# Agent Integration — Local LLM (Ollama)

## When to use
- Processing data that must not leave the machine (HIPAA, GDPR, corporate policy)
- High-volume classification/extraction where zero marginal API cost matters ($0 vs. $X per 1M tokens)
- Development and testing — no API keys, no rate limits, no costs, no internet required
- Edge computing or offline environments (IoT, air-gapped systems)
- Custom fine-tuned models deployed locally after training
- Agent prototyping before committing to cloud provider pricing

## When NOT to use
- Best-quality responses are required — even largest local models (70B) trail frontier cloud models on complex reasoning
- Hardware is unavailable: 7B needs 8GB VRAM or RAM; 70B needs 48GB — check before planning
- Real-time latency requirements on small hardware (inference on CPU is 5-20x slower than GPU)
- Multilingual tasks across >20 languages — local models lag cloud providers significantly
- Fine-tuned custom behavior is needed but GPU for fine-tuning is not available

## Where it fails / limitations
- Tool calling reliability degrades on smaller models (<13B); Llama 3.1+ with 32K+ context is minimum for reliable tool use
- First-token latency is high on large models (5-30s for 70B on consumer GPU) — streaming helps UX but not latency
- Context window in practice is limited by RAM: loading a 70B model at Q4 already uses 40GB; longer contexts use more
- Structured output (JSON schema mode) works in Ollama but compliance varies by model — test your specific model+schema combination
- Model updates are manual: `ollama pull <model>` — unlike cloud APIs, you don't get silent improvements
- No built-in load balancing or failover; requires external orchestration for production multi-instance setups

## Agentic workflow
Agents use Ollama via its OpenAI-compatible endpoint (`http://localhost:11434/v1`), enabling drop-in replacement of the OpenAI SDK with the base URL override. This means existing OpenAI-based agent code works with local models by changing one environment variable. For tool-calling agents, use Llama 3.1 8B or higher with `num_ctx: 32768`; tool calls below this context size fail unpredictably. Implement a health check before agent startup; on failure, fall back to cloud API automatically.

### Recommended subagents
- Any extraction or classification sub-agent where privacy matters
- Local test agents for CI pipelines that mock cloud LLM behavior

### Prompt pattern
OpenAI-compatible client (Python):
```python
from openai import OpenAI

# Drop-in replacement: just change base_url
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def local_chat(prompt: str, model: str = "llama3.1:8b") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].message.content
```

Native Ollama client with streaming:
```python
import ollama

def stream_response(prompt: str, model: str = "llama3.1:8b"):
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]
```

Tool-calling (Llama 3.1+ required):
```python
import ollama

tools = [{"type": "function", "function": {
    "name": "get_weather",
    "description": "Get weather for a city",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
}}]

response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": "Weather in Kyiv?"}], tools=tools)
if response.message.tool_calls:
    for tc in response.message.tool_calls:
        print(tc.function.name, tc.function.arguments)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ollama` | Run, manage, serve local models | `curl -fsSL https://ollama.com/install.sh \| sh` / ollama.com |
| `ollama-python` | Python client with async support | `pip install ollama` / github.com/ollama/ollama-python |
| `openai` Python SDK | Works with Ollama via base_url override | `pip install openai` |
| `litellm` | Unified proxy: routes OpenAI calls to Ollama | `pip install litellm` / docs.litellm.ai |
| `ngrok` / `cloudflared` | Expose local Ollama to remote agents | ngrok.com / developers.cloudflare.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ollama | OSS | Yes | Core runtime; OpenAI-compatible API at port 11434 |
| Ollama Model Library | SaaS | Yes | Hub for community models; `ollama pull <name>` |
| LiteLLM | OSS | Yes | Proxy that normalizes Ollama + cloud providers under one API |
| Open WebUI | OSS | Partial | Web UI for Ollama; not agent-facing but useful for model testing |
| Langfuse | OSS | Yes | Tracing works with Ollama via LiteLLM proxy |
| Qdrant | OSS | Yes | Vector DB for RAG pipelines using Ollama embeddings |

## Templates & scripts
See `templates.md` for: Modelfile for custom system prompts, multi-model router, Ollama+Qdrant RAG pipeline template.

Inline: health check with automatic cloud fallback (~25 lines):

```python
import httpx
from openai import OpenAI

def get_llm_client(prefer_local: bool = True) -> tuple[OpenAI, str]:
    """Return (client, model) — local if healthy, cloud fallback otherwise."""
    if prefer_local:
        try:
            resp = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
            if resp.status_code == 200:
                return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"), "llama3.1:8b"
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
    return OpenAI(), "gpt-4o-mini"  # cloud fallback
```

## Best practices
- Match quantization to available VRAM: Q4_K_M for memory-constrained, Q8_0 for quality-sensitive tasks
- Set `num_ctx` explicitly in Modelfile or request options — default (2048) is too small for most agent tasks; use 8192-32768
- Keep models loaded between calls: set `OLLAMA_KEEP_ALIVE=1h` to avoid 5-30s cold start on each request
- Test structured output compliance for your exact model + schema before committing to it in production
- Use GPU inference when available: CPU inference on 7B models is ~5-10 tokens/sec; GPU is 30-100 tokens/sec
- Pin model tags: `llama3.1:8b` not `llama3.1` — the untagged version may resolve to a different quantization after `ollama pull`
- For embedding tasks, use dedicated embedding models (`nomic-embed-text`, `mxbai-embed-large`) not generalist chat models

## AI-agent gotchas
- Human-in-loop checkpoint: local models have higher hallucination rates on specialized knowledge — add output validation before any action on local model outputs
- Tool calling fails silently if context window is too small: the model returns text instead of JSON tool calls — always set `num_ctx >= 32768` for tool use
- Ollama does not support concurrent model loading on the same GPU — sequential requests to different models cause eviction + reload overhead
- The OpenAI-compatible endpoint (`/v1/`) has slightly different error format than the native Ollama API — test error handling paths with both
- Container deployments need GPU passthrough (`--gpus all` for Docker); without it, inference falls back to CPU automatically with no warning
- `ollama serve` must be running before agent startup — implement retry loop with timeout, not `sleep X && start agent`

## References
- https://ollama.com/
- https://github.com/ollama/ollama
- https://ollama.com/library
- https://github.com/ollama/ollama-python
- https://docs.ollama.com/capabilities/tool-calling
- https://ollama.com/blog/structured-outputs
- https://docs.litellm.ai/docs/providers/ollama
