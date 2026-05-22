---
slug: fine-tuning-openai-data-prep
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a validated OpenAI fine-tuning JSONL training file plus a data-preparation spec covering schema, token counts, train/validation split, and reusable Python validators.
content_id: "b19f87f63e37e227"
complexity: medium
produces: spec
est_tokens: 4200
tags: [fine-tuning, openai, data-preparation, jsonl, validation]
---
# OpenAI Fine-Tuning Data Preparation

## Summary

**One-sentence:** Produces a validated OpenAI fine-tuning JSONL training file plus a data-preparation spec covering schema, token counts, train/validation split, and reusable Python validators.

**One-paragraph:** Produces a validated OpenAI fine-tuning JSONL training file plus a data-preparation spec. Covers JSONL schema requirements, validation procedures, token counting, train/validation splitting (80/20 default), CSV-to-JSONL conversion, and reusable Python builders + validators. High-quality training data is the primary determinant of fine-tuning success — garbage in, garbage out applies harder to fine-tuning than to prompting.

**Ефективно для:** Data engineer перед OpenAI fine-tune run — фіксує jsonl-формат + token budget до upload.

## Applies If (ALL must hold)

- Decision record selected 'api-sft' or 'api-dpo' (OpenAI fine-tuning endpoint).
- Source data lives in CSV / DB / proprietary format and needs conversion to JSONL.
- Training corpus ≥100 examples (≥10 minimum to call the API but underflow risks).
- Need to split train / validation for the OpenAI fine-tune job.
- Token-counting budget required before upload (cost = tokens * unit price).

## Skip If (ANY kills it)

- Fine-tuning decision landed on LoRA / QLoRA / Full FT — use the corresponding HF JSONL schema.
- Source data already in OpenAI-valid JSONL and tokens counted.
- Data volume <10 examples — OpenAI rejects the upload outright.
- Provider is not OpenAI — schemas differ.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Source data | csv / parquet / db dump | data-team |
| Target task definition | markdown | product / ML lead |
| Budget envelope | yaml ($/job) | finance |
| OpenAI API key | env var | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/finetuning` | Parent decision; this methodology elaborates its 'api-sft' branch. |
| `geek/ai/ml-engineer/fine-tuning-openai-sft` | Downstream training methodology consuming this output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: extract → schema-map → validate → split → upload. | ~700 |
| `content/05-examples.xml` | medium | Worked example: customer-support tickets CSV → JSONL train/val pair. | ~600 |
| `content/06-decision-tree.xml` | essential | Branch by source format + chat vs completion + DPO presence. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-map` | haiku | Mechanical CSV-column → JSONL-message mapping. |
| `token-budget` | sonnet | Estimate cost; flag if any example exceeds model context. |
| `data-quality-audit` | opus | Cross-example coherence; surface labelling drift. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openai-jsonl-builder.py` | CSV→JSONL builder with schema validation. |
| `templates/openai-validate-jsonl.py` | Pre-upload validator (schema + token counts). |
| `templates/data-prep-spec.md` | Markdown spec listing source/transform/output. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fine-tuning-openai-data-prep.py` | Validate that the data-prep spec matches the schema (counts, splits, token budget). | Pre-upload of every OpenAI fine-tune dataset. |

## Related

- [[fine-tuning-openai-sft]] — downstream training step.
- [[fine-tuning-openai-eval]] — eval set comes from the same split logic.
- [[finetuning]] — parent decision.

## Decision tree

Decision tree at `content/06-decision-tree.xml` chooses format (chat / completion / DPO pairs) and split strategy. Use BEFORE writing the builder script.
