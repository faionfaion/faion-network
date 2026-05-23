# Vision Document Extraction

## Summary

**One-sentence:** Pulls structured fields from invoices, receipts, forms, contracts, and IDs via VLM with Pydantic-enforced output and a deterministic post-validator (totals add up, dates parseable, IDs checksummed).

**One-paragraph:** Document extraction with VLMs replaces classic OCR+template pipelines for documents whose layouts vary (handwritten receipts, multi-vendor invoices, ID cards). The risk: VLM hallucinates fields. The fix: Pydantic schema enforcement at output, plus a post-validator that re-runs deterministic checks (totals add up, dates parseable, IDs checksum) and triggers a human-review queue on failure. Always include a confidence score per field, not a per-document score.

**Ефективно для:**

- AP automation: invoice intake across 50+ vendors with varying layouts.
- Receipt OCR for expense reports where photos are crooked, blurry, multi-currency.
- Onboarding KYC: ID + proof-of-address from international document types.
- Legacy contract digitisation where templates are not available.

## Applies If (ALL must hold)

- Documents have variable layout (classic OCR + template will not generalise).
- Structured output is required (downstream system needs typed fields).
- Manual review queue exists for low-confidence extractions.

## Skip If (ANY kills it)

- Documents have fixed layout — classic OCR + template is cheaper and faster.
- Volume < 50/day — manual entry might be cheaper than tuning the pipeline.
- Documents are high-stakes legal text that must be quoted verbatim — risk of hallucination too high.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Document image | pdf/jpg/png | Upload bus |
| Schema | Pydantic model | BA + Eng joint authoring |
| Validation rules | Python module | BA output |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `doc_type_classify` | haiku | Route to per-type prompt. |
| `vlm_extract` | sonnet | Vision call with strict schema. |
| `post_validate` | haiku | Deterministic field checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/extraction-schema.yaml` | Per-doc-type Pydantic schema sketches |
| `templates/post-validate.py` | Deterministic post-validator skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vision-document-extraction.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-agentic-pipeline]]
- [[vision-provider-selection]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Was the doc-type classifier confident? Branches route to a rule id from `content/01-core-rules.xml` (doc-type-router, pydantic-required, review-queue-on-fail, ...) so every leaf is traceable to a testable statement.
