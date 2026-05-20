---
slug: llm-judge-rubric-evidence-first
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When you cannot use exact-match or unit-test checks (open-ended outputs: summaries, code review, plans, agent transcripts), use another LLM as a judge — but only with a structured rubric, JSON output, evidence cited BEFORE the score, per-criterion scoring, and explicit mitigation of position/verbosity/self-preference/authority bias.
content_id: "d20f29345fd86535"
tags: [evaluation, llm-judge, rubric, bias-mitigation, evals]
---
# LLM-as-Judge — Rubric, Evidence-First, Bias-Mitigated

## Summary

**One-sentence:** When you cannot use exact-match or unit-test checks (open-ended outputs: summaries, code review, plans, agent transcripts), use another LLM as a judge — but only with a structured rubric, JSON output, evidence cited BEFORE the score, per-criterion scoring, and explicit mitigation of position/verbosity/self-preference/authority bias.

**One-paragraph:** When you cannot use exact-match or unit-test checks (open-ended outputs: summaries, code review, plans, agent transcripts), use another LLM as a judge — but only with a structured rubric, JSON output, evidence cited BEFORE the score, per-criterion scoring, and explicit mitigation of position/verbosity/self-preference/authority bias. "Rate 1-10" prompts are not evals; they are noise generators.

## Applies If (ALL must hold)

- Evaluating open-ended agent outputs where exact-match is impossible (summaries, plans, multi-turn dialogue).
- Grading code review comments, refactor plans, or other reasoning artifacts.
- Pairwise comparison of two agent variants on the same task set.
- Building a regression suite for prompt or model changes that touch generation quality.

## Skip If (ANY kills it)

- Output is verifiable deterministically (compiles, passes tests, matches schema) — judges add cost and noise; use the deterministic check first.
- Single-LLM stack on borderline cases — self-preference bias is unfixable; bring in a second model family for cross-judging.
- Privacy-sensitive outputs you cannot send to a third-party judge — keep evals local or skip.
- Throwaway prototypes — overhead of rubric design is not justified before the agent is real.

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

- parent skill: `geek/ai/ai-agents/`
