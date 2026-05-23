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

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-applications.py` | Validate task-specific JSON against 02-output-contract task schemas. | Post-VLM call, before downstream auto-action. |

## Related

- [[vision-basics]] — single-image typed extraction layer this builds on.
- [[content-moderation]] — moderation patterns extended with policy enforcement.
- [[structured-output-basics]] — JSON-schema contract.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` routes by task type (document → DocumentAnalyzer; classify → ImageClassifier; moderate → ContentModerator), provider by stakes (high-stakes → Claude or GPT-4o; high-volume → Gemini Flash), and decides when to escalate to human review based on confidence threshold (default 0.7) and severity. Use it at the route() entry point in VisionService.
