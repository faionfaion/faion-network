# Agent Integration — Local LLM (Ollama)

## When to use
- Data privacy requirements that prohibit sending content to external APIs
- High-volume, low-stakes tasks (classification, summarization) where cloud API costs are prohibitive
- Offline or air-gapped environments (edge devices, secure facilities)
- Development and testing — no API costs, no rate limits, instant iteration
- Deploying a custom fine-tuned model that is not hosted externally
- Latency-sensitive applications where local inference beats network round-trip

## When NOT to use
- Tasks requiring frontier-level reasoning (complex code generation, multi-step math) — local 7B/13B models underperform Opus/GPT-4o
- When the machine has <8GB RAM — models will page to disk and be unusably slow
- Production services with unpredictable load spikes — local GPU is not elastically scalable
- When you need the latest model capabilities — local model libraries lag cloud providers by months

## Where it fails / limitations
- RAM ceiling is hard: a 13B model requires ~16GB RAM; exceeding it causes OOM or extreme slowdown
- GPU detection can fail silently — Ollama may fall back to CPU without warning; always check inference speed
- Context window of local models is typically 4K–8K tokens by default (configured via `num_ctx` in Modelfile); cloud models offer 128K–2M
- Ollama server must be running before the agent starts — no auto-start by default on Linux
- Model pull during first use adds a blocking delay of minutes; agents must handle this gracefully
- Tool use / function calling support varies by model family — llama3.1 supports it; older mistral does not

## Agentic workflow
An agent using Ollama should check server availability via `/api/tags` at startup and fail fast with a clear error if Ollama is not running. Model selection should be configurable (not hardcoded) so the agent works on different hardware. The OpenAI-compatible endpoint (`/v1`) lets agents swap between Ollama and cloud APIs by changing only `base_url` and `api_key`, making local/cloud switching seamless for testing vs. production.

### Recommended subagents
- `faion-sdd-executor-agent` — can be configured to use Ollama for local SDD task drafts before sending to cloud for review

### Prompt pattern
Health-check before calling the model:
```python
import requests
def ollama_ready(base_url="http://localhost:11434") -> bool:
    try:
        return requests.get(f"{base_url}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False
```

OpenAI-compatible drop-in (swap `base_url` for local/cloud routing):
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ollama` (CLI) | Model management, server, interactive chat | https://ollama.com/install.sh / https://ollama.com |
| `ollama` (Python lib) | Pythonic wrapper over Ollama REST API | `pip install ollama` / https://github.com/ollama/ollama-python |
| `openai` (Python SDK) | OpenAI-compatible client for Ollama `/v1` endpoint | `pip install openai` |
| `docker` / `docker compose` | Containerized Ollama deployment with GPU passthrough | https://hub.docker.com/r/ollama/ollama |
| `nvidia-smi` | Monitor GPU VRAM usage during inference | built-in with NVIDIA driver |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Ollama | OSS | Yes | Primary — HTTP API on port 11434 |
| Open WebUI | OSS | Partial | Browser UI over Ollama; not for agent-to-agent calls |
| LM Studio | SaaS (free desktop) | Yes | OpenAI-compatible local API, Windows/macOS |
| llama.cpp | OSS | Yes | Lower-level; Ollama wraps it internally |
| Hugging Face Transformers | OSS | Yes | Full control, more complex than Ollama |
| Jan | OSS | Yes | Local app with OpenAI-compatible API |

## Templates & scripts
See `templates.md` for `OllamaService` class template. Minimal startup check + generation:

```python
import requests, json

OLLAMA = "http://localhost:11434"

def check_and_generate(prompt: str, model="llama3.1:8b") -> str:
    if requests.get(f"{OLLAMA}/api/tags", timeout=2).status_code != 200:
        raise RuntimeError("Ollama not running. Start with: ollama serve")
    models = [m["name"] for m in requests.get(f"{OLLAMA}/api/tags").json()["models"]]
    if model not in models:
        raise RuntimeError(f"Model {model!r} not pulled. Run: ollama pull {model}")
    r = requests.post(f"{OLLAMA}/api/generate",
                      json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
    return r.json()["response"]
```

## Best practices
- Match model size to available VRAM: 7B/8B needs 6–8GB, 13B needs 12–16GB, 70B needs 40GB+
- Use quantized variants (Q4_K_M, Q5_K_M) — they cut VRAM by 50–60% with 2–5% quality loss
- Set `num_ctx` in Modelfile explicitly — default is model-dependent and often too small for production
- Keep Ollama running as a systemd service on Linux so agents don't need to start it
- Use Modelfiles to bake system prompts into a named model (`ollama create task-agent -f Modelfile`) — avoids re-sending system prompts per call
- Set `timeout=120` or higher for large models; default HTTP timeouts will fail on first token generation
- For concurrent agent requests, Ollama queues them — design agents to expect serialized local inference

## AI-agent gotchas
- Ollama does not support parallel request processing by default — an agent pool sending concurrent requests will serialize, not parallelize
- `eval_count` and `total_duration` in the response let you compute tokens/second; log these to detect GPU fallback (CPU is 10–50x slower)
- Model names must match exactly including the tag (e.g., `llama3.1:8b` not `llama3.1`) — wrong name returns 404 with no helpful message
- Agents that pull models on first use must handle the pull as a blocking operation with streaming status — the pull JSONL stream ends with `"status": "success"`
- The `/api/generate` endpoint does not support tool use; use `/api/chat` with supported models (llama3.1, mistral-nemo) for function calling
- Local model context windows are small — an agent that passes a long conversation history will silently truncate it; monitor `eval_count` for signs of truncation

## References
- https://ollama.com/
- https://github.com/ollama/ollama
- https://ollama.com/library (model catalog)
- https://github.com/ollama/ollama-python
- https://github.com/ollama/ollama/blob/main/docs/modelfile.md
