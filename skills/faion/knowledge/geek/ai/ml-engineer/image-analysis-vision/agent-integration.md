# Agent Integration — Image Analysis & Vision

## When to use
- Extracting structured data from uploaded documents: invoices, receipts, contracts, forms
- Content moderation pipeline where images are submitted by end users
- Accessibility tooling: auto-generating alt text and image descriptions at scale
- OCR replacement for scanned PDFs where layout matters (tables, multi-column text)
- Visual Q&A over a corpus of images (product catalogs, medical scans, satellite imagery)
- Automated analysis of charts/graphs in research reports or BI dashboards
- Agent-driven document processing workflows where images arrive as tool results

## When NOT to use
- Simple barcode/QR decoding — specialized libraries (zxing, python-qrcode) are faster and cheaper
- Object detection with bounding boxes at scale — fine-tuned YOLO/DETR models beat VLMs on throughput and cost
- Real-time video frame analysis at >5 FPS — VLM API latency (500ms-2s) makes this impractical; use local CV models
- Medical imaging requiring FDA/CE-certified inference — off-the-shelf VLM APIs are not cleared devices
- Privacy-sensitive images where sending to third-party APIs violates data agreements — use self-hosted Qwen3-VL or GLM-4.5V
- Tasks where deterministic pixel-level output is needed (measurement, calibration) — statistical VLM outputs are not reliable here

## Where it fails / limitations
- Claude 4 / GPT-4o hallucinate specific numbers in charts — always validate extracted numerical data against a second pass or a deterministic chart parser
- Text rendering accuracy degrades below ~100px font size and on handwritten text; 2.1% CER for printed is production-grade, but cursive handwriting remains unreliable
- Complex multi-column PDF layouts with footnotes and margin notes often produce merged or reordered text chunks
- Gemini 3 Pro's 3,600-image-per-request limit sounds high but each image consumes ~250-750 tokens — real batch size is context-limited
- Model content policies reject borderline medical/forensic images unpredictably — implement retry with prompt reformulation
- Structured JSON output from vision is not guaranteed unless you enforce it with response_format or output_parsers; free-form descriptions drift from schema

## Agentic workflow
Use a vision-extraction subagent that takes an image (URL or base64), calls the appropriate VLM based on task type (layout-heavy → Claude Sonnet; high-volume OCR → Gemini Flash; artistic/ambiguous → GPT-4o), and returns a structured Pydantic object. A routing subagent upstream classifies the image type (document, photo, chart, medical) and selects the VLM + extraction prompt. For document processing pipelines, chain: OCR agent → validation agent → structured-storage agent, with a human-review queue for low-confidence extractions (confidence < 0.85).

### Recommended subagents
- `image-router` — classifies image type and selects VLM + prompt variant
- `vision-extractor` — calls VLM API, enforces structured output schema, returns Pydantic model
- `validation-agent` — cross-checks extracted fields against business rules (date formats, numeric ranges, required fields)
- `alt-text-generator` — generates accessible alt text descriptions; separate from data extraction to keep prompts focused

### Prompt pattern
```
Extract all data from this document image and return as JSON matching this schema:
{schema}

Rules:
- If a field is not visible or legible, set it to null
- Do not infer or guess values not present in the image
- For amounts, include currency symbol if visible
- Confidence: set "low" if any field required significant interpretation
```

```python
# Model selection by task
def select_vision_model(task_type: str) -> str:
    routing = {
        "ocr_high_volume": "gemini-2.0-flash",
        "complex_layout": "claude-sonnet-4-5",
        "medical_imaging": "gemini-2.5-pro",
        "general_qa": "gpt-4o",
        "privacy_sensitive": "qwen-vl-local",  # self-hosted
    }
    return routing.get(task_type, "claude-sonnet-4-5")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` | Claude Vision API | `pip install anthropic` / https://docs.anthropic.com/en/docs/vision |
