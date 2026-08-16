# OpenAI Function Calling and Structured Outputs

## Summary

**One-sentence:** Disciplined caller for `client.chat.completions.create(tools=...)` and `client.beta.chat.completions.parse(response_format=Model)` — handles message order, parallel-tool coherence, refusals, and tool_choice gating.

**One-paragraph:** OpenAI-specific patterns for function calling (tool use), Pydantic-validated structured extraction via `client.beta.chat.completions.parse`, parallel tool calls, and multimodal extensions (DALL-E 3, Whisper, TTS). Primary distinction from generic tool use: structured outputs enforce schema compliance at the API level, not just by prompt instruction. Pipelines that drive external actions (writes, payments) must validate parallel tool calls for coherence before execution.

**Ефективно для:** AI-інженера, що під'єднує LLM до зовнішніх дій — закриває цикл tool_call → execute → result із гарантією схеми та порядку повідомлень.

## Applies If (ALL must hold)

- Reliable, schema-validated JSON extraction from unstructured text.
- Pipeline driving external actions (API calls, DB writes) triggered by model decisions.
- Multiple tools needed in one response (parallel tool calls) to cut round-trips.
- Image generation (DALL-E 3), speech-to-text (Whisper), or TTS alongside text LLM calls.
- Strict output enforcement where `json_object` mode alone is insufficient.

## Skip If (ANY kills it)

- Only need a JSON blob without schema strictness — `response_format={"type": "json_object"}` is simpler.
- Simple prompting + regex post-processing is sufficient.
- Schema is deeply nested (&gt;10 params) and the model mis-selects — simplify the schema first.
- Real-time audio generation at sub-200ms latency — TTS streaming is not suitable.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pydantic model | Python class | pipeline schema layer |
| Tool registry | dict[name, callable] | pipeline tools module |
| `OPENAI_API_KEY` | env var | vault / 1Password |
| Model id | string | gpt-4o or newer (parse requires it) |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/openai-chat-completions` | Base SDK patterns (retry, finish_reason). |
| `geek/ai/llm-integration/tool-use-basics` | Generic tool-loop discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: message-order, parse-on-gpt-4o, refusal null-check, parallel-coherence, tool_choice gates, register-then-call | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for one parse-record (model, parsed, refusal, tool_calls) + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair: wrong-order, refusal-ignored, parallel-contradiction, parse-on-old-model, missing-tool-result | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: define tools/model → call → branch tool_calls vs parsed → execute → append → final call | ~700 |
| `content/06-decision-tree.xml` | essential | Picks parse vs json_object vs free-form; tool_choice required vs auto | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-tool-schema` | sonnet | Per-domain tool schema authorship; balance verbosity with selection accuracy. |
| `extract-structured` | haiku | Per-call extraction with parse + Pydantic. |
| `audit-parallel-calls` | opus | Cross-call coherence when parallel writes contradict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pydantic-extraction.py` | Full structured-extraction caller with refusal handling and retry. |
| `templates/whisper-chunked.py` | Whisper transcription helper for &gt;25MB audio (chunked upload). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-function-calling.py` | Validate a parse/tool-call record JSON matches the output contract. | Post-call in pipeline; nightly audit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[openai-chat-completions]] — base SDK pattern.
- [[tool-use-basics]] — generic tool-loop discipline (provider-agnostic).
- [[structured-output-patterns]] — when parse is overkill.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks (a) `parse` vs `json_object` vs free-form by strictness need, (b) `tool_choice=required` vs `auto` by whether the pipeline depends on a tool result, and (c) parallel vs sequential by whether tool effects are commutative. Use it at every tool-using call site.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pydantic-extraction.py`

```python
"""
from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
import json
from openai import OpenAI

T = TypeVar('T', bound=BaseModel)


def extract(
    client: OpenAI,
    text: str,
    output_class: Type[T],
    model: str = "gpt-4o",
    max_retries: int = 3,
) -> Optional[T]:
    """Extract structured data using OpenAI Structured Outputs.

    Falls back to json_object mode if parse raises (model not supported).
    Returns None after max_retries exhausted — never raises.
    """
    for attempt in range(max_retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[{"role": "user", "content": text}],
                response_format=output_class,
            )
            msg = response.choices[0].message
            if msg.refusal:
                return None
            return msg.parsed
        except NotImplementedError:
            # Model does not support Structured Outputs — use JSON mode
            schema = output_class.model_json_schema()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": f"Return valid JSON matching: {json.dumps(schema)}"},
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )
            try:
                data = json.loads(response.choices[0].message.content)
                return output_class(**data)
            except (json.JSONDecodeError, ValidationError):
                pass
        except (json.JSONDecodeError, ValidationError):
            pass
    return None
```

### `templates/whisper-chunked.py`

```python
"""
import subprocess
import tempfile
import os
from pathlib import Path
from openai import OpenAI


def transcribe_large(
    client: OpenAI,
    audio_path: str,
    chunk_minutes: int = 10,
    prompt: str = "",
) -> str:
    """Transcribe large audio file by splitting into chunks.

    Args:
        audio_path: Path to audio file (any ffmpeg-supported format).
        chunk_minutes: Duration of each chunk in minutes.
        prompt: Proper noun hints repeated on every chunk for consistency.
    Returns:
        Full transcript as a single joined string.
    """
    chunks_dir = tempfile.mkdtemp()
    chunk_pattern = os.path.join(chunks_dir, "chunk_%03d.mp3")

    subprocess.run([
        "ffmpeg", "-i", audio_path,
        "-f", "segment", "-segment_time", str(chunk_minutes * 60),
        "-c", "copy", chunk_pattern,
    ], check=True, capture_output=True)

    parts = []
    for chunk in sorted(Path(chunks_dir).glob("chunk_*.mp3")):
        with open(chunk, "rb") as f:
            kwargs = {"model": "whisper-1", "file": f}
            if prompt:
                kwargs["prompt"] = prompt  # repeat hint on every chunk
            parts.append(client.audio.transcriptions.create(**kwargs).text)

    return " ".join(parts)
```
