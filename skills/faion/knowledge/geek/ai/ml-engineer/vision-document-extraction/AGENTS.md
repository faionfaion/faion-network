---
slug: vision-document-extraction
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Document extraction uses VLMs to pull structured data from invoices, receipts, forms, contracts, and ID documents.
content_id: "cee5b320d420d343"
tags: [vision, ocr, document-extraction, structured-output, invoice]
---
# Vision Document Extraction

## Summary

**One-sentence:** Document extraction uses VLMs to pull structured data from invoices, receipts, forms, contracts, and ID documents.

**One-paragraph:** Document extraction uses VLMs to pull structured data from invoices, receipts, forms, contracts, and ID documents. The core pattern is: schema-defined prompt → response_format enforcement → Pydantic validation → confidence routing to human review. Claude Sonnet is the default choice for complex layouts; Gemini Flash for high-volume simple documents.

## Applies If (ALL must hold)

- Extracting structured data from uploaded documents: invoices, receipts, contracts, forms.
- OCR replacement for scanned PDFs where layout matters (tables, multi-column text).
- Processing ID documents (passports, driver's licences) to extract personal information.
- Automating data entry from paper-based or image-based forms into backend systems.
- Batch processing of historical document archives that were not machine-readable.

## Skip If (ANY kills it)

- Simple barcode/QR decoding — zxing or python-qrcode are faster and cheaper.
- Documents where pixel-level measurement accuracy is required — statistical VLM outputs are not reliable for calibration tasks.
- Medical records where FDA/CE-cleared inference is required — off-the-shelf VLMs are not cleared devices.
- Privacy-regulated documents where sending to third-party APIs violates GDPR/HIPAA data agreements — use self-hosted Qwen3-VL instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-engineer/`
