---
slug: cot-techniques
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced reasoning patterns beyond zero-shot CoT: Tree of Thoughts (ToT) for branching decisions, Least-to-Most for sequential sub-dependencies, and Self-Consistency for high-stakes answers.
content_id: "d5b52e4f362adf19"
tags: [chain-of-thought, tree-of-thoughts, least-to-most, self-consistency, advanced-prompting]
---
# Chain-of-Thought Advanced Techniques

## Summary

**One-sentence:** Advanced reasoning patterns beyond zero-shot CoT: Tree of Thoughts (ToT) for branching decisions, Least-to-Most for sequential sub-dependencies, and Self-Consistency for high-stakes answers.

**One-paragraph:** Advanced reasoning patterns beyond zero-shot CoT: Tree of Thoughts (ToT) for branching decisions, Least-to-Most for sequential sub-dependencies, and Self-Consistency for high-stakes answers. Always start with zero-shot CoT ("Think step by step.") — it solves 70–80% of cases. Escalate to advanced techniques only when zero-shot fails.

## Applies If (ALL must hold)

- Multi-step reasoning where zero-shot CoT still produces wrong answers.
- Branching solution paths (architecture choices, algorithm selection) — use Tree of Thoughts.
- Sequential sub-dependencies (build order, migration path) — use Least-to-Most decomposition.
- Verification pipelines where the model must self-check before returning.
- Agent planning steps requiring reasoning about which tool to call next.

## Skip If (ANY kills it)

- Simple factual lookups — CoT inflates token usage without improving accuracy.
- Classification tasks with 3–5 clear categories — few-shot without CoT is cheaper.
- High-throughput pipelines where latency matters — each ToT branch is a separate API call.
- When self-consistency requires 5–10 samples — cost multiplies linearly; benchmark gain vs. cost first.

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

- parent skill: `geek/ai/llm-integration/`
