# Vision Basics

## Summary

**One-sentence:** Analyses one or more images with a VLM (GPT-4o / Claude Sonnet / Gemini Flash) and returns a typed Pydantic object with description, text_content, confidence.

**One-paragraph:** Resizes images to 1024px long edge (50-70% token reduction), base64-encodes them, sends to the chosen VLM with `response_format={"type": "json_object"}`, parses the response into a Pydantic model with retry-on-parse-error, and caches the result by sha256 of the image bytes. Includes input-method choice (URL vs base64), per-provider size cap awareness (Anthropic 5MB, OpenAI 20MB), and stateful Q&A pattern that sends the image only on the first turn.

**Ефективно для:** агента-перцептора, що читає скриншоти / скани / діаграми у пайплайні — закриває петлю між зображенням і типізованим JSON для downstream-агентів.

## Applies If (ALL must hold)

- Agent reads content from screenshots, scans, diagrams, photos, or scraped images.
- Output is consumed by a downstream agent (typed schema needed, not free text).
- Image size fits the provider cap (5 MB Anthropic / 20 MB OpenAI) after resize.
- Latency budget allows 500ms-2s per call (VLM call latency floor).
- Privacy policy permits sending image bytes to the chosen provider.

## Skip If (ANY kills it)

- Real-time video at &gt; 2 FPS — VLM latency is too high; use YOLOv11 or GroundingDINO locally.
- High-volume barcode / QR decoding — `zxing` or `python-qrcode` is 100x cheaper and deterministic.
- Pixel-level measurement — VLMs produce semantic estimates, not precise pixel values.
- Privacy-sensitive content must stay local — use Qwen2.5-VL or LLaVA via Ollama.
- Task is reducible to EXIF / file metadata — VLMs cannot see metadata; use Pillow / ExifTool.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Image source | URL, local path, or base64 string | content store / scraper / upload |
| Task description | string in the agent prompt | caller |
| Pydantic schema | class extending BaseModel | downstream consumer contract |
| Provider credentials | env: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` | secrets manager |
| Cache dir | filesystem path with rw | pipeline orchestrator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/vision-applications` | downstream patterns for OCR / classification / moderation that build on this. |
| `geek/ai/llm-integration/structured-output-basics` | Pydantic + response_format contract this methodology depends on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: resize 1024px, base64 for sensitive, label multi-image, json_object enforce, retry-on-parse, cache by image hash | ~1000 |
| `content/02-output-contract.xml` | essential | Pydantic schema + valid/invalid examples + per-provider size caps | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: oversized image, missing labels, schema drift, chart hallucination, EXIF asked of VLM | ~900 |
| `content/04-procedure.xml` | medium | 6-step procedure: validate → resize → encode → cache probe → VLM call → parse with retry | ~700 |
| `content/05-examples.xml` | medium | Worked Claude Sonnet extraction of an invoice with retry-on-bad-JSON | ~500 |
| `content/06-decision-tree.xml` | essential | Provider choice (Claude vs GPT-4o vs Gemini), URL vs base64, detail level | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `resize-encode` | haiku | Mechanical: Pillow resize + base64; no judgment. |
| `extract` | sonnet | Per-image judgment, structured Pydantic. |
| `route-provider` | sonnet | Decision-tree walk on layout complexity + size + language. |
| `cross-validate-numbers` | sonnet | Second pass for chart values when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vision_extract.py` | analyze_image_url / analyze_local_image / structured_analysis / VisualQA with Pydantic. |
| `templates/prepare_image.py` | Resize to 1024px long edge + base64 encode + media-type detection. |
| `templates/prompt-vision.txt` | Agent prompt for structured vision extraction with null-on-ambiguity rule. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-basics.py` | Validate extraction JSON against the declared Pydantic schema. | Post-VLM call, before downstream consumes. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[vision-applications]] — production patterns (OCR, classification, moderation) on top of these basics.
- [[structured-output-basics]] — Pydantic + json_object contract used everywhere.
- [[img-gen-basics]] — generator side; vision-basics verifies generated frames.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the provider (Claude for complex layouts and 200K context, GPT-4o for json_object enforcement, Gemini Flash for high-volume batch), the input mode (URL vs base64 based on sensitivity), and the detail level (`low` for classification, `high` for dense text). Use it at the extract() entry point before any provider call.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/vision_extract.py`

```python
"""Vision extraction: typed Pydantic output with retry-on-parse-error."""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel


