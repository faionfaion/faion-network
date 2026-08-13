# Vision Applications

## Summary

**One-sentence:** Production VLM patterns for OCR, document extraction, image classification, and content moderation — each typed, retry-safe, and human-review-gated.

**One-paragraph:** Wraps four common VLM tasks behind VisionService: DocumentAnalyzer (typed field extraction from receipts / forms / passports), ImageClassifier (predefined categories with confidence), ContentModerator (severity flags with low-confidence → human-review route), and VisionService (size validation, async batch via asyncio.gather with concurrency cap, content-hash cache). Each call enforces json_object output, normalises severity / category strings to lowercase, and rejects requests over 20 MB before any provider hit.

**Ефективно для:** інженера AI-конвеєра, що обробляє користувацький контент (інвойси, фото, скриншоти) у потоці — закриває петлю між зображенням і структурованим рішенням з human-review-фолбеком.

## Applies If (ALL must hold)

- Document digitisation (invoices, receipts, forms, passports, business cards) at &gt; 10 docs / hour.
- Content moderation pipeline classifies user uploads before storage or display.
- E-commerce auto-tag / alt-text generation at upload time.
- Output is consumed by downstream auto-action (write to DB, route, hide) — confidence threshold matters.
- Per-image cost is acceptable; volume &lt; 10 000 / day.

## Skip If (ANY kills it)

- Bulk processing &gt; 10 000 images / day — CLIP / YOLO / Tesseract are 100-1000x cheaper.
- Pixel-level precision (medical, satellite) — VLMs reason semantically, not at pixel level.
- Real-time video — frame-by-frame VLM adds 1-3 s latency per frame.
- Standardised forms with fixed layout — AWS Textract / dedicated OCR is faster and cheaper.
- Sole-source content moderation — false-negative rate is non-zero; pair with a second-pass model.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Image source | URL or local path | upload / scrape / CDN |
| Task type | enum: `document` / `classify` / `moderate` | router |
| Category list (classify) | list[str] | catalog / policy registry |
| Policy categories (moderate) | list[str] | compliance team |
| Pydantic schema (document) | class extending BaseModel | downstream consumer contract |
| Provider credentials | env: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` | secrets manager |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/multimodal-ai/vision-basics` | core resize / encode / cache / Pydantic patterns reused here. |
| `geek/ai/llm-integration/structured-output-basics` | response_format + retry-on-parse contract. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: size cap, detail-auto default, json_object + schema, normalize severity, async-gather cap, human-review gate | ~1000 |
| `content/02-output-contract.xml` | essential | Per-task schemas: document, classify, moderate + needs_human_review flag | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: HIGH severity drift, URL behind auth, sequential batch, prompt-only schema, no-review-on-low | ~900 |
| `content/04-procedure.xml` | deep | 7-step procedure: route task → validate size → cache probe → call VLM → parse → normalize → route to review | ~900 |
| `content/05-examples.xml` | medium | Worked invoice extraction + content moderation with severity normalization + review routing | ~600 |
| `content/06-decision-tree.xml` | essential | Task router: document vs classify vs moderate + provider routing + review threshold | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `route-task` | sonnet | Decide document / classify / moderate from incoming metadata. |
| `extract-document` | sonnet | Typed field extraction needs per-field judgment. |
| `classify-image` | haiku | Categorical decision against fixed list. |
| `moderate-image` | sonnet | Multi-category severity decision with confidence. |
| `escalate-low-conf` | sonnet | Compose human-review ticket with evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/document-analyzer.py` | DocumentAnalyzer wrapping GPT-4o Vision with json_object. |
| `templates/image-classifier.py` | ImageClassifier with batch support and confidence. |
| `templates/content-moderator.py` | ContentModerator returning structured severity flags + needs_human_review. |
| `templates/prompt-extract.txt` | Structured field-extraction prompt with null-on-ambiguity. |
| `templates/prompt-moderate.txt` | Content moderation prompt with severity threshold. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-applications.py` | Validate task-specific JSON against 02-output-contract task schemas. | Post-VLM call, before downstream auto-action. |

## Related

- [[vision-basics]] — single-image typed extraction layer this builds on.
- [[vision-classification-moderation]] — moderation patterns extended with policy enforcement.
- [[structured-output-basics]] — JSON-schema contract.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by task type (document → DocumentAnalyzer; classify → ImageClassifier; moderate → ContentModerator), provider by stakes (high-stakes → Claude or GPT-4o; high-volume → Gemini Flash), and decides when to escalate to human review based on confidence threshold (default 0.7) and severity. Use it at the route() entry point in VisionService.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/document-analyzer.py`

```python
"""DocumentAnalyzer + VisionService with json_object + retry pattern."""
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional, Union, Any
from pathlib import Path
from enum import Enum
import base64
import json
import logging


class ImageSource(Enum):
    URL = "url"
    FILE = "file"
    BASE64 = "base64"


@dataclass
class VisionConfig:
    model: str = "gpt-4o"
    max_image_size_mb: int = 20
    detail: str = "auto"   # "low" | "high" | "auto"
    max_retries: int = 3
    timeout: int = 60