| `openai` | GPT-4o Vision API | `pip install openai` / https://platform.openai.com/docs/guides/vision |
| `google-generativeai` | Gemini Vision API | `pip install google-generativeai` / https://ai.google.dev/gemini-api/docs/image-understanding |
| `pytesseract` | Local OCR fallback (Tesseract) | `pip install pytesseract` / https://github.com/tesseract-ocr/tesseract |
| `pdf2image` | PDF to image conversion for document pipelines | `pip install pdf2image` |
| `Pillow` | Image preprocessing (resize, compress before API) | `pip install Pillow` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Best for complex document layouts; supports base64 and URL |
| OpenAI API | SaaS | Yes | Best text rendering accuracy; structured JSON output via response_format |
| Google AI Studio / Vertex AI | SaaS | Yes | Gemini Flash for high-volume; Gemini Pro for medical/scientific |
| Replicate | SaaS | Yes | Host Qwen3-VL and other open-source VLMs with simple API; pay-per-call |
| AWS Bedrock | SaaS | Yes | Stable Diffusion 3.5 + Claude on-prem-ish; enterprise compliance |
| Azure AI Vision | SaaS | Partial | Good for OCR on Azure stack; less capable than frontier VLMs on layout |
| Roboflow | SaaS | Yes | Manages fine-tuned vision model datasets and inference endpoints |

## Templates & scripts
See `templates.md` for full document extraction templates.

Minimal vision extraction with confidence routing:
```python
import anthropic, base64
from pydantic import BaseModel

class InvoiceData(BaseModel):
    vendor: str | None
    total_amount: float | None
    date: str | None
    line_items: list[dict]
    confidence: str  # "high" | "low"

def extract_invoice(image_path: str) -> InvoiceData:
    client = anthropic.Anthropic()
    with open(image_path, "rb") as f:
        img_b64 = base64.standard_b64encode(f.read()).decode()

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
                {"type": "text", "text": "Extract invoice data as JSON: {vendor, total_amount, date, line_items, confidence}. confidence=low if any ambiguity."},
            ],
        }],
    )
    import json
    data = json.loads(response.content[0].text)
    return InvoiceData(**data)
```

## Best practices
- Compress images to 1024px on the long edge before sending to API — reduces token cost by 50-70% with minimal quality loss for OCR tasks
- Always send images as base64 for sensitive documents; URL-based images are fetched by the provider's servers and may be logged
- Use `detail: "high"` in GPT-4o for complex layouts; `detail: "low"` for thumbnails and previews — mismatching costs 4x tokens
- For batch document processing, process in parallel with async clients; single-threaded VLM calls at 1-2s each do not scale
- Implement a second-pass validation: extract data, then in a separate call ask the VLM to verify specific fields against the image
- Cache extraction results keyed on image hash — the same invoice scanned twice should not hit the API twice

## AI-agent gotchas
- VLMs cannot see file metadata (EXIF, PDF author, creation date) — agents expecting metadata from vision calls will get nothing; use PyMuPDF or Pillow for metadata extraction separately
- Pydantic schema enforcement via prompt is unreliable without `response_format`/tool-use — always parse with try/except and fallback to a re-prompt with explicit error
- Human-in-the-loop checkpoint: for financial document extraction (invoices, contracts), require human review when confidence is "low" or extracted total exceeds a business threshold before writing to ERP
- Image size limits: Anthropic API max 5MB per image, OpenAI 20MB — agents handling user uploads need pre-flight size checks to avoid silent API errors

## References
- Anthropic Claude Vision: https://docs.anthropic.com/en/docs/vision
- OpenAI Vision guide: https://platform.openai.com/docs/guides/vision
- Gemini image understanding: https://ai.google.dev/gemini-api/docs/image-understanding
- VLM benchmark (2026): https://www.datacamp.com/blog/top-vision-language-models
- Qwen3-VL (self-hosted): https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct
