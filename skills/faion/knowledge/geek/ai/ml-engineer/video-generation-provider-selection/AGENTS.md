---
slug: video-generation-provider-selection
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Picks the cheapest provider whose capability matrix covers the task constraints (duration, audio, lip-sync, resolution) before any integration code is written.
content_id: "f3906a1739b8f109"
complexity: medium
produces: decision-record
est_tokens: 3400
tags: [video-generation, runway, luma, sora, provider-selection]
---
# AI Video Generation Provider Selection

## Summary

**One-sentence:** Picks the cheapest provider whose capability matrix covers the task constraints (duration, audio, lip-sync, resolution) before any integration code is written.

**One-paragraph:** Each AI-video provider (Runway, Luma, Sora 2, Veo 3, Replicate, Kling) excels at a narrow slice: lip-sync, native audio, duration, 4K, custom fine-tunes. Picking the wrong provider either wastes credits on inferior quality or blocks the pipeline when a required capability is absent. This methodology selects a provider by hard-matching the task's mandatory capabilities against the 2026 matrix.

**Ефективно для:**

- New video pipeline build: prevents 2-week integration rewrites when picked provider lacks lip-sync/audio.
- Provider switch under cost or quality pressure: gives an apples-to-apples re-evaluation.
- Multi-provider abstraction: decides which 2-3 providers actually need an adapter.
- RFP / vendor briefing: produces a defensible scoring rubric.

## Applies If (ALL must hold)

- Selecting a provider before starting any video generation integration.
- Evaluating provider capabilities for a new content pipeline (news, social media, marketing).
- Switching providers due to API access changes, cost, or quality regression.
- Building a multi-provider abstraction and deciding which providers to include.

## Skip If (ANY kills it)

- Provider already selected and integration is underway — refer to async-api or production-service methodologies instead.
- Precise character consistency across multiple shots is required — no current provider reliably delivers this.
- Video longer than 60 seconds from a single call is needed — all current APIs cap at 5-60s per generation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task spec | markdown | Product brief listing duration, resolution, audio, lip-sync, IP constraints |
| Expected volume | int (videos/month) | Pipeline estimate for cost modelling |
| Budget cap | USD/month | Hard ceiling for provider credit purchase |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `requirements_extract` | sonnet | Parse product brief into capability matrix. |
| `matrix_scoring` | haiku | Deterministic capability lookup; no creative work. |
| `decision_record` | sonnet | Write narrative justification + budget table. |

## Templates

| File | Purpose |
|------|---------|
| `templates/provider-matrix.md` | Markdown capability-matrix scoring sheet |
| `templates/decision-record.md` | Filled-in provider-selection decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-video-generation-provider-selection.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-provider-selection]]
- [[voice-agents]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Does the task require lip-sync OR native audio OR 4K? Branches route to a rule id from `content/01-core-rules.xml` (runway-when, veo-when, sora-when, ...) so every leaf is traceable to a testable statement.