client = OpenAI()

MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _encode_local(image_path: str) -> tuple[str, str]:
    """Read image, return (base64_data, media_type). Does NOT resize — use prepare_image for that."""
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()
    media_type = MEDIA_TYPES.get(Path(image_path).suffix.lower(), "image/jpeg")
    return data, media_type


def analyze_image_url(image_url: str, prompt: str = "Describe this image in detail.") -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]}],
    )
    return response.choices[0].message.content


def analyze_local_image(image_path: str, prompt: str = "Describe this image in detail.") -> str:
    data, media_type = _encode_local(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}},
        ]}],
    )
    return response.choices[0].message.content


class DetectedObject(BaseModel):
    name: str
    confidence: float
    description: str


class ImageAnalysis(BaseModel):
    description: str
    objects: list[DetectedObject]
    colors: list[str]
    mood: str
    text_content: Optional[str]
    tags: list[str]
    confidence: str  # "high" | "low"


def structured_analysis(image_path: str, max_retries: int = 2) -> ImageAnalysis:
    """Get structured analysis with parse-with-retry on JSON failure."""
    data, media_type = _encode_local(image_path)
    prompt = (
        "Analyze this image and return JSON with: description, objects (name, confidence 0-1, description), "
        "colors, mood, text_content (or null), tags, confidence (high|low). "
        "Set confidence to low if any field required significant interpretation."
    )
    for attempt in range(max_retries):
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}},
            ]}],
        )
        try:
            return ImageAnalysis(**json.loads(response.choices[0].message.content))
        except Exception as e:
            prompt = f"Previous response caused parse error: {e}. Return valid JSON with all required fields."
    raise ValueError("structured_analysis failed after retries")


class VisualQA:
    """Stateful visual Q&A: image included only in first turn."""

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self._history: list[dict] = []
        self._image_data: str | None = None
        self._media_type: str = "image/jpeg"

    def set_image(self, image_path: str) -> None:
        self._image_data, self._media_type = _encode_local(image_path)
        self._history = []

    def ask(self, question: str) -> str:
        if not self._image_data:
            raise ValueError("No image set. Call set_image() first.")
        if not self._history:
            # First turn: include image
            user_msg: dict = {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:{self._media_type};base64,{self._image_data}"}},
            ]}
        else:
            user_msg = {"role": "user", "content": question}
        messages = self._history + [user_msg]
        response = client.chat.completions.create(model=self.model, messages=messages)
        answer = response.choices[0].message.content
        self._history.extend([user_msg, {"role": "assistant", "content": answer}])
        return answer
```

### `templates/prepare_image.py`

```python
"""Image preprocessing: resize 1024px + base64 + media-type detection."""
from __future__ import annotations

import base64
import io

from PIL import Image

FORMAT_TO_MEDIA_TYPE = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
    "GIF": "image/gif",
}


def prepare_image(path: str, max_px: int = 1024) -> tuple[str, str]:
    """
    Resize image to max_px on long edge and base64-encode.
    Returns (base64_data, media_type).
    Call this before any VLM API request with local images.
    """
    img = Image.open(path)
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = img.format or "PNG"
    img.save(buf, format=fmt)
    data = base64.standard_b64encode(buf.getvalue()).decode()
    media_type = FORMAT_TO_MEDIA_TYPE.get(fmt, "image/png")
    return data, media_type


def check_size_mb(path: str) -> float:
    """Return file size in MB. Check before API call: Anthropic max 5MB, OpenAI max 20MB."""
    from pathlib import Path
    return Path(path).stat().st_size / (1024 * 1024)
```

### `templates/prompt-vision.txt`

```text
Analyze this image and return JSON matching the schema below.

Rules:
- If a field is not visible or ambiguous, set it to null.
- Do not infer values not present in the image.
- Set confidence to "low" if any field required significant interpretation.
- For numbers extracted from charts: always set confidence to "low" and note "chart values require cross-validation".

Schema: {{SCHEMA_JSON}}

Image task: {{TASK_DESCRIPTION}}
```
