# Gemini API Integration

## Summary

**One-sentence:** Produces a production Google Gemini API client wiring up streaming, function calling, multimodal input (image/audio/video), context caching, and Live API for real-time voice/video sessions.

**One-paragraph:** Produces a production-ready Google Gemini API client. Models: Gemini 3 Pro/Flash (1M+ context, dynamic thinking), Gemini 2.0 Flash (fast, agentic), Gemini 1.5 Pro (2M context). Key differentiators: native video/audio input, Live API for real-time voice/video, code execution sandbox, Google Search grounding, context caching (75% cost reduction on repeated context). Standardises retry/backoff, structured-output JSON mode, safety settings, and cache-key pattern.

**Ефективно для:** Бекенд-розробник для multimodal feature — за один прохід отримує client.py з streaming + caching + safety.

## Applies If (ALL must hold)

- Building an LLM integration where Gemini is the chosen provider (or one of several).
- Need at least one of: long context (>200k tokens), multimodal input (image/audio/video), Google Search grounding, code execution.
- Production deployment — needs retry, backoff, structured output, safety controls.
- Caching repeated context (system prompts >1024 tokens) is worthwhile economically.
- Real-time voice/video session use case (Live API) is in scope.

## Skip If (ANY kills it)

- Pure text LLM use case with no Gemini-specific differentiators — pick whichever provider is cheaper.
- Latency-critical interactive UI with sub-200ms target — Gemini Flash but not Pro.
- Strict data-residency outside Google's regions — verify region map.
- No Google Cloud / API key access — out of scope.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| API key | env var GOOGLE_API_KEY | ops |
| Model choice | string (gemini-3-pro / gemini-3-flash / ...) | ML lead |
| Use-case profile | yaml | product |
| Safety settings policy | yaml | trust+safety |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-decision-framework` | Selects Gemini as the provider. |
| `geek/ai/ml-engineer/llm-observability-stack` | Traces every Gemini call for cost / latency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: wire-client → enable-streaming → add-tools → wire-cache → wire-safety. | ~700 |
| `content/06-decision-tree.xml` | essential | Branch by model variant + caching + Live API. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-client` | haiku | Fill gemini-client.py from inputs. |
| `integrate-feature` | sonnet | Wire one Gemini-specific feature (cache, search grounding, code exec). |
| `debug-live-api` | opus | Real-time voice/video session debugging — cross-cutting. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gemini-client.py` | Production client: retry, streaming, function calling, structured output. |
| `templates/gemini-multimodal.py` | Image / audio / video input variants. |
| `templates/gemini-cache.py` | Context cache create + reuse pattern. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gemini-api.py` | Validate the client config (model, safety, cache_ttl, structured_output_schema). | Pre-merge of every Gemini-client PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[llm-decision-framework]] — provider choice.
- [[llm-observability-stack]] — tracing surface.
- [[claude-api]] — sibling provider methodology.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks Gemini variant (3 Pro / 3 Flash / 2.0 Flash / 1.5 Pro) + caching strategy + Live-API toggle.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/gemini-client.py`

```python
"""

"""
Production Gemini client: model setup, retry logic, streaming, function calling.
Requires: pip install google-generativeai
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Callable

import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, ResourceExhausted

logger = logging.getLogger(__name__)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def create_model(
    model_name: str = "gemini-2.0-flash",
    system_instruction: str | None = None,
    temperature: float = 1.0,
    tools: list[Callable] | None = None,
) -> genai.GenerativeModel:
    """Create a configured Gemini model instance."""
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        tools=tools,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 8192,
        },
    )


def generate_with_retry(
    model: genai.GenerativeModel,
    prompt: str,
    max_retries: int = 3,
) -> str | None:
    """Generate content with exponential backoff on rate limit errors."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            # Safety check — blocked responses have no .text
            if response.prompt_feedback.block_reason:
                logger.warning("Response blocked: %s", response.prompt_feedback.block_reason)
                return None
            return response.text

        except ResourceExhausted:
            wait = 2 ** attempt
            logger.warning("Rate limited, retry %d/%d in %ds", attempt + 1, max_retries, wait)
            time.sleep(wait)

        except InvalidArgument as exc:
            logger.error("Invalid request: %s", exc)
            return None

        except Exception as exc:
            logger.exception("Unexpected error on attempt %d", attempt + 1)
            if attempt == max_retries - 1:
                return None

    return None


class GeminiChat:
    """Multi-turn chat session with streaming support."""

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        system_instruction: str | None = None,
    ) -> None:
        self.model = create_model(model_name, system_instruction)
        self._chat = self.model.start_chat()

    def send(self, message: str) -> str | None:
        """Send message and return full response text."""
        response = self._chat.send_message(message)
        if response.prompt_feedback.block_reason:
            return None
        return response.text

    def stream(self, message: str):
        """Send message and yield response chunks as they arrive."""
        response = self._chat.send_message(message, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def history(self) -> list[dict]:
        """Return conversation history as list of {role, content} dicts."""
        return [
            {"role": msg.role, "content": msg.parts[0].text}
            for msg in self._chat.history
            if msg.parts
        ]

    def reset(self) -> None:
        """Start a fresh conversation."""
        self._chat = self.model.start_chat()


class GeminiFunctionAgent:
    """Agent with automatic function calling (Gemini auto-executes registered tools)."""

    def __init__(
        self,
        tools: list[Callable],
        model_name: str = "gemini-2.0-flash",
        system_instruction: str | None = None,
        max_iterations: int = 10,
    ) -> None:
        self.max_iterations = max_iterations
        self.model = create_model(model_name, system_instruction, tools=tools)

    def run(self, query: str) -> str | None:
        """Run agent query with automatic function dispatch."""
        chat = self.model.start_chat(enable_automatic_function_calling=True)

        for _ in range(self.max_iterations):
            response = chat.send_message(query)
            # If no more function calls pending, return final text
            has_function_call = any(
                hasattr(part, "function_call")
                for part in response.candidates[0].content.parts
            )
            if not has_function_call:
                return response.text

        logger.warning("Max iterations (%d) reached", self.max_iterations)
        return None


# ── Example tools for GeminiFunctionAgent ─────────────────────────────────────

def get_weather(location: str, unit: str = "celsius") -> dict[str, Any]:
    """Get current weather for a location.

    Args:
        location: City and country, e.g. 'Tokyo, Japan'
        unit: Temperature unit, 'celsius' or 'fahrenheit'
    """
    return {"location": location, "temperature": 22, "unit": unit, "condition": "sunny"}


def calculator(expression: str) -> dict[str, Any]:
    """Evaluate a mathematical expression safely.

    Args:
        expression: Math expression to evaluate, e.g. '2 + 2 * 3'
    """
    try:
        result = eval(expression, {"__builtins__": {}})  # noqa: S307
        return {"result": result}
    except Exception as exc:
        return {"error": str(exc)}


# Usage:
# agent = GeminiFunctionAgent(tools=[get_weather, calculator])
# result = agent.run("What is 15*23 and what is the weather in Tokyo?")
```

### `templates/gemini-multimodal.py`

```python
"""

