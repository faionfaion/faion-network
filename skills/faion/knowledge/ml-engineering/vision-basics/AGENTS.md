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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-basics.py` | Validate extraction JSON against the declared Pydantic schema. | Post-VLM call, before downstream consumes. |

## Related

- [[vision-applications]] — production patterns (OCR, classification, moderation) on top of these basics.
- [[structured-output-basics]] — Pydantic + json_object contract used everywhere.
- [[img-gen-basics]] — generator side; vision-basics verifies generated frames.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the provider (Claude for complex layouts and 200K context, GPT-4o for json_object enforcement, Gemini Flash for high-volume batch), the input mode (URL vs base64 based on sensitivity), and the detail level (`low` for classification, `high` for dense text). Use it at the extract() entry point before any provider call.