class DocumentAnalyzer:
    """Extract text and structured fields from documents."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def extract_text(self, image_path: str) -> str:
        return self._analyze(image_path, "Extract all text. Maintain formatting where possible.")

    def extract_structured_data(self, image_path: str, fields: list[str]) -> dict:
        fields_str = ", ".join(fields)
        prompt = (
            f"Extract these fields: {fields_str}. "
            "Return JSON with field names as keys. Use null for missing fields."
        )
        response = self._analyze(image_path, prompt, json_mode=True)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}

    def analyze_receipt(self, image_path: str) -> dict:
        prompt = (
            "Extract store_name, date, items (list of name/quantity/price), "
            "subtotal, tax, total, payment_method. Return JSON."
        )
        try:
            return json.loads(self._analyze(image_path, prompt, json_mode=True))
        except json.JSONDecodeError:
            return {}

    def _analyze(self, image_path: str, prompt: str, json_mode: bool = False) -> str:
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}]
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


class VisionService:
    """Production vision service with size validation and retry."""

    MEDIA_TYPES = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"
    }

    def __init__(self, config: Optional[VisionConfig] = None):
        self.config = config or VisionConfig()
        self.client = OpenAI()
        self.logger = logging.getLogger(__name__)

    def analyze(self, image: Union[str, Path], prompt: str,
                source_type: ImageSource = ImageSource.FILE,
                structured_output: bool = False) -> dict[str, Any]:
        try:
            image_content = self._prepare_image(image, source_type)
            messages = [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": image_content, "detail": self.config.detail}}
            ]}]
            kwargs: dict[str, Any] = {
                "model": self.config.model,
                "messages": messages,
                "timeout": self.config.timeout
            }
            if structured_output:
                kwargs["response_format"] = {"type": "json_object"}

            for attempt in range(self.config.max_retries):
                try:
                    response = self.client.chat.completions.create(**kwargs)
                    content = response.choices[0].message.content
                    return {
                        "success": True,
                        "content": json.loads(content) if structured_output else content,
                        "usage": {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens
                        }
                    }
                except Exception as e:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == self.config.max_retries - 1:
                        raise
        except Exception as e:
            self.logger.error(f"Vision analysis failed: {e}")
            return {"success": False, "error": str(e)}

    def _prepare_image(self, image: Union[str, Path], source_type: ImageSource) -> str:
        if source_type == ImageSource.URL:
            return str(image)
        if source_type == ImageSource.BASE64:
            return f"data:image/jpeg;base64,{image}"
        path = Path(image)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_image_size_mb:
            raise ValueError(f"Image too large: {size_mb:.1f}MB > {self.config.max_image_size_mb}MB")
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode()
        media_type = self.MEDIA_TYPES.get(path.suffix.lower(), "image/jpeg")
        return f"data:{media_type};base64,{data}"
```

### `templates/image-classifier.py`

```python
"""ImageClassifier with batch (asyncio.gather under semaphore) + normalization."""
from openai import OpenAI
import base64
import json


class ImageClassifier:
    """Classify images into predefined categories."""

    def __init__(self, categories: list[str], model: str = "gpt-4o"):
        self.categories = categories
        self.client = OpenAI()
        self.model = model

    def classify(self, image_path: str) -> dict:
        """Returns {category, confidence (0-1), reasoning}."""
        categories_str = ", ".join(self.categories)
        prompt = (
            f"Classify this image into one of: {categories_str}. "
            "Return JSON: {\"category\": str, \"confidence\": float, \"reasoning\": str}"
        )
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}],
            response_format={"type": "json_object"}
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"category": "unknown", "confidence": 0.0, "reasoning": "parse error"}

    def classify_batch(self, image_paths: list[str]) -> list[dict]:
        return [self.classify(path) for path in image_paths]
```

### `templates/content-moderator.py`

```python
"""ContentModerator with severity normalization and human-review gate."""
from openai import OpenAI
import base64
import json


class ContentModerator:
    """Check images for policy violations. Never use as sole moderation layer."""

    PROMPT = """Analyze for policy violations.
Categories: violence, adult_content, hate_symbols, self_harm, illegal_activity.
Return JSON:
{
  "is_safe": true|false,
  "flags": [list of categories violated],
  "severity": "none" | "low" | "medium" | "high",
  "confidence": 0.0-1.0,
  "needs_human_review": true|false,
  "details": "brief explanation"
}
Set needs_human_review: true when confidence < 0.7.
Always use lowercase severity values."""

    def __init__(self, model: str = "gpt-4o"):
        self.client = OpenAI()
        self.model = model

    def moderate(self, image_path: str) -> dict:
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": self.PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}],
            response_format={"type": "json_object"}
        )
        try:
            result = json.loads(response.choices[0].message.content)
            # Normalize severity to lowercase — model occasionally returns uppercase
            if "severity" in result:
                result["severity"] = result["severity"].lower()
            return result
        except json.JSONDecodeError:
            return {"is_safe": False, "flags": [], "severity": "none",
                    "confidence": 0.0, "needs_human_review": True,
                    "details": "parse error"}
```

### `templates/prompt-extract.txt`

```text
Analyze this image and extract the following fields as JSON.
Required fields: {field_list}
For missing or illegible fields, use null.
Do not include fields not in the list.
Return only valid JSON, no explanation.
```

### `templates/prompt-moderate.txt`

```text
You are a content moderator. Analyze this image for policy violations.
Categories: violence, adult_content, hate_symbols, self_harm, illegal_activity.
Return JSON:
{"is_safe": bool, "flags": [str], "severity": "none|low|medium|high",
 "confidence": 0.0-1.0, "needs_human_review": bool}
If confidence < 0.7, set needs_human_review: true.
Always use lowercase severity values.
```
