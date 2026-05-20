---
slug: fine-tune-vs-prompt-decision-tree
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Opinionated decision tree on WHEN finetune beats prompt+RAG+routing on cost-quality-latency-maintenance axes — engineers over-finetune without it.
content_id: "c862a545a1351565"
tags: [fine-tune-vs-prompt-decision-tree, ai, geek]
---

# Fine-tune vs Prompt+RAG Decision Tree

## Summary

**One-sentence:** Opinionated decision tree on WHEN finetune beats prompt+RAG+routing on cost-quality-latency-maintenance axes — engineers over-finetune without it.

**One-paragraph:** Faion has fine-tuning-openai-* and lora-qlora HOW. Missing: an opinionated decision tree on WHEN finetune beats prompt+RAG+routing. Engineers over-finetune. Output: decision tree + decision record + revisit triggers.

## Applies If (ALL must hold)

- team considering fine-tuning a model
- ≥1 production workflow with eval set
- either cost, quality, or latency is below target

## Skip If (ANY kills it)

- research / exploration with no production constraint
- compliance requirement forcing on-prem fine-tune (decision pre-made)
- no eval set — build eval first

## Prerequisites

- eval set ≥100 cases (smaller is too noisy for fine-tune ROI)
- current cost, quality, latency baseline
- list of alternatives tried (better prompting, RAG, routing, distillation)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents` | parent skill — provides operating context for this methodology |
| `geek/ai/fine-tuning-openai-supervised` | peer methodology — produces inputs or consumes outputs |
| `geek/ai/lora-qlora` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer methodology: `geek/ai/fine-tuning-openai-supervised`
- peer methodology: `geek/ai/lora-qlora`
- peer methodology: `geek/ai/llm-cascade-routing`
- external: https://platform.openai.com/docs/guides/fine-tuning; https://arxiv.org/abs/2106.09685 (LoRA); https://www.anthropic.com/news/prompt-caching
