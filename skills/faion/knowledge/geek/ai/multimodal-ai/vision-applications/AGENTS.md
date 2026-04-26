# Vision Applications

## Summary

Production patterns for vision LLM tasks: OCR, document extraction, image classification, and content moderation using GPT-4o, Claude, or Gemini Vision. Each task sends an image plus a structured prompt and receives JSON-formatted output.

## Why

Vision LLMs outperform traditional OCR on complex layouts, handwriting, and mixed languages, and they unify classification, extraction, and moderation into a single API call. The key constraint is token cost: `detail: "high"` on a 4K image consumes 1500+ prompt tokens, so images must be validated and resized before encoding.

## When To Use

- Document digitization: invoices, receipts, forms, passports, business cards
- Content moderation: classify user-uploaded images before storage or display
- E-commerce: auto-tag product images, generate descriptions, classify categories
- Accessibility: generate alt-text for images at upload time
- Visual QA: answer questions about screenshots, diagrams, charts

## When NOT To Use

- High-volume bulk processing (>10k images/day) — per-image token cost accumulates; CLIP/YOLO/Tesseract are 100-1000x cheaper for classification/detection
- Pixel-level precision tasks (medical imaging, satellite analysis) — vision LLMs reason semantically, not at pixel level
- Real-time video analysis — frame-by-frame API calls add 1-3s latency per frame
- Standardized forms with fixed layout — dedicated OCR tools are faster and cheaper

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | DocumentAnalyzer, ImageClassifier, ContentModerator classes; production VisionService with retry and size validation |
| `content/02-rules.xml` | Token budget rules, image prep before encoding, JSON mode gotchas, batch async pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/document-analyzer.py` | DocumentAnalyzer and VisionService with config dataclass |
| `templates/image-classifier.py` | ImageClassifier with batch support |
| `templates/content-moderator.py` | ContentModerator returning structured severity flags |
| `templates/prompt-extract.txt` | Structured field extraction prompt |
| `templates/prompt-moderate.txt` | Content moderation prompt with confidence threshold |
