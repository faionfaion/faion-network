# Vision Basics

## Summary

Analyze images with VLM APIs (GPT-4o, Claude Sonnet, Gemini Flash): single-image analysis,
multi-image comparison, structured JSON extraction via Pydantic, and stateful visual Q&A.
Covers input methods (URL vs. base64), detail settings, token cost control, and the failure modes
that make VLMs unsuitable for precision tasks.

## Why

VLM API calls fail silently when images exceed provider size caps, base64-encode unexpectedly large
requests, or produce unvalidated JSON that breaks downstream agents. Resize images to 1024px before
sending (50-70% token reduction), enforce structured output via `response_format`, and cache by
SHA-256 of image bytes to avoid re-scanning identical images.

## When To Use

- Agents need to read content from screenshots, diagrams, or scanned forms.
- Pipeline receives images as intermediate outputs (web scraping returns screenshot; agent reads the page).
- Generating alt-text or captions for images at scale.
- Classifying images (safe/unsafe, relevant/irrelevant) as a routing step.
- Extracting text from images when dedicated OCR is unavailable or layout is complex.

## When NOT To Use

- Real-time video analysis at >2 FPS — VLM API latency (500ms-2s) is too high; use YOLOv11 or GroundingDINO locally.
- High-volume barcode/QR decoding — use zxing or python-qrcode; 100x cheaper and deterministic.
- Pixel-level measurement — VLM outputs are statistical estimates, not precise values.
- Privacy-sensitive images that must not leave the local environment — use Qwen2.5-VL or LLaVA via Ollama.
- Tasks reducible to image metadata (EXIF, creation date) — VLMs cannot see metadata; use Pillow or ExifTool.
- Medical, legal, or forensic images where model content policies may silently reject inputs.

## Content

| File | What's inside |
|------|---------------|
| `content/01-input-methods.xml` | URL vs. base64, media type detection, resize helper, provider size limits. |
| `content/02-structured-extraction.xml` | Pydantic schema, `response_format`, multi-image labeling, JSON parse-with-retry. |
| `content/03-rules.xml` | Core rules: resize, caching, detail setting, stateful Q&A image-in-first-turn-only, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vision_extract.py` | `analyze_image_url`, `analyze_local_image`, `structured_analysis`, `VisualQA` with Pydantic. |
| `templates/prepare_image.py` | Resize + base64 encode helper (1024px cap, returns media_type). |
| `templates/prompt-vision.txt` | Agent prompt for structured vision extraction with null-on-ambiguity rule. |
