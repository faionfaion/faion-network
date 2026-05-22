---
slug: llm-classifier-design
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a cost-minimised LLM classifier — single forced tool call, batched by numeric id, prompt cache on the system prefix, calibrated judge.
content_id: "65ffa4c52aba6b6d"
complexity: medium
produces: code
est_tokens: 3000
tags: [classifier, llm, structured-output, batching, prompt-cache]
---
# LLM Classifier Design

## Summary

**One-sentence:** Produces a cost-minimised LLM classifier — single forced tool call, batched by numeric id, prompt cache on the system prefix, calibrated judge.

**One-paragraph:** When the model's job is "look at this and emit one structured verdict", a multi-turn chat shape is overkill. Force the answer through a single tool call (tool_choice="extract"), batch items by numeric id inside one prompt, cache the long system prefix between batches, pick the smallest model that hits the κ target after calibration. Result: 10-100x cheaper than naive per-item chat calls without quality loss for fixed-shape verdicts.

**Ефективно для:** sufficiency audit, spam triage, intent detection, content gating, dedup matching, rubric grading.

## Applies If (ALL must hold)

- Output shape is fixed (enum, JSON object, score) and known upfront.
- ≥100 items per run (batching amortises overhead).
- Calibration set available to pick model + threshold per `[[judge-calibration-protocol]]`.
- Cost matters more than per-item explanation.

## Skip If (ANY kills it)

- Output shape unknown — open generation needed.
- Multi-step reasoning materially helps — use Extended Thinking, not single tool call.
- &lt;100 items — overhead of designing the classifier exceeds per-item cost saving.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Item batch | JSONL | data pipeline |
| Output schema | JSON Schema | spec |
| Calibration holdout | JSONL | judge calibration |
| Smallest viable model | string | model card / eval |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[judge-calibration-protocol]]` | Calibrates the classifier as a judge. |
| `[[claude-tool-use]]` | Forced-tool pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 rules: single tool call, smallest model after κ, batch by numeric id, cache system prefix, output one structured answer, eval calibration | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for classifier-config.json + batch input + verdicts shape | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: chat-shape per item, oversized model, no cache, no calibration, freeform output | ~600 |
| `content/04-procedure.xml` | medium | 6-step: define schema → pick model → wire tool → batch → calibrate → ship | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "fixed-shape verdict at scale (≥100 items)?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Design schema | sonnet | Schema authoring. |
| Pick model | opus | Multi-axis tradeoff. |
| Run calibration | haiku | Numerical. |
| Operate batch | runtime | Mechanical. |

## Templates

| File | Purpose |
|---|---|
| `templates/classifier-config.schema.json` | JSON Schema for classifier-config.json. |
| `templates/classifier-runner.py` | Reference batched runner with prompt-cache + forced tool call. |
| `templates/system-prefix.md` | Cacheable system prefix template. |
| `templates/_smoke-test.json` | Minimum valid classifier-config. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llm-classifier-design.py` | Validates classifier-config: schema present, model pinned, batch size sane, calibration κ ≥0.7. | Pre-commit on config. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[judge-calibration-protocol]]`
- `[[claude-tool-use]]`
- `[[function-calling-patterns]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` checks fit: small batches → skip; open-ended output → skip; fixed-shape at scale → run-the-checklist.
