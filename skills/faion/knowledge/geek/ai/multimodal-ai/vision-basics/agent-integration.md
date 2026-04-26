# Agent Integration — Image Analysis: Core Concepts

## When to use
- Agents need to read content from uploaded images: screenshots, diagrams, scanned forms
- Pipeline receives images as intermediate outputs (e.g., web-scraping tool returns a screenshot, agent must read the page)
- Generating alt-text or captions for images at scale in a content pipeline
- Classifying images (e.g., is this image safe/unsafe, relevant/irrelevant) as a routing step before further processing
- Extracting text from images where a dedicated OCR tool is not available or the layout is complex
- Answering questions about product images or screenshots in a customer-facing chatbot flow

## When NOT to use
- Real-time video analysis at >2 FPS — VLM API latency (500ms–2s per image) makes it unsuitable; use local CV models (YOLOv11, GroundingDINO)
- High-volume barcode/QR decoding — use zxing or python-qrcode; they are 100x cheaper and deterministic
- Pixel-level measurement or calibration tasks — VLM outputs are statistical, not precise
- Medical, legal, or forensic images where model content policies may reject inputs without warning
- Privacy-sensitive images that must not leave the local environment — use self-hosted Qwen2.5-VL or LLaVA via Ollama
- Tasks reducible to image metadata (EXIF, file size, creation date) — VLMs cannot see metadata; use Pillow or ExifTool

## Where it fails / limitations
- Numbers extracted from charts are frequently hallucinated — always cross-validate with a second pass or a deterministic chart parser
- Handwritten text accuracy is low; printed text below ~100px height also degrades significantly
- Base64 encoding of large images bloats request size and context; a 5MB JPEG becomes ~7MB of base64 text
- API image size caps: Anthropic 5MB, OpenAI 20MB — silent failures if agent does not pre-check
- VLM JSON output is not guaranteed without response_format enforcement; prompt-only schema requests drift
- Multi-image comparisons (>5 images) become expensive fast — each image consumes 500–1500 tokens depending on detail setting

## Agentic workflow
A vision agent receives an image (URL or base64) and a task description, calls the appropriate VLM (Claude Sonnet for complex layouts, Gemini Flash for high volume, GPT-4o for general QA), and returns a structured Pydantic object. Upstream, a routing subagent classifies the image type (document, photo, screenshot, chart) and selects the VLM and prompt variant. For multi-image workflows, a fan-out pattern works well: spawn parallel vision subagents per image, then merge results in a reduction step.

### Recommended subagents
- `vision-router` — classifies image type (document/photo/chart/screenshot) and selects VLM + detail setting
- `vision-extractor` — calls VLM API, enforces structured output schema (Pydantic + response_format), returns typed result
- `vision-qa` — stateful Q&A over a single image across multiple questions (maintains conversation history with image in first turn only)
- `vision-validator` — second-pass VLM call to verify specific extracted fields against the source image

### Prompt pattern
```
Analyze this image and return JSON matching the schema below.
- If a field is not visible or ambiguous, set it to null.
- Do not infer values not present in the image.
- Set confidence to "low" if any field required significant interpretation.

Schema: {schema_json}
```

```python
# Minimal Claude vision extraction
import anthropic, base64, json
from pydantic import BaseModel

class ImageResult(BaseModel):
    description: str
    text_content: str | None
    confidence: str  # "high" | "low"

def extract_image(image_path: str, task: str) -> ImageResult:
    client = anthropic.Anthropic()
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode()
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}},
            {"type": "text", "text": f"{task}\nReturn JSON: {{description, text_content, confidence}}"},
        ]}],
    )
    return ImageResult(**json.loads(resp.content[0].text))
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude Vision API (Sonnet, Haiku) | `pip install anthropic` / https://docs.anthropic.com/en/docs/vision |
| `openai` | GPT-4o Vision API | `pip install openai` / https://platform.openai.com/docs/guides/vision |
| `google-generativeai` | Gemini Vision API | `pip install google-generativeai` / https://ai.google.dev/gemini-api/docs/image-understanding |
| `Pillow` | Image preprocessing: resize, compress, convert before API call | `pip install Pillow` |
| `pdf2image` | Convert PDF pages to images for vision pipeline ingestion | `pip install pdf2image` |
| `pytesseract` | Local OCR fallback for printed text (Tesseract) | `pip install pytesseract` / https://github.com/tesseract-ocr/tesseract |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Best for complex layouts and long-context documents |
| OpenAI API | SaaS | Yes | Best structured JSON extraction via response_format; 20MB image limit |
| Google AI Studio / Vertex AI | SaaS | Yes | Gemini Flash for high-volume batch; Gemini Pro for multimodal reasoning |
| Replicate | SaaS | Yes | Host Qwen2.5-VL, LLaVA, and other open-source VLMs with REST API |
| Ollama | OSS | Yes | Run LLaVA, Qwen2.5-VL locally; no data leaves machine; use via REST |
| AWS Bedrock | SaaS | Yes | Claude + Titan on-prem-ish; enterprise compliance |
| Roboflow | SaaS | Partial | Fine-tuned detection models, not general VLM; good for classification tasks |

## Templates & scripts
See `templates.md` for full multi-image and structured extraction templates.

Resize + encode helper (prevents oversized API requests):
```python
from PIL import Image
import base64, io

def prepare_image(path: str, max_px: int = 1024) -> tuple[str, str]:
    """Resize image to max_px on long edge, return (base64, media_type)."""
    img = Image.open(path)
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = img.format or "PNG"
    img.save(buf, format=fmt)
    data = base64.standard_b64encode(buf.getvalue()).decode()
    mt = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp", "GIF": "image/gif"}.get(fmt, "image/png")
    return data, mt
```

## Best practices
- Resize images to 1024px long edge before sending to reduce token cost by 50–70% with minimal quality loss for text/diagram tasks
- Send images as base64 for sensitive content; URL-based images are fetched by the provider's servers and may be logged
- Use GPT-4o `detail: "low"` for quick classification; `detail: "high"` for layout-heavy documents — mismatching costs 4x tokens
- For stateful visual Q&A, include the image only in the first message of the conversation; subsequent turns are text-only
- Cache extraction results keyed on a SHA-256 of the image bytes — re-scanning the same image should not re-call the API
- For batch classification, use structured output (Pydantic + response_format) so downstream agents always receive typed results

## AI-agent gotchas
- VLMs cannot read file metadata (EXIF, PDF author, creation date) — if your agent needs metadata, extract it with Pillow or PyMuPDF in a separate step before or after the VLM call
- JSON schema compliance via prompt alone is unreliable — always parse with try/except and re-prompt with the specific parse error if validation fails
- Human-in-the-loop checkpoint: for financial or legal document extraction, require human review when confidence is "low" or when extracted amounts exceed a business threshold before writing to any system of record
- Image size limits are per-image, not per-request — a request with 10 images at 4.9MB each can still fail if the provider enforces a total payload cap
- When comparing multiple images (e.g., before/after, product variants), label each image explicitly in the prompt ("Image 1:", "Image 2:") — VLMs lose track of which image they are describing without explicit labels

## References
- https://docs.anthropic.com/en/docs/vision
- https://platform.openai.com/docs/guides/vision
- https://ai.google.dev/gemini-api/docs/image-understanding
- https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct (self-hosted option)
- https://github.com/tesseract-ocr/tesseract (local OCR fallback)