"""
Gemini multimodal helpers: image analyzer, video analyzer, document processor.
Requires: pip install google-generativeai pillow
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


class ImageAnalyzer:
    """Analyze images with Gemini vision."""

    def __init__(self, model_name: str = "gemini-2.0-flash") -> None:
        import PIL.Image  # noqa: PLC0415
        self._pil = PIL.Image
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, image_path: str, prompt: str) -> str:
        """Run arbitrary prompt against an image."""
        image = self._pil.open(image_path)
        response = self.model.generate_content([prompt, image])
        return response.text

    def describe(self, image_path: str) -> str:
        """Return detailed description of image contents."""
        return self.analyze(image_path, "Describe this image in detail. Include objects, colors, composition, and any text visible.")

    def extract_text(self, image_path: str) -> str:
        """OCR: extract all text from image."""
        return self.analyze(image_path, "Extract all text visible in this image. Return plain text, preserving line breaks.")

    def compare(self, image_paths: list[str], prompt: str) -> str:
        """Compare multiple images with a custom prompt."""
        images = [self._pil.open(p) for p in image_paths]
        response = self.model.generate_content([prompt, *images])
        return response.text


class VideoAnalyzer:
    """Analyze video files with Gemini (via File API)."""

    def __init__(self, model_name: str = "gemini-1.5-pro") -> None:
        self.model = genai.GenerativeModel(model_name)
        self._cache: dict[str, genai.File] = {}

    def upload(self, video_path: str) -> genai.File:
        """Upload video and wait for processing to complete."""
        if video_path in self._cache:
            return self._cache[video_path]

        video_file = genai.upload_file(video_path)
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name != "ACTIVE":
            raise RuntimeError(f"Video processing failed: {video_file.state.name}")

        self._cache[video_path] = video_file
        return video_file

    def analyze(self, video_file: genai.File, prompt: str) -> str:
        """Run prompt against uploaded video file."""
        response = self.model.generate_content([prompt, video_file])
        return response.text

    def summarize(self, video_path: str) -> str:
        """Upload and summarize video."""
        f = self.upload(video_path)
        return self.analyze(f, "Summarize this video. Include key points, main scenes, and overall message.")

    def transcribe(self, video_path: str) -> str:
        """Transcribe all spoken words in video."""
        f = self.upload(video_path)
        return self.analyze(f, "Transcribe all spoken words in this video. Include speaker labels if multiple speakers.")


class DocumentProcessor:
    """Process PDFs and documents with Gemini."""

    def __init__(self, model_name: str = "gemini-1.5-pro") -> None:
        self.model = genai.GenerativeModel(model_name)
        self._file_cache: dict[str, genai.File] = {}

    def upload(self, file_path: str) -> genai.File:
        """Upload document (caches by path)."""
        if file_path in self._file_cache:
            return self._file_cache[file_path]
        file = genai.upload_file(file_path)
        self._file_cache[file_path] = file
        return file

    def process(self, file_path: str, prompt: str) -> str:
        """Run custom prompt against document."""
        file = self.upload(file_path)
        response = self.model.generate_content([prompt, file])
        return response.text

    def summarize(self, file_path: str, length: str = "medium") -> str:
        """Summarize document. length: 'short'|'medium'|'long'."""
        lengths = {
            "short": "in 2-3 sentences",
            "medium": "in 1-2 paragraphs with key points",
            "long": "in detail covering all major sections",
        }
        instruction = lengths.get(length, lengths["medium"])
        return self.process(file_path, f"Summarize this document {instruction}.")

    def extract_structured(self, file_path: str, schema: dict[str, Any]) -> str:
        """Extract structured JSON from document per schema."""
        json_model = genai.GenerativeModel(
            model_name=self.model._model_name,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )
        file = self.upload(file_path)
        response = json_model.generate_content(["Extract the required fields from this document:", file])
        return response.text

    def answer(self, file_path: str, question: str) -> str:
        """Answer a question about the document."""
        return self.process(file_path, f"Based on this document, answer: {question}")


# Usage:
# img = ImageAnalyzer(); print(img.describe("photo.jpg"))
# vid = VideoAnalyzer(); print(vid.summarize("meeting.mp4"))
# doc = DocumentProcessor(); print(doc.summarize("report.pdf", length="short"))
```

### `templates/gemini-cache.py`

```python
"""

# Stub — see methodology AGENTS.md ## Templates table.
```
