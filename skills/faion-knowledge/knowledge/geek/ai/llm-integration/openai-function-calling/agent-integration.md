# Agent Integration — OpenAI Function Calling & Structured Outputs

## When to use
- You need reliable, schema-validated JSON extraction from unstructured text (use `client.beta.chat.completions.parse` with Pydantic)
- The pipeline drives external actions (API calls, DB writes) triggered by model decisions; function calling provides a clean interface boundary
- Multiple tools may be needed in a single model response (parallel tool calls) to reduce round-trips
- You need image generation (DALL-E 3), speech-to-text (Whisper), or text-to-speech (TTS) alongside text LLM calls in one OpenAI-integrated pipeline
- Strict output format enforcement is required and `json_object` mode alone is insufficient

## When NOT to use
- You only need a JSON blob and do not care about schema strictness — `response_format={"type": "json_object"}` is simpler
- The workflow is simple enough that structured prompting + regex post-processing is sufficient
- The function schema is so complex (deeply nested objects, >10 parameters) that the model frequently misselects or misformats arguments — simplify the schema first
- You need real-time audio generation — TTS streaming exists but is not suitable for sub-200ms latency requirements

## Where it fails / limitations
- `client.beta.chat.completions.parse` (Pydantic structured output) is only available on `gpt-4o` and `gpt-4o-mini`; calling it on `gpt-3.5-turbo` raises `NotImplementedError`
- DALL-E 3 rewrites prompts via `revised_prompt`; the model may significantly change the intended composition — log `revised_prompt` and compare to original
- DALL-E 3 image URLs expire after 1 hour; agents that store URLs instead of downloading and saving images immediately will have broken links in storage
- Parallel tool calls: the model may batch two contradictory tool calls (e.g., create and delete the same resource); agents must validate tool call coherence before executing
- Whisper has a 25MB file size limit; agents processing long audio must chunk the file with overlap to avoid transcript discontinuities at chunk boundaries

## Agentic workflow
A subagent using OpenAI function calling should: define Pydantic models for structured extraction, use `client.beta.chat.completions.parse` for data extraction tasks, and use the standard tool-calling loop for action-oriented tasks. For multi-modal pipelines (text → image → TTS), the subagent should pipeline DALL-E and TTS calls asynchronously after the text generation completes to minimize total latency. Whisper transcription should be wrapped with automatic chunking for files >20MB.

### Recommended subagents
- `faion-sdd-executor-agent` — implement function schema registry, parallel tool execution, and Pydantic extraction pipeline as SDD tasks
- General-purpose subagent — use structured output parsing to extract typed data from documents, emails, or database records

### Prompt pattern
```
Extract the following fields from the text using the Person Pydantic model.
Required fields: name, age, email. Optional: addresses.
If a field is missing, use None. Return the parsed object.
Text: {text}
```

```
You have {count} tools available. Execute them in parallel when independent.
After parallel execution, reason about the combined results.
Tools: {tool_names}
User request: {request}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pip install openai` | OpenAI SDK (includes DALL-E, Whisper, TTS, structured output) | [pypi](https://pypi.org/project/openai/) |
| `pip install pydantic` | Schema definition for `client.beta.chat.completions.parse` | [pypi](https://pypi.org/project/pydantic/) |
| `ffmpeg` | Split audio files >25MB for Whisper chunking | system / [ffmpeg.org](https://ffmpeg.org) |
| `yt-dlp` | Download audio from YouTube for Whisper transcription | `pip install yt-dlp` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Chat Completions | SaaS | Yes | Function calling, parallel tools, structured output |
| OpenAI Images (DALL-E 3) | SaaS | Yes | Agents generate images; download immediately (URL expires 1h) |
| OpenAI Audio (Whisper) | SaaS | Yes | Transcription + translation; 25MB limit; $0.006/min |
| OpenAI Audio (TTS) | SaaS | Yes | 6 voices; streaming support; $15-30/1M chars |
| Azure OpenAI | SaaS | Yes | Same function calling API; enterprise compliance; VNet support |
| Instructor (PyPI) | OSS | Yes | Pydantic wrapper for OpenAI + Anthropic; cleaner than `parse` |

## Templates & scripts
See `templates.md` for complete tool loop, Pydantic extraction, and DALL-E generation templates.

Inline Whisper chunked transcription (≤30 lines):
```python
import subprocess, tempfile, os
from pathlib import Path

def transcribe_large(client, audio_path: str, chunk_min: int = 10) -> str:
    """Transcribe audio file >25MB by splitting into chunks."""
    chunks_dir = tempfile.mkdtemp()
    chunk_pattern = os.path.join(chunks_dir, "chunk_%03d.mp3")
    subprocess.run([
        "ffmpeg", "-i", audio_path, "-f", "segment",
        "-segment_time", str(chunk_min * 60),
        "-c", "copy", chunk_pattern
    ], check=True, capture_output=True)

    parts = []
    for chunk in sorted(Path(chunks_dir).glob("chunk_*.mp3")):
        with open(chunk, "rb") as f:
            parts.append(client.audio.transcriptions.create(model="whisper-1", file=f).text)
    return " ".join(parts)
```

## Best practices
- Use `client.beta.chat.completions.parse` (Pydantic structured output) over `json_object` mode for any schema with required fields; it enforces field presence at the API level
- For DALL-E 3: always download and store the image within 60 minutes of generation; URL expiry is a frequent agent failure point
- Specify `timestamp_granularities=["word"]` in Whisper only when you need word-level alignment; it doubles response size and latency for normal transcription
- When using parallel tool calls, sort tool results by `tool_call_id` before appending to messages — the order matters for the model's next reasoning step
- Pin DALL-E model to `dall-e-3` explicitly; `dall-e-2` is still the default in some SDK versions and produces lower quality output

## AI-agent gotchas
- `response.choices[0].message.parsed` is `None` if the model refused to fill the schema (e.g., safety filter); check `message.refusal` before accessing `parsed`
- DALL-E 3 `revised_prompt` can introduce content that was not in the original prompt; agents generating images for brand content must log both original and revised prompts for review
- TTS voice characteristics vary significantly by model (`tts-1` vs. `tts-1-hd`); do not switch models mid-conversation — the voice changes noticeably and breaks user experience
- Whisper `prompt` parameter (hints for proper nouns) affects only the first segment in chunked transcription; repeat the prompt for each chunk to maintain consistency
- Human checkpoint before using function calling to write to production databases or send messages; the model selects which function to call based on natural language intent, which can be ambiguous — always show the user what action will be taken before executing

## References
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI Images API](https://platform.openai.com/docs/api-reference/images)
- [OpenAI Audio API (Whisper)](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI TTS API](https://platform.openai.com/docs/guides/text-to-speech)
- [Instructor library (Pydantic + LLMs)](https://github.com/jxnl/instructor)
