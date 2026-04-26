# ML/AI Decision Framework

## Summary

A structured decision process for selecting the right AI approach (prompt engineering, RAG, fine-tuning) and the right model tier for a given task. Applies a progressive enhancement strategy: start with prompting → add RAG when external data is needed → add fine-tuning only when behavioral specialization is required at scale. Implements complexity-based model routing to reduce cost by 40-60%.

## Why

Defaulting to GPT or Opus for all tasks leads to 2-3x overspending on simple tasks. Fine-tuning ROI is often overestimated: 6x inference cost + training + maintenance rarely breaks even below 1M requests/month. Model pricing shifts dramatically — the framework must be re-evaluated quarterly. A lightweight complexity classifier routing simple tasks to DeepSeek and complex tasks to Opus captures most of the savings with minimal complexity.

## When To Use

- Starting a new AI feature and choosing between prompting, RAG, or fine-tuning
- Monthly API spend has grown and you suspect model over-selection
- A model is deprecated or a cheaper/faster alternative has appeared
- Different pipeline stages require different capability/cost trade-offs
- Evaluating whether to switch providers for a specific workload

## When NOT To Use

- The task is trivial and the model is already decided — don't over-engineer
- A deadline is imminent — pick the safe default (Claude Sonnet or GPT-4o) and optimize later
- Purely creative tasks (marketing copy, story generation) — model quality differences are subjective; user preference testing matters more than a framework

## Content

| File | What's inside |
|------|---------------|
| `content/01-approach-selection.xml` | Approach decision: prompt engineering vs RAG vs fine-tuning; progressive enhancement; when each fails |
| `content/02-model-selection.xml` | Model tier routing, cost comparison (2025-2026), latency budgets, multi-model routing pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-selection-record.md` | Decision record template: requirements, options considered, cost projection, success metrics |
| `templates/litellm-router.py` | LiteLLM complexity-based routing: simple→DeepSeek, balanced→Sonnet, complex→Opus |
