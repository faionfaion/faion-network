# Agent Integration — Gemini Multimodal

## When to use
- Processing video natively — Gemini is the only frontier model with native video understanding (no frame extraction needed)
- Audio transcription and analysis without a separate Whisper call
- Long document pipelines — 2M token context window handles books, large codebases, multi-document sets
- Combined modality tasks: video + PDF slides, image + audio explanation, multiple images compared
- Code execution tasks where the model must compute results, not just generate code
- Enterprise Google Cloud deployments requiring CMEK, VPC Service Controls, IAM integration (Vertex AI)

## When NOT to use
- Simple text-only tasks — Gemini text quality is comparable to GPT-4o/Claude but adds SDK complexity if you're already on OpenAI/Anthropic
- When you need maximum reasoning depth — Claude Opus or o1 outperform Gemini on complex multi-step reasoning benchmarks
- Privacy-sensitive content that cannot leave on-premises — Gemini requires upload to Google servers
- Low-latency real-time voice — Gemini Live API exists but is more complex than OpenAI Realtime API
- When your team already has deep OpenAI or Anthropic expertise — switching SDK adds friction for marginal gains on text tasks

## Where it fails / limitations
- Video upload requires a polling wait loop — `video_file.state.name == "PROCESSING"` can take 30s–5min for long videos; agents must handle this asynchronously
- File uploads are not permanent — files expire after 48 hours; agents must re-upload or use GCS URIs for long-lived pipelines
- Context caching requires a minimum of 32K tokens — below this, caching is unavailable and you pay full price per call
- Code execution sandbox runs only Python, has no internet access, and has an execution time limit
- Vertex AI and Gemini Developer API have different authentication methods, SDKs, and some feature gaps

## Agentic workflow
A multimodal agent using Gemini separates file management from inference: files are uploaded once (or referenced via GCS URI), and the file reference is passed to multiple inference calls. For high-traffic document Q&A, use context caching: upload the document, create a cache, and instantiate the model from the cache so all questions reuse the cached tokens. For video analysis pipelines, implement a state machine (upload → poll → analyze) rather than blocking on the upload.

### Recommended subagents
- `faion-sdd-executor-agent` — can invoke Gemini for design document generation from uploaded architecture diagrams
- A dedicated `media-analysis-agent` that handles file upload, polling, and extraction, exposing a simple `analyze(file_path, query)` interface

### Prompt pattern
Structured extraction from any modality:
```python
response = model.generate_content([
    """Extract the following in JSON format:
    {"summary": "...", "key_points": [...], "action_items": [...]}
    Do not include keys not listed above.""",
    uploaded_file
])
```

Multi-turn document Q&A with context caching:
```python
model = genai.GenerativeModel.from_cached_content(cache)
chat = model.start_chat()
# All messages in this chat reuse cached document tokens
answer = chat.send_message("What are the payment terms?")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-generativeai` | Gemini Developer API (non-Vertex) | `pip install google-generativeai` / https://ai.google.dev |
| `vertexai` | Google Cloud Vertex AI SDK (enterprise) | `pip install vertexai` / https://cloud.google.com/vertex-ai/docs |
| `google-cloud-aiplatform` | Lower-level Vertex AI client | `pip install google-cloud-aiplatform` |
| `Pillow` | Image loading for PIL.Image objects | `pip install Pillow` |
| `gcloud` (CLI) | GCS upload, IAM, project management | https://cloud.google.com/sdk/docs/install |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Gemini Developer API | SaaS | Yes | Free tier available; genai SDK |
| Vertex AI (Gemini) | SaaS | Yes | Enterprise; IAM auth, CMEK, VPC |
| Google Cloud Storage | SaaS | Yes | Use GCS URIs instead of uploads for large/persistent files |
| Firebase App Check | SaaS | Partial | Mobile-facing; not for server-to-server agent calls |
| Google AI Studio | SaaS | Partial | Web UI for prototyping; not for production agent calls |

## Templates & scripts
See `templates.md` for context caching and Vertex AI patterns. Video analysis with async polling:

```python
import time
import google.generativeai as genai

def analyze_video(path: str, query: str, model_name="gemini-1.5-pro") -> str:
    file = genai.upload_file(path)
    # Poll until processing complete
    for _ in range(60):  # 5-minute max wait
        file = genai.get_file(file.name)
        if file.state.name == "ACTIVE":
            break
        if file.state.name == "FAILED":
            raise RuntimeError(f"Video processing failed: {file.name}")
        time.sleep(5)
    else:
        raise TimeoutError("Video processing timed out")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([query, file])
    return response.text
```

## Best practices
- Use GCS URIs (`gs://bucket/file.mp4`) instead of uploading via SDK for large files — faster, no re-upload if file already exists in GCS
- Set TTL on context caches to match your query pattern — 1 hour for interactive sessions, 24 hours for batch jobs
- Use `gemini-2.0-flash` for fast, cheap multimodal tasks; `gemini-1.5-pro` for long video and complex reasoning
- Specify output format explicitly in the prompt (JSON, markdown table, bullet list) — Gemini follows format instructions reliably
- For PDF extraction, prefer Gemini over custom PDF parsers — it handles tables, images, and multi-column layouts natively
- Handle the 48-hour file expiry: store `file.name` in a DB with upload timestamp and re-upload if expired
- For code execution, inspect `part.executable_code` and `part.code_execution_result` separately — they are distinct content parts

## AI-agent gotchas
- File upload is not idempotent — uploading the same file twice creates two separate file objects; cache file names to avoid duplicate uploads
- The polling loop must have a max-iteration guard — a stuck "PROCESSING" state will loop forever without it
- `model.generate_content()` is synchronous; for concurrent agent workers, use `asyncio` with `aiohttp` or the async Vertex SDK
- Context cache requires a minimum of 32K tokens — if your document is smaller, caching raises an error; check token count before creating
- Gemini's 2M context window tempts agents to stuff everything in one call — but cost is linear with tokens; use retrieval for large corpora
- Code execution results may be truncated for long-running computations; the sandbox has execution time limits (~30s)
- Vertex AI auth uses Application Default Credentials (`gcloud auth application-default login`) — different from `GOOGLE_API_KEY` used by the Gemini Developer API

## References
- https://ai.google.dev/docs (Gemini Developer API)
- https://cloud.google.com/vertex-ai/generative-ai/docs (Vertex AI)
- https://github.com/google-gemini/gemini-api-cookbook
- https://ai.google.dev/gemini-api/docs/caching (context caching)
- https://ai.google.dev/gemini-api/docs/code-execution (code execution)
