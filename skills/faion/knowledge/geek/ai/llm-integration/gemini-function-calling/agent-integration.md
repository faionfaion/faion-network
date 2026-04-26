# Agent Integration — Gemini Function Calling

## When to use
- Agent pipelines that already use Google Cloud / Vertex AI infrastructure
- Tasks requiring Google Search grounding — live web search results embedded in LLM responses
- Workflows that benefit from Gemini's native automatic function calling (model executes tools without the caller managing the loop)
- Embedding generation for RAG pipelines using `text-embedding-004` (768d, strong multilingual)
- Structured extraction with `response_mime_type: application/json` + JSON Schema (Gemini native, no beta)

## When NOT to use
- When OpenAI or Claude is already in the pipeline — adding Gemini increases vendor surface area without clear benefit unless Google Search grounding is needed
- Production pipelines requiring deterministic tool execution — automatic function calling may call tools in unexpected order
- Tasks requiring Anthropic Extended Thinking-level reasoning — Gemini 2.0 Flash lacks comparable transparent reasoning
- When the function signatures are complex (deeply nested args) — Gemini parses docstrings as schema; complex types degrade accuracy

## Where it fails / limitations
- Automatic function calling is opaque — you cannot inspect what the model decided to call before it executes; use manual mode for auditability
- Parallel function calling is non-deterministic — order of parallel calls and which functions are called is model-decided
- `tool_config={"mode": "ANY"}` forces a function call but may choose the wrong function — always validate function name before executing
- Google Search grounding adds latency and has its own per-query cost; `dynamic_threshold` tuning is empirical
- `text-embedding-004` produces 768-dimension vectors — incompatible with indexes built for 1536d (OpenAI) or 1024d embeddings
- Gemini function calling requires type hints and docstrings on Python functions — undocumented functions may be ignored
- Rate limits on free tier are aggressive (15 RPM gemini-1.5-pro); production requires a billing account

## Agentic workflow
A Gemini subagent is best used with manual function calling (not automatic) so the orchestrating agent can log, validate, and potentially veto tool invocations before execution. Pass the function response back using `genai.protos.FunctionResponse`. For structured extraction without tool use, use `response_mime_type="application/json"` with a JSON Schema — this is simpler than function-forcing and available on all Gemini 1.5+ models. Use Google Search grounding only when the task genuinely needs current web data (news, prices, live events).

### Recommended subagents
- `faion-sdd-executor-agent` — can use Gemini for Google Search grounded research steps
- no dedicated Gemini-specific agent exists; embed Gemini calls inside general-purpose pipeline agents

### Prompt pattern
```python
import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")

# Manual function calling — auditable
def call_with_tool(user_query: str, fn) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash", tools=[fn])
    chat = model.start_chat()
    resp = chat.send_message(user_query)

    for part in resp.candidates[0].content.parts:
        if hasattr(part, "function_call"):
            fc = part.function_call
            # Validate before executing
            assert fc.name == fn.__name__, f"Unexpected tool: {fc.name}"
            result = fn(**dict(fc.args))
            # Return result to model
            follow = chat.send_message(genai.protos.Content(parts=[
                genai.protos.Part(function_response=genai.protos.FunctionResponse(
                    name=fc.name, response={"result": result}
                ))
            ]))
            return follow.text
    return resp.text
```

```python
# Structured extraction — no tool use needed
from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    topics: List[str]
    sentiment: str

model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": Article.model_json_schema()
    }
)
resp = model.generate_content("Extract from: " + article_text)
data = Article.model_validate_json(resp.text)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-generativeai` | Python SDK for Gemini API | `pip install google-generativeai` |
| `google-cloud-aiplatform` | Vertex AI SDK (enterprise Gemini) | `pip install google-cloud-aiplatform` |
| `gcloud` CLI | Auth, project config, quota management | `apt install google-cloud-cli` |
| `numpy` | Cosine similarity for embedding search | `pip install numpy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google AI Studio | SaaS | Partial | API key access; good for prototyping, not production |
| Vertex AI | SaaS | Yes | Enterprise Gemini; IAM, VPC, audit logs, higher quotas |
| Google Search (grounding) | SaaS | Yes | Built-in via `Tool.from_google_search_retrieval`; per-query cost |
| Pinecone | SaaS | Yes | Store `text-embedding-004` vectors for RAG |
| ChromaDB | OSS | Yes | Local vector store; 768d compatible with text-embedding-004 |
| LiteLLM | OSS proxy | Yes | Unified interface; routes to Gemini API with OpenAI-compatible format |

## Templates & scripts
See `templates.md` for RAG and agent loop patterns. Embedding batch helper:

```python
def embed_batch(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a list of texts. task: RETRIEVAL_DOCUMENT | RETRIEVAL_QUERY | SEMANTIC_SIMILARITY"""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=texts,
        task_type=task
    )
    return result["embedding"]

# Index documents
doc_embeddings = embed_batch(document_texts)

# Query
query_embedding = embed_batch([query], task="RETRIEVAL_QUERY")[0]
```

## Best practices
- Use `enable_automatic_function_calling=False` for agent pipelines — manual control gives you logging, validation, and the ability to abort
- Write clear, specific docstrings on every tool function — Gemini uses docstrings as tool descriptions; vague docstrings produce wrong tool selection
- Set `tool_config={"mode": "ANY", "allowed_function_names": ["fn_name"]}` to force a specific tool when you know which one the model should call
- Use `task_type="RETRIEVAL_QUERY"` for search queries and `task_type="RETRIEVAL_DOCUMENT"` for indexed docs — using the wrong type degrades retrieval quality
- Always normalize embeddings before cosine similarity computation (`np.linalg.norm`)
- Cache computed document embeddings — re-embedding on every request is expensive and unnecessary
- Set a maximum iteration count on any agent loop using Gemini tools; the model can loop indefinitely on ambiguous tasks

## AI-agent gotchas
- `enable_automatic_function_calling=True` executes your functions directly in the SDK call — if a function raises, the entire call fails with no retry
- `dict(fn_call.args)` on a Gemini FunctionCall may return `MapComposite` objects, not plain Python dicts — call `dict()` recursively or use `json_format.MessageToDict`
- Google Search grounding is not available on all Gemini models (check model card) — mixing grounding + custom tools is experimental
- `response_mime_type="application/json"` does not guarantee schema compliance — Gemini may return valid JSON that violates the schema; always validate with Pydantic
- Vertex AI and AI Studio quotas are separate — a project hitting AI Studio limits may have headroom on Vertex
- `genai.protos.Content` for function responses must wrap everything in `parts` list — omitting the list raises a cryptic proto error

## References
- https://ai.google.dev/gemini-api/docs/function-calling
- https://ai.google.dev/gemini-api/docs/grounding
- https://ai.google.dev/gemini-api/docs/embeddings
- https://ai.google.dev/gemini-api/docs/structured-output
- https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini
