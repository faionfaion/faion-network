# Agent Integration — Gemini API Integration

## When to use
- The pipeline needs a 1M+ token context window to process entire codebases, long transcripts, or video in one shot
- Multimodal input (text + image + audio + video) in a single API call is required
- The project is already in the Google Cloud ecosystem and Vertex AI integration is preferred
- Cost at scale is the primary constraint and Gemini 1.5 Flash pricing wins over alternatives
- YouTube/video content analysis is in scope (upload via Files API then analyze)

## When NOT to use
- The task is pure text and latency is critical — OpenAI gpt-4o-mini or Claude Haiku are faster at P50
- Regulatory compliance requires Anthropic or Azure OpenAI (some regulated industries exclude Google AI)
- Grounding (Google Search) adds cost that is not justified by the task; use a separate web-search tool instead
- You need fine-tuning — Gemini fine-tuning is region-restricted and limited compared to OpenAI's offering
- The agent already uses Claude's Anthropic SDK; mixing providers adds complexity without clear benefit

## Where it fails / limitations
- File uploads (video/audio) are asynchronous; agents that do not poll `state.name == "PROCESSING"` will call the model before the file is ready and get errors
- Safety filters block responses without raising a Python exception unless explicitly checked — silent failures produce empty content
- Google Search grounding nearly doubles cost per query; agents that enable it unconditionally blow budgets
- Region restrictions apply: some Gemini features (Grounding, Code Execution) are unavailable outside US/EU
- `google-generativeai` SDK is being superseded by `google-genai` (v0.8+); mixing the two in one codebase causes import conflicts

## Agentic workflow
A subagent driving Gemini integration should first determine whether the task is multimodal or text-only to select Flash vs. Pro, then upload any binary files via the Files API and poll until ready before constructing the prompt. For long-context document analysis, the subagent should check if chunking is needed (>900K tokens after encoding) or if the full document fits. Function calling loops should cap iteration at a configurable limit (default 10) to prevent infinite tool calls.

### Recommended subagents
- `faion-sdd-executor-agent` — scaffold Gemini service class, unit tests, and retry logic as SDD tasks
- General-purpose research agent — use Gemini's 1M context to analyze entire codebases for architecture reviews

### Prompt pattern
```
Use Gemini 1.5 Pro with the Files API to analyze the uploaded video.
Upload the file, poll until state == ACTIVE, then answer: {question}.
Return structured JSON with keys: summary, key_points, timestamps.
```

```
Configure a Gemini 1.5 Flash model with safety settings BLOCK_MEDIUM_AND_ABOVE for all harm categories.
Generate a response to: {prompt}. Check response.prompt_feedback.block_reason before accessing response.text.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install google-generativeai` | Python SDK (legacy, still works) | [pypi](https://pypi.org/project/google-generativeai/) |
| `pip install google-genai` | New unified Python SDK (v0.8+) | [pypi](https://pypi.org/project/google-genai/) |
| `gcloud` | Authenticate for Vertex AI, manage projects | [cloud.google.com/sdk](https://cloud.google.com/sdk) |
| `yt-dlp` | Download YouTube videos before uploading to Files API | `pip install yt-dlp` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google AI Studio | SaaS | Yes | API key auth; free tier available; not for production PII |
| Vertex AI (Google Cloud) | SaaS | Yes | Enterprise compliance, IAM auth, VPC-SC support |
| Google AI Gemini API | SaaS | Yes | Direct REST or SDK; supports Files API for large uploads |
| Firebase Genkit | OSS | Yes | Flow-based orchestration with Gemini plugins; TypeScript/Go |
| Gemini Cookbook (GitHub) | OSS | Yes | Reference implementations; check for up-to-date SDK usage |

## Templates & scripts
Inline polling script for file uploads (≤30 lines):
```python
import time
import google.generativeai as genai

def upload_and_wait(path: str, mime_type: str = None):
    """Upload file to Gemini Files API and wait for processing."""
    f = genai.upload_file(path, mime_type=mime_type)
    for _ in range(60):  # max 5 min
        if f.state.name == "ACTIVE":
            return f
        if f.state.name == "FAILED":
            raise RuntimeError(f"File upload failed: {f.name}")
        time.sleep(5)
        f = genai.get_file(f.name)
    raise TimeoutError(f"File not ready after 5 min: {f.name}")
```

## Best practices
- Always configure `generation_config.max_output_tokens` explicitly; the default is unlimited and causes runaway costs
- Use `gemini-1.5-flash` for classification, extraction, and simple Q&A; reserve Pro for complex reasoning or >128K contexts
- Enable context caching (`genai.CachedContent`) when the same large document is queried multiple times in a session — 75% token cost reduction
- Check `response.prompt_feedback.block_reason` before accessing `response.text`; accessing `.text` on a blocked response raises `ValueError`
- Use `response.usage_metadata` to log `prompt_token_count` and `candidates_token_count` for every call; Gemini's 1M context makes it easy to accidentally send huge prompts

## AI-agent gotchas
- File expiry: uploaded files via the Files API expire after 48 hours; agents that cache file handles across sessions will fail silently — store file names, not handles, and re-upload if expired
- Parallel tool calls: Gemini supports function calling but does not guarantee the same parallel-execution semantics as OpenAI; test multi-tool responses explicitly
- JSON mode (`response_mime_type: "application/json"`) does not guarantee schema compliance without also setting `response_schema`; always validate the parsed object
- Human checkpoint needed before any action that uses Code Execution (Gemini can run Python inside the model); results are non-deterministic and may affect external state if the code calls APIs
- Grounding with Google Search is a separate pricing tier; an agent that enables it by default without surfacing cost to the user is a common budget blowout pattern

## References
- [Gemini API docs](https://ai.google.dev/docs)
- [Google AI Python SDK (google-generativeai)](https://github.com/google/generative-ai-python)
- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
- [Vertex AI Gemini](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini)
- [Files API reference](https://ai.google.dev/api/files)
