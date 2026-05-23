---
slug: inference-cost-unit-economics
tier: pro
group: ai
domain: ai-core
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Report quantifying per-feature inference cost (tokens × price + retrieval + tools), gross margin per feature, and the cost-per-successful-outcome — not cost-per-call.
content_id: "482a7b267ba4e242"
complexity: medium
produces: report
est_tokens: 4900
tags: [unit-economics, inference-cost, finops, gross-margin, cost-per-outcome]
---

# Inference Cost Unit Economics

## Summary

**One-sentence:** Report quantifying per-feature inference cost (tokens × price + retrieval + tools), gross margin per feature, and the cost-per-successful-outcome — not cost-per-call.

**One-paragraph:** Report quantifying per-feature inference cost (tokens × price + retrieval + tools), gross margin per feature, and the cost-per-successful-outcome — not cost-per-call. This methodology codifies the rules, output contract, failure modes, and decision tree needed for a report produced by an agent applying inference cost unit economics. The deliverable is validated against an explicit JSON Schema and routed through a decision tree that maps observable signals to rule ids in `01-core-rules.xml`.

**Ефективно для:**

- Building a reproducible report for inference cost unit economics across teams.
- Reviewing AI-or-human work against an explicit contract instead of vibes.
- Wiring the output into downstream automation (CI gates, observability, post-mortems).
- Avoiding the failure modes listed in `03-failure-modes.xml`.

## Applies If (ALL must hold)

- AI feature has paying users or a path to revenue and gross-margin matters
- feature uses LLM calls + retrieval + tools whose costs vary per invocation
- the team can attribute cost to feature and feature to revenue (or to value proxy)

## Skip If (ANY kills it)

- feature is internal-tooling only with no revenue model — track cost but skip the unit-economics framing
- feature is one-shot research, not a recurring product surface — use ad-hoc cost report instead
- billing data is not yet attributable to features — fix attribution first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-call cost decomposition (tokens in/out + retrieval + tool) | logging | platform |
| Feature attribution (calls → feature) | telemetry | ml-engineering |
| Revenue or value-proxy attribution per feature | analytics | product |
| Outcome definition per feature (success metric) | product spec | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-feature-observability-four-pillars]] | Observability pillar 4 — cost — feeds this report |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounding the methodology with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the deliverable + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 800 |
| `content/05-examples.xml` | essential | Worked example from real engagement | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cost_decomposition` | sonnet | Break cost into tokens / retrieval / tool components. |
| `outcome_attribution` | opus | Map calls → successful outcomes (not just calls). |
| `margin_synthesis` | opus | Cost-per-outcome + gross-margin per feature. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit-economics-report.md` | Report skeleton |
| `templates/cost-decomposition.json` | Cost-decomposition JSON schema |
| `templates/_smoke-test.md` | Minimum viable filled-in unit-economics report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-inference-cost-unit-economics.py` | Validate the report artefact against the 02-output-contract schema | After subagent returns, before commit/publish |

## Related

- [[ai-call-site-inventory]]
- [[ai-feature-observability-four-pillars]]
- [[ai-feature-progressive-rollout]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from inputs and intermediate artefacts to a rule from `01-core-rules.xml`, telling the agent which variant of the methodology to apply or when to stop. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
