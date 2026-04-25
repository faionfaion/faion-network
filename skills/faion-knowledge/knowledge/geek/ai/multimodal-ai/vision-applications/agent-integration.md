# Agent Integration — Vision Applications (Image Analysis)

## When to use
- Document digitization: extract structured data from invoices, receipts, forms, passports, business cards
- Content moderation pipeline: classify user-uploaded images before storage/display
- E-commerce: auto-tag product images, generate descriptions, classify categories
- Accessibility: generate alt-text for images at upload time
- Visual QA: answer questions about screenshots, diagrams, charts in a support or analytics workflow
- OCR replacement: vision LLMs outperform traditional OCR on complex layouts, handwriting, mixed languages

## When NOT to use
- High-volume bulk processing (>10k images/day) — per-image token cost accumulates; traditional CV models (CLIP, YOLO, Tesseract) are 100-1000x cheaper for classification/detection
- Tasks requiring pixel-level precision (medical imaging, satellite analysis) — vision LLMs reason at semantic level, not pixel level
- Real-time video analysis — frame-by-frame API calls introduce 1-3s latency per frame
- Tasks solvable by structured OCR (standardized forms with fixed layout) — dedicated OCR tools are faster and cheaper

## Where it fails / limitations
- Images larger than 20MB are rejected by OpenAI API — always check file size before encoding
- `detail: "high"` costs 85 tokens per 512x512 tile + base 85 tokens; a 4K image can consume 1500+ tokens just for the image
- `json_mode=True` requires the model to produce valid JSON — it hallucinates invalid JSON on complex nested structures; always wrap in `try/except json.JSONDecodeError`
- Base64 encoding increases payload size by ~33% — for batch processing, pre-encode and cache encoded strings
- Vision models cannot read text smaller than ~8pt in low-detail mode; switch to `detail: "high"` for dense documents
- Content moderation via LLM is probabilistic — false negative rate on subtly harmful content is non-zero; never use as sole moderation layer

## Agentic workflow
Vision analysis fits naturally into agent pipelines as a perception step: agent receives an image path or URL, calls the `VisionService`, and branches based on structured output (classification, extracted fields, moderation flags). For document extraction, the agent uses JSON mode and routes the parsed result to downstream logic. Claude subagents can drive the full pipeline — image intake → validation → analysis → result routing — with human review only on low-confidence or flagged outputs.

### Recommended subagents
- `faion-sdd-execution` — scaffold a vision pipeline for a specific use case (receipt parsing, moderation, alt-text generation)
- Custom moderation agent — analyze image + return severity flag; escalate `high` severity to human queue

### Prompt pattern
```
Analyze this image and extract the following fields as JSON.
Required fields: {field_list}
For missing or illegible fields, use null.
Do not include fields not in the list.
Return only valid JSON, no explanation.
```

```
You are a content moderator. Analyze this image for policy violations.
Categories: violence, adult_content, hate_symbols, self_harm, illegal_activity.
Return JSON: {"is_safe": bool, "flags": [str], "severity": "none|low|medium|high", "confidence": 0-1}
If confidence < 0.7, set "needs_human_review": true.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` | Vision via GPT-4o; base64 or URL image input | `pip install openai` · platform.openai.com/docs/guides/vision |
| `anthropic` | Vision via Claude claude-opus-4-5 (200K context, multi-image) | `pip install anthropic` · docs.anthropic.com/en/docs/vision |
| `Pillow` | Image resize, format conversion, size validation pre-API | `pip install pillow` · python-pillow.org |
| `httpx` | Async HTTP for downloading remote images before analysis | `pip install httpx` |
| `google-generativeai` | Gemini Vision (1M context, native PDF support) | `pip install google-generativeai` · ai.google.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI GPT-4o | SaaS | Yes — REST/SDK | Best general vision; JSON mode; up to 20MB images |
| Anthropic Claude | SaaS | Yes — REST/SDK | Multi-image comparison; 200K context; strong at documents |
| Google Gemini Pro Vision | SaaS | Yes — REST/SDK | Native PDF; 1M context; competitive on charts/diagrams |
| AWS Textract | SaaS | Yes — Boto3 | Specialized OCR for forms/tables; cheaper than LLM for standard docs |
| Google Cloud Vision | SaaS | Yes — Python client | Fast label detection, face detection, landmark; not generative |
| Azure Computer Vision | SaaS | Yes — SDK | OCR, object detection, content moderation; pairs with Azure OpenAI |
| Roboflow | SaaS | Yes — API | Custom CV model training and serving; YOLO-based detection |

## Templates & scripts
See `templates.md` for `DocumentAnalyzer`, `ImageClassifier`, `ContentModerator`, and `VisionService` classes.

Inline: resize image to stay within API token budget:
```python
from PIL import Image
import io, base64

def prepare_image_for_api(path: str, max_short_side: int = 768) -> str:
    """Resize image and encode as base64. Keeps detail:auto within budget."""
    img = Image.open(path)
    w, h = img.size
    short = min(w, h)
    if short > max_short_side:
        scale = max_short_side / short
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = "JPEG" if path.lower().endswith((".jpg", ".jpeg")) else "PNG"
    img.save(buf, format=fmt, quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode()
```

## Best practices
- Always validate image size and format before encoding — reject files > 20MB and unsupported formats early
- Use `detail: "auto"` for most cases; switch to `detail: "high"` only for dense text documents or charts
- For structured extraction, define the exact JSON schema in the prompt and use `response_format: json_object` — parse with `try/except` always
- For content moderation: set confidence threshold and route low-confidence results to human review, not to auto-action
- Cache base64-encoded images by content hash to avoid re-encoding on retry
- For batch processing, use `asyncio.gather()` with concurrency limit (10-20 simultaneous requests) to avoid rate limits
- Include a few-shot example in the prompt for classification tasks — vision models benefit significantly from concrete examples

## AI-agent gotchas
- JSON mode does not guarantee schema adherence — a `ContentModerator` returning `{"severity": "HIGH"}` instead of `"high"` breaks downstream logic silently; normalize output
- Remote image URLs embedded in prompts are fetched by the API server; ensure URLs are publicly accessible and not behind auth
- An agent passing raw file paths assumes the runtime has read access — always validate path existence before `open()`
- The `VisionService.batch_analyze()` in the README is sequential (one-by-one); for true parallelism, wrap with `asyncio` or `concurrent.futures`
- Vision models occasionally "hallucinate" text in images (especially small or blurry text) — for high-stakes OCR, cross-validate with a second API call using a different prompt

## References
- https://platform.openai.com/docs/guides/vision
- https://docs.anthropic.com/en/docs/build-with-claude/vision
- https://ai.google.dev/tutorials/python_quickstart#vision
- https://docs.aws.amazon.com/textract/latest/dg/what-is.html
- https://platform.openai.com/docs/guides/vision/calculating-costs
