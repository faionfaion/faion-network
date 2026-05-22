---
slug: ollama-tool-calling
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Wires tool calling against an Ollama model: schema declaration, fallback JSON-mode parser, repair loop, and validation against the JSON Schema.
content_id: "c56516d6395257f7"
complexity: medium
produces: code
est_tokens: 4300
tags: [ollama, tool-calling, function-calling, local-llm, json-schema]
---
# Ollama Tool Calling and Structured Outputs

## Summary

**One-sentence:** Wires tool calling against an Ollama model: schema declaration, fallback JSON-mode parser, repair loop, and validation against the JSON Schema.

**One-paragraph:** Wires tool calling against an Ollama model: schema declaration, fallback JSON-mode parser, repair loop, and validation against the JSON Schema. The methodology assumes the inputs in Prerequisites and produces a `code` artefact validated by `scripts/validate-ollama-tool-calling.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Developers building agents on local Ollama models where native tool calling support is partial or quantisation-fragile.

## Applies If (ALL must hold)

- Building a local agent that needs to call external tools or APIs without cloud API costs.
- Extracting structured data (entities, classifications, analysis) from text with schema validation.
- Replacing cloud LLM tool-calling in CI pipelines or privacy-sensitive workflows.
- Testing agent tool-calling logic locally before deploying against cloud models.

## Skip If (ANY kills it)

- Models smaller than 13B — tool calling reliability degrades significantly; Llama 3.1 8B is the practical minimum.
- Context window below 32k — the model returns text instead of JSON tool calls silently.
- Complex multi-tool chains where frontier cloud models (GPT-4o, Claude) produce significantly more reliable results.
- Structured output schemas with deeply nested objects — compliance varies by model; test thoroughly before production.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ollama-python-client]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `scripts/validate-ollama-tool-calling.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[ollama-python-client]]
- [[tool-use-function-calling]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-tool-calling` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
