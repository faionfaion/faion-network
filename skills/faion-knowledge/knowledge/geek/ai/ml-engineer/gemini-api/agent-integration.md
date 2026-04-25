# Agent Integration — Google Gemini API

## When to use
- Task requires the largest available context window (1M-2M tokens): full codebase review, long document analysis
- Native multimodal input needed: video, audio, or PDF without conversion preprocessing
- Google Search grounding is required for factual, real-time answers
- Cost-sensitive high-volume workload where Gemini Flash is 3-5x cheaper than GPT-4o
- Python sandbox / code execution must run inside the model response (no external infra)
- Live API needed: real-time audio/video streaming with VAD and sub-second responses

## When NOT to use
- Existing stack is OpenAI-native and migration cost exceeds benefit — stay with GPT-4o
- Output must be deterministic across providers: Gemini's token encoding and sampling differ
- Task is Claude-specific (extended thinking, long XML prompts, Constitution AI behavior)
- Free tier limits (10 RPM, 1000 RPD) are hit in production — upgrade or switch to paid tier first
- Enterprise compliance requires Azure or AWS VPC deployment — use Vertex AI, not Google AI Studio

## Where it fails / limitations
- Thought Signatures must be included in multi-turn Gemini 3 conversations even at `thinking_level=minimal` — omitting them breaks context continuity
- Function calling responses can include images/video in Gemini 3 but these are large blobs — handle MIME types explicitly
- Context caching saves 75% cost but has minimum size requirements (≥32K tokens) and 1-hour minimum TTL
- Free tier rate limits (2 RPM for 1.5 Pro) make it unusable for any production traffic
- Safety filters block more aggressively than OpenAI in some categories; tune `safety_settings` or switch to Vertex AI
- `generate_content` is synchronous by default in the Python SDK; always use `generate_content_async` in agents
- Vertex AI requires GCP project + service account setup — 2-3x more friction than Google AI Studio keys

## Agentic workflow
Gemini integrates cleanly into multi-step agents via function declarations. Declare tools using `genai.protos.Tool` and iterate the function-calling loop: call model → parse `function_call` responses → execute → return `function_response` parts. For long-context tasks (codebase review, document analysis), use context caching to pin the large corpus and only vary the query per iteration. Use `generate_content_async` throughout the loop to avoid blocking the event loop in FastAPI or async agents.

### Recommended subagents
- `faion-sdd-executor-agent` — can be configured to use Gemini Flash for cost-sensitive execution steps

### Prompt pattern
```python
import google.generativeai as genai
import asyncio

model = genai.GenerativeModel(
    "gemini-2.0-flash",
    tools=[search_tool, db_tool],
    system_instruction="You are a data analyst. Always call tools before answering."
)

async def agent_loop(query: str) -> str:
    chat = model.start_chat()
    response = await chat.send_message_async(query)
    while response.candidates[0].finish_reason.name == "STOP":
        # check for function_call parts
        for part in response.parts:
            if fn := part.function_call:
                result = await dispatch(fn.name, dict(fn.args))
                response = await chat.send_message_async(
                    genai.protos.Part(function_response=genai.protos.FunctionResponse(
                        name=fn.name, response={"result": result}
                    ))
                )
        break
    return response.text
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-generativeai` | Official Python SDK (Google AI Studio) | `pip install google-generativeai` / [docs](https://ai.google.dev/docs) |
| `google-cloud-aiplatform` | Vertex AI SDK (enterprise, GCP) | `pip install google-cloud-aiplatform` / [docs](https://cloud.google.com/vertex-ai) |
| `litellm` | Unified proxy with Gemini support | `pip install litellm` / [docs](https://docs.litellm.ai) |
| `gcloud` CLI | GCP auth, Vertex AI project setup | [install](https://cloud.google.com/sdk/docs/install) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google AI Studio | SaaS | Yes | Free tier + paid; API keys; simplest setup |
| Vertex AI (GCP) | SaaS | Yes | Enterprise compliance, VPC, IAM; higher setup cost |
| LiteLLM | OSS proxy | Yes | Normalizes Gemini to OpenAI format; enables drop-in swap |
| OpenRouter | SaaS | Yes | Routes to Gemini with unified billing; adds ~20ms latency |
| Portkey | SaaS gateway | Yes | Multi-provider routing; Gemini + cost tracking |

## Templates & scripts
```python
# context_cache.py — pin large corpus, vary queries cheaply (≤40 lines)
import google.generativeai as genai
from datetime import timedelta

genai.configure(api_key="GOOGLE_API_KEY")

def create_cached_context(document_text: str) -> str:
    """Cache a large document for repeated queries. Returns cache name."""
    cache = genai.caching.CachedContent.create(
        model="models/gemini-1.5-pro-001",
        contents=[{"role": "user", "parts": [{"text": document_text}]}],
        ttl=timedelta(hours=1),
        display_name="document_cache",
    )
    return cache.name

def query_with_cache(cache_name: str, query: str) -> str:
    model = genai.GenerativeModel.from_cached_content(
        cached_content=cache_name
    )
    response = model.generate_content(query)
    return response.text

# Usage:
# cache_name = create_cached_context(open("large_doc.txt").read())
# answer = query_with_cache(cache_name, "What are the key risks?")
```

## Best practices
- Use `gemini-2.0-flash` as the default agent model; upgrade to 3 Pro only for tasks requiring deep reasoning
- Always pass `thinking_budget` or `thinking_level` explicitly in Gemini 3 — default `high` adds latency and cost
- Context cache activates at ≥32K tokens; batch short documents into one cached corpus rather than caching individually
- Use `media_resolution="medium"` for PDFs and `"high"` for images requiring detail — `ultra-high` rarely needed
- Prefer Vertex AI over Google AI Studio for production: SOC 2, HIPAA, no data training by default
- For streaming in agents, use `stream=True` and process `chunk.text` incrementally to reduce TTFT
- Store API keys in env vars; never log `genai.configure()` call arguments
- In multi-turn conversations with Gemini 3, always include `thought_signature` parts even when thinking is minimal

## AI-agent gotchas
- `finish_reason` values differ from OpenAI: `STOP` = normal, `MAX_TOKENS` = truncated, `SAFETY` = blocked — handle all three
- Safety blocks return a response with no `text` and `finish_reason=SAFETY`; check before accessing `.text` to avoid AttributeError
- Function call responses must be `genai.protos.Part` objects, not raw dicts — serialization errors are silent
- Gemini 3 Thought Signatures are required even when `thinking_level="minimal"`; omitting breaks multi-turn continuity
- The free tier's 10 RPM limit triggers `ResourceExhausted` 429 errors within seconds under concurrent agent calls; implement exponential backoff
- Context window advertised as 2M tokens but reliable performance degrades past ~500K for complex reasoning tasks
- Async SDK (`generate_content_async`) is required in FastAPI/asyncio agents; sync calls block the event loop

## References
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Python SDK GitHub](https://github.com/google-gemini/generative-ai-python)
- [Gemini Cookbook](https://github.com/google-gemini/gemini-api-cookbook)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Context Caching Guide](https://ai.google.dev/gemini-api/docs/caching)
- [Live API Docs](https://ai.google.dev/gemini-api/docs/live)
- [LiteLLM Gemini Integration](https://docs.litellm.ai/docs/providers/gemini)
