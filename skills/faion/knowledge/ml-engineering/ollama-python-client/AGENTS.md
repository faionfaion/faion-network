# Ollama Python Client Patterns

## Summary

**One-sentence:** Implements a Python Ollama client wrapper with retry, streaming, model warmup, JSON-mode parsing, and OpenTelemetry tracing.

**One-paragraph:** Implements a Python Ollama client wrapper with retry, streaming, model warmup, JSON-mode parsing, and OpenTelemetry tracing. The methodology assumes the inputs in Prerequisites and produces a `code` artefact validated by `scripts/validate-ollama-python-client.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** Python engineers integrating Ollama into agents, data pipelines, or services with production-grade observability.

## Applies If (ALL must hold)

- Building a Python application that calls a local Ollama instance.
- Needing concurrent batch processing with asyncio.
- Requiring streaming output for real-time UX.
- Generating embeddings locally for RAG pipelines.
- Processing images with local vision models.

## Skip If (ANY kills it)

- Production cloud deployment where OpenAI SDK with Ollama base_url override suffices — see ollama-agent-integration.
- Simple one-off scripting where the CLI (ollama run) is faster to use.
- TypeScript/JavaScript frontends — use the OpenAI-compatible REST API directly.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[ollama-agent-integration]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `scripts/validate-ollama-python-client.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[ollama-agent-integration]]
- [[ollama-deployment]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `ollama-python-client` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
