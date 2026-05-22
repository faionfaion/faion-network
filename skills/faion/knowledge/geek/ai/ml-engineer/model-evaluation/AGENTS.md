---
slug: model-evaluation
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a systematic LLM evaluation report covering quality, latency, cost, and safety across offline benchmarks, online A/B tests, and continuous production monitoring.
content_id: "611b9c6ae3a1b79e"
complexity: deep
produces: report
est_tokens: 4300
tags: [evaluation, llm, metrics, benchmarks, llm-judge]
---
# Model Evaluation

## Summary

**One-sentence:** Produces a systematic LLM evaluation report covering quality, latency, cost, and safety across offline benchmarks, online A/B tests, and continuous production monitoring.

**One-paragraph:** Produces a systematic LLM evaluation report covering quality, latency, cost, and safety across offline benchmarks, online A/B tests, and continuous production monitoring. The methodology assumes the inputs in Prerequisites and produces a `report` artefact validated by `scripts/validate-model-evaluation.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers gating model upgrades and prompt changes through reproducible offline + online evaluation pipelines.

## Applies If (ALL must hold)

- Selecting between two or more candidate models for a production use case
- Before promoting a prompt change or model upgrade to production
- After fine-tuning, to verify quality improvement over the base model
- Setting up continuous monitoring with alerts when quality drifts below threshold
- Running A/B tests to compare a new model against current production baseline

## Skip If (ANY kills it)

- Task is trivial and any capable model passes — skip formal evaluation, ship
- No baseline exists yet — gather production data first, then evaluate against it
- Purely synthetic benchmarks for a highly domain-specific task — use real query samples
- Budget does not allow LLM-as-judge at scale — use cheaper automated metrics as a proxy first

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-evaluation]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five testable rules with rationale and source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples for the output artefact. | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix. | ~800 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether the methodology applies, ending in rule refs. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-metrics` | sonnet | Deterministic metric computation. |
| `synthesize-narrative` | opus | Cross-metric story with caveats. |
| `format-report` | haiku | Template binding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/report.md.tmpl` | Markdown report skeleton: metrics table, narrative, caveats, attachments. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-evaluation.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-evaluation]]
- [[rag-evaluation]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `model-evaluation` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
