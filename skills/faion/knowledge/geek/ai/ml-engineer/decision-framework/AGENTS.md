---
slug: decision-framework
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a decision record naming the AI approach (prompt / RAG / fine-tune / hybrid) and the model tier for a given task, with progressive-enhancement justification and a quarterly re-evaluation clause.
content_id: "df-001ai-2345decision"
complexity: deep
produces: decision-record
est_tokens: 4000
tags: [decision-record, model-selection, rag, fine-tuning, routing, finops]
---
# ML/AI Decision Framework

## Summary

**One-sentence:** Emits a versioned decision record that picks one of {prompt, RAG, fine-tune, hybrid} and the model tier {haiku/sonnet/opus or deepseek/gpt-mini/gpt-frontier} for a new AI feature, applying progressive enhancement and quarterly re-evaluation.

**One-paragraph:** Defaulting to frontier models for every task overspends 2-3×; defaulting to fine-tuning rarely beats prompting+RAG below ~1M req/month due to 6× inference cost + dataset upkeep. This methodology forces an explicit decision-record: start with prompt engineering, escalate to RAG only when external/private/changing data is required, escalate to fine-tuning only when behavioral specialization at scale is needed. Model tier is chosen by complexity routing — Haiku/DeepSeek for extraction/classification, Sonnet/GPT-4o for standard generation, Opus for irreversible-error tasks. The record is dated and tagged with quarterly_review_due so deprecations and pricing shifts don't silently lock teams into the wrong choice.

**Ефективно для:**

- Старту нової AI-фічі, коли треба обрати один з prompt / RAG / fine-tune і записати, чому саме він.
- Аудиту наявного pipeline, коли spend росте і виникає підозра на модельний overshoot.
- Депрекацій (модель знімається з API) — пере-оцінка з фіксованим framework замість "що дешевше прямо зараз".
- Архітектурної ради перед інвестицією в fine-tuning: блокує дороге рішення без ROI-обґрунтування.
- Командам, які перевищують свій SLA по latency, але не знають, чи це prompt, чи модель, чи retrieval.

## Applies If (ALL must hold)

- A new or rebooted AI feature requires choosing between prompt / RAG / fine-tune / hybrid.
- The team has at least the task's input/output shape, expected volume, and quality SLO.
- The decision affects ≥1 production code path (not a one-off prototype).

## Skip If (ANY kills it)

- Task is trivial AND model already decided in prior decision-record — don't redo work.
- Imminent deadline (<48h) — pick safe default (Sonnet + prompting) and create a follow-up review item; do not delay shipping for the framework.
- Pure creative output (marketing copy, story generation) — model quality is subjective; user-preference testing matters more.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task spec (input shape, output shape, SLO) | Markdown | Product brief |
| Expected request volume | number / period | Product / analytics |
| Data inventory (private, public, change frequency) | Markdown | Engineering directory |
| Quality SLO + golden eval set (5-50 examples) | rubric + JSONL | QA team |
| Budget envelope per request | USD / 1k req | FinOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is the upstream decision; nothing else loads before it. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: progressive enhancement, RAG-only-when-data-changes-or-private, FT-only-at-scale, complexity-routing, quarterly-review-clause, no-FT-for-factual | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision record: chosen approach, model tier, rationale per axis, quarterly_review_due | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: default-to-frontier, RAG-on-small-corpus, FT-without-ROI, no-quarterly-review, override-without-record | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure: scope → data → approach → model → quarterly-review | 600 |
| `content/05-examples.xml` | reference | 3 worked decisions: support-bot (RAG+Sonnet), domain-tone-rewriter (FT+Haiku), realtime-classifier (prompt+Haiku) | 600 |
| `content/06-decision-tree.xml` | essential | Approach tree → model tree → quarterly-review tag | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_task_brief` | haiku-4-5 | Cheap structured extraction from product brief. |
| `draft_decision_record` | sonnet-4-6 | Multi-input synthesis: brief + data inventory + budget. |
| `challenge_decision` | opus-4-7 | Devil's advocate pass with extended thinking on irreversibility. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-selection-record.md` | Decision-record Markdown skeleton. |
| `templates/litellm-router.py` | LiteLLM complexity-based router config snippet. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-framework.py` | Validate a decision-record JSON against the contract. | Pre-commit on the record file; before opening the architecture-review PR. |

## Related

- [[cost-optimization]] — consumes this decision and prices each axis.
- [[claude-api]] — implements the chosen tier on the Anthropic path.
- [[finetuning]] — runs the FT track when this decision says fine-tune.

## Decision tree

See `content/06-decision-tree.xml`. The tree walks two axes. Approach axis: is the data private/changing-frequently/cite-required → RAG; is behavior (writing style, persona, jargon) the specialization need AND volume ≥1M/month → fine-tune; otherwise prompt. Model axis (conditional on approach): simple extraction/classification → Haiku/DeepSeek; standard generation → Sonnet/GPT-4o; irreversible-error or deep reasoning → Opus. Every leaf tags the record with quarterly_review_due so pricing shifts and deprecations force re-evaluation.
