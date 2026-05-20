---
slug: fine-tuning-openai-data-prep
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: High-quality training data is the primary determinant of fine-tuning success.
content_id: "d891e3bc7b484913"
tags: [fine-tuning, openai, data-preparation, jsonl, validation]
---
# OpenAI Fine-Tuning Data Preparation

## Summary

**One-sentence:** High-quality training data is the primary determinant of fine-tuning success.

**One-paragraph:** High-quality training data is the primary determinant of fine-tuning success. This methodology covers JSONL format requirements, validation procedures, token counting, train/validation splitting, CSV conversion, and reusable Python builders and validators for OpenAI fine-tuning datasets.

## Applies If (ALL must hold)

- Before every fine-tuning job upload — validate JSONL format and count tokens.
- When building training data from CSV, database exports, or human annotations.
- When assessing dataset quality: coverage, balance, duplicates, PII exposure.
- When generating training examples programmatically from existing documents.

## Skip If (ANY kills it)

- Data is already validated and in correct JSONL format — skip re-validation to save time.
- Using the OpenAI Playground dataset builder — it validates format automatically.

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
