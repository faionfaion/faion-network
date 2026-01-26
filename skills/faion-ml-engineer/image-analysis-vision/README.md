# Image Analysis & Vision

Vision-based AI for image analysis, OCR, document understanding, and visual question answering.

## Overview

Modern Vision Language Models (VLMs) enable powerful image understanding capabilities:

- **OCR & Text Extraction** - Read text from images, documents, screenshots
- **Document Understanding** - Analyze invoices, receipts, forms, contracts
- **Visual Question Answering** - Answer questions about image content
- **Image Classification** - Categorize images into predefined classes
- **Content Moderation** - Detect inappropriate or unsafe content
- **Accessibility** - Generate alt text and image descriptions

## Provider Comparison (2025-2026)

| Provider | Model | Context | Best For | Pricing |
|----------|-------|---------|----------|---------|
| OpenAI | GPT-4.1 | 1M | General vision, charts, OCR | $2.50/1M in |
| OpenAI | GPT-4o | 128K | Balanced cost/quality | $2.50/1M in |
| Anthropic | Claude 4 Opus | 200K | Long docs, reasoning | Premium |
| Anthropic | Claude 4 Sonnet | 200K (1M beta) | Production workloads | Mid-tier |
| Google | Gemini 3 Pro | 1M | Medical imaging, video | Competitive |
| Google | Gemini 2.5 Flash | 1M | High-volume OCR | $0.16/1M in |
| Open-source | Qwen3-VL-235B | 128K | Self-hosted, privacy | Compute only |
| Open-source | GLM-4.5V | 128K | Document screening | Compute only |

## Key Capabilities by Model

### OpenAI GPT-4.1 / GPT-4o

- Native multimodal (text + images)
- Up to 4 images per API request
- Structured JSON output mode
- Object counting, visual QA, OCR
- Chart and diagram analysis

### Anthropic Claude 4

- 200K context (1M beta on Sonnet 4)
- Hybrid OCR for scanned documents
- Layout-aware document understanding
- 2.1% Character Error Rate on printed text
- Best-in-class for complex document layouts

### Google Gemini 3 Pro

- Native sparse MoE architecture
- Up to 3,600 images per request
- Object detection and segmentation
- Medical/biomedical imagery SOTA
- High frame rate video understanding (10 FPS)

## Files in This Module

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and provider comparison |
| [checklist.md](checklist.md) | Implementation checklists |
| [examples.md](examples.md) | Code examples for common tasks |
| [templates.md](templates.md) | Reusable code templates |
| [llm-prompts.md](llm-prompts.md) | Optimized prompts for vision tasks |

## Quick Start

```python
# OpenAI Vision
from openai import OpenAI
import base64

client = OpenAI()

with open("document.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract all text from this document"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
        ]
    }]
)
```

## Decision Framework

```
Task Type               → Recommended Approach
──────────────────────────────────────────────
Simple OCR              → Gemini Flash 2.0 (cost-effective)
Complex layouts         → Claude 4 Sonnet (layout-aware)
Medical/scientific      → Gemini 3 Pro (specialized training)
High-volume batch       → Fine-tuned smaller model
Privacy-sensitive       → Qwen3-VL / local deployment
Real-time processing    → GPT-4o Mini / Gemini Flash
```

## References

- [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision)
- [Claude Vision Docs](https://docs.anthropic.com/en/docs/vision)
- [Gemini Image Understanding](https://ai.google.dev/gemini-api/docs/image-understanding)
- [Top Vision Language Models 2026](https://www.datacamp.com/blog/top-vision-language-models)
