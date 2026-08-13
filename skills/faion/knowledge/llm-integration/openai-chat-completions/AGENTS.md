# OpenAI Chat Completions

## Summary

**One-sentence:** Disciplined wrapper around `client.chat.completions.create` that pins model, temperature, response_format, finish-reason check, retry policy, and usage logging — so pipelines do not silently truncate, double-spend, or hit rate-limits blind.

**One-paragraph:** Complete guide to the OpenAI Chat Completions endpoint (`/v1/chat/completions`): request structure, model selection (gpt-4o vs gpt-4o-mini vs o-series), parameters (temperature, max_tokens, response_format, seed), streaming, vision (URL and base64), error handling with exponential backoff via tenacity, rate-limit headers, and cost tracking via tiktoken. The core rule: always read `finish_reason` — `"length"` means silent truncation; never parse JSON from a truncated response.

**Ефективно для:** AI/ML інженера, що збирає продакшн-агентний pipeline на OpenAI — закриває петлю між запитом, обробкою помилок та обліком вартості.

## Applies If (ALL must hold)

- Building agent pipelines calling OpenAI models (gpt-4o, gpt-4o-mini, o1, o3-mini).
- Streaming partial outputs to users or downstream pipeline steps in real time.
- Generating structured JSON via `response_format={"type": "json_object"}` (not strict-schema parse).
- Multi-image or screenshot analysis inside an automated workflow.
- Cost-sensitive pipelines where gpt-4o-mini quality is acceptable.

## Skip If (ANY kills it)

- Persistent conversation state across sessions — use Assistants API.
- Guaranteed schema compliance — use Structured Outputs (`beta.parse`), not JSON Mode.
- More than 128K context required — switch to Claude 200K or Gemini.
- Anthropic Claude is available and the task is quality-sensitive — Claude wins on long-form reasoning.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `OPENAI_API_KEY` | env var | OpenAI dashboard, vault, or 1Password |
| `model` choice | string | matched to task complexity per model table |
| `messages` array | list[dict] | pipeline upstream (system+user+optional assistant turns) |
| Token budget cap | int | pipeline cost policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/prompt-basics` | Message-role discipline upstream of the call. |
| `geek/ai/llm-integration/structured-output-basics` | Decision between `json_object` vs strict-schema `beta.parse`. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: finish_reason guard, temperature discipline, mini-first routing, async-throttle, usage logging, header pre-check | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one logged call (model, usage, finish_reason, content); valid + invalid examples; forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix: truncated-JSON, blind-retry, model-not-found, vision-cost-blowup, sequential-batch-saturation | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: pick model → build messages → set params → call with retry → check finish_reason → log usage | ~700 |
| `content/06-decision-tree.xml` | essential | Picks `json_object` vs `beta.parse`, mini vs flagship, sync vs async; references rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inner-loop-extraction` | haiku | Cheap structured fill where mini quality matches. |
| `prompt-authoring` | sonnet | Per-prompt judgment, balance cost vs reliability. |
| `error-mode-synthesis` | opus | Multi-call failure analysis when usage / costs spike. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retry-client.py` | OpenAI client wrapper with tenacity retry on RateLimitError and APIError, plus finish_reason guard. |
| `templates/encode-image.py` | Base64 image-to-data-URL helper for vision messages, with MIME detection. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-chat-completions.py` | Validate a logged-call JSON record matches the output contract (model, usage, finish_reason, content shape). | Post-call in pipeline; nightly audit of call logs. |

## Related

- [[openai-function-calling]] — strict-schema extraction via `beta.parse`.
- [[openai-embeddings]] — embedding sibling for the same SDK.
- [[structured-output-basics]] — picking JSON Mode vs Structured Outputs.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides three things from the call site: (a) gpt-4o-mini vs gpt-4o vs o-series by task class; (b) `json_object` vs `beta.parse` vs free-form; (c) sync vs async based on parallel-fan-out > 2. Use it at the top of every new pipeline stage that calls Chat Completions.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/retry-client.py`

```python
"""
import time
from openai import OpenAI, RateLimitError, APIError, BadRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

client = OpenAI()


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
def call_chat(
    messages: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    max_tokens: int = 2048,
    response_format: dict | None = None,
    seed: int | None = None,
) -> dict:
    """Call Chat Completions with retry on transient errors only."""
    if not isinstance(messages, list) or not messages:
        raise BadRequestError("messages must be a non-empty list")
    t0 = time.monotonic()
    kwargs = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if response_format is not None:
        kwargs["response_format"] = response_format
    if seed is not None:
        kwargs["seed"] = seed
    raw = client.chat.completions.with_raw_response.create(**kwargs)
    latency_ms = int((time.monotonic() - t0) * 1000)
    parsed = raw.parse()
    choice = parsed.choices[0]
    if choice.finish_reason == "length":
        raise ValueError(f"Response truncated by max_tokens={max_tokens}")
    return {
        "content": choice.message.content,
        "usage": parsed.usage.model_dump() if hasattr(parsed.usage, "model_dump") else dict(parsed.usage.__dict__),
        "finish_reason": choice.finish_reason,
        "request_id": raw.headers.get("x-request-id", ""),
        "latency_ms": latency_ms,
    }
```

### `templates/encode-image.py`

```python
"""
import base64
from pathlib import Path

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def encode_image_as_data_url(image_path: str) -> str:
    """Encode image file as base64 data URL for use in OpenAI vision requests."""
    path = Path(image_path)
    mime = MIME_TYPES.get(path.suffix.lower(), "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def encode_image_b64(image_path: str) -> tuple[str, str]:
    """Return (base64_data, mime_type) for use in Anthropic/Gemini vision requests."""
    path = Path(image_path)
    mime = MIME_TYPES.get(path.suffix.lower(), "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return b64, mime
```
