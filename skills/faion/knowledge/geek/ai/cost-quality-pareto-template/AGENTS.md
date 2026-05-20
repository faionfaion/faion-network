---
slug: cost-quality-pareto-template
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "7675f1a22f6d07fa"
summary: Standard Pareto template for LLM cost vs quality decisions — fixed axes, eval fixtures, plotting helper — so model-choice and config-choice decisions are defensible and reproducible.
tags: [llm-eval, cost-quality, pareto, model-selection, geek-ai, p7-llm-agent-dev]
---
# Cost-Quality Pareto Template

## Summary

**One-sentence:** A reusable Pareto-analysis template (fixed axes, fixture set, scoring rubric, plotting helper) for choosing between LLM models and configurations — replaces eyeballed "this seems good enough" with a defensible cost-quality curve.

**One-paragraph:** P7 LLM-agent developers face a constant decision: opus vs sonnet vs haiku, GPT-4 vs 4o vs mini, prompt-cached vs not, with-tools vs without. Each decision is currently made by vibes ("opus felt better"), which produces three failures: a) the wrong model gets picked because a bad test case dominated the impression, b) decisions cannot be replayed when a new SOTA model arrives, c) "we tested it" claims survive no scrutiny. This methodology pins a template: a fixed fixture set per use-case (held constant across model evals), a scoring rubric (3-5 dimensions with rater agreement), per-call cost and latency capture, and a plotting helper that renders the cost-quality Pareto. Output: a Pareto chart + decision memo per choice, archived for replay.

## Applies If (ALL must hold)

- The team is choosing between LLM models OR LLM configurations for a production-facing task.
- Task has a measurable quality dimension (correctness, faithfulness, helpfulness — not "vibes").
- A fixture set of at least 20 representative inputs is available or can be assembled.
- Decision will affect &gt; $100/month of LLM spend OR a high-traffic latency-sensitive path.

## Skip If (ANY kills it)

- Pre-prototype exploration — vibes are fast and the model choice is reversible.
- Internal-only tool with one user and trivial spend — analysis overhead exceeds benefit.
- Task lacks a scorable quality dimension — must define the rubric first.
- Single-model deployment with no contender — there's no comparison to make.

## Prerequisites

- Production task description and example inputs.
- Scoring rubric draft (correctness criteria, faithfulness criteria, etc.).
- LLM API access to candidates with cost/token metadata.
- A spreadsheet or notebook for results.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/structured-output-patterns` | Output capture and parsing for scoring assumed. |
| `geek/sdlc-ai/test-property-based-llm-invariants` | Sibling — invariant tests used as part of the rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: fixture freeze, multi-dim scoring, full-cost capture, replay metadata, Pareto frontier | ~1000 |
| `content/02-output-contract.xml` | essential | Pareto memo + chart + fixture archive shape | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: cherry-pick fixtures, single-rater, ignoring latency, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fixture-assembly` | sonnet | Bounded curation of representative inputs |
| `score-output` | opus or human | Per the scoring rubric; rater quality matters |
| `plot-pareto` | haiku | Mechanical: render the chart from results CSV |

## Templates

| File | Purpose |
|------|---------|
| `templates/fixtures.json` | Schema for fixture entries with input + expected behavior |
| `templates/scoring-rubric.md` | Multi-dimension rubric with rater instructions |
| `templates/pareto-memo.md` | Decision memo skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/run-eval.py` | Iterate fixtures × candidates; capture cost/latency/output | Eval run |
| `scripts/plot-pareto.py` | Render cost-vs-quality scatter + Pareto frontier | Post-eval |

## Related

- parent skill: `geek/ai/llm-integration/`
- peer methodology: `cost-vs-quality-decision-log`, `llm-eval-fundamentals`, `prompt-caching-strategy`
- external: [Anthropic evals guidance](https://docs.anthropic.com/en/docs/build-with-claude/evaluations) · [OpenAI evals](https://github.com/openai/evals)
