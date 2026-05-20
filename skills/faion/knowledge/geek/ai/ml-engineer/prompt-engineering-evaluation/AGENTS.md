---
slug: prompt-engineering-evaluation
tier: geek
group: ai
domain: ml-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prompts without a test suite degrade silently.
content_id: "ad6e0b997d805b0f"
tags: [prompt-evaluation, testing, prompt-engineering, llm-evaluation, debugging]
---
# Prompt Engineering — Evaluation and Debugging

## Summary

**One-sentence:** Prompts without a test suite degrade silently.

**One-paragraph:** Prompts without a test suite degrade silently. This methodology covers pre-flight checklists, test case design, quality metrics, evaluation rubrics, A/B comparison techniques, debugging workflows for incorrect or inconsistent outputs, and the full deployment checklist for production prompts. Includes LLM-assisted prompt analysis prompts.

## Applies If (ALL must hold)

- Before deploying any prompt to production — all prompts need a minimum test coverage.
- After modifying an existing prompt — regression testing prevents new failures.
- When outputs are inconsistent across runs — debugging workflow identifies root cause.
- When comparing prompt variants — A/B framework gives a structured decision.
- When quality degrades in production — evaluation metrics quantify the regression.

## Skip If (ANY kills it)

- One-off exploratory prompts — full evaluation overhead is not justified.
- Prompts used only for synthetic data generation where output correctness is manually reviewed.

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
