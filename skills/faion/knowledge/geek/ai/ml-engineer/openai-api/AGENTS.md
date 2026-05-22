---
slug: openai-api
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Integrates OpenAI Chat Completions / Responses API with pinned model versions, Structured Outputs, Batch API, max_tokens, retries, and prompt-cache hits.
content_id: "cc027a7b2fe0a111"
complexity: medium
produces: code
est_tokens: 4300
tags: [openai, llm-api, structured-output, function-calling, batch-processing]
---
# OpenAI API Integration

## Summary

**One-sentence:** Integrates OpenAI Chat Completions / Responses API with pinned model versions, Structured Outputs, Batch API, max_tokens, retries, and prompt-cache hits.

**One-paragraph:** Integrates OpenAI Chat Completions / Responses API with pinned model versions, Structured Outputs, Batch API, max_tokens, retries, and prompt-cache hits. The methodology assumes the inputs in Prerequisites and produces a `code` artefact validated by `scripts/validate-openai-api.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Python and TypeScript engineers shipping production features on the OpenAI API with cost and reliability discipline.

## Applies If (ALL must hold)

- Production app requiring best-in-class structured output with native schema enforcement
- Vision tasks requiring GPT-4o's image understanding
- Batch processing of non-time-sensitive data (50% cost discount via Batch API)
- Function calling / tool use as the primary agentic mechanism
- Audio transcription (Whisper) or TTS in agent pipelines

## Skip If (ANY kills it)

- Privacy-sensitive data that must not leave your infrastructure (use local Ollama instead)
- Very long context (>128K tokens) — use Claude (200K) or Gemini (2M)
- When Anthropic Claude's instruction-following is more reliable for your specific task
- Tight budget with high-volume simple tasks — Gemini Flash ($0.10/M) is cheaper than gpt-4o-mini ($0.15/M)

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[claude-api]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `generate-skeleton` | sonnet | Boilerplate + schema scaffolding. |
| `fill-business-logic` | opus | Domain-judgment-heavy core logic. |
| `lint-and-test` | haiku | Mechanical checks against the contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.py` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/skeleton.py` | Working code skeleton showing the produced shape with the contract types. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openai-api.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[claude-api]]
- [[structured-output]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `openai-api` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
