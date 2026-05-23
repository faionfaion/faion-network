# Prompt Engineering — Production Patterns

## Summary

**One-sentence:** Hardens prompts for production: model pinning, prompt-cache hits, latency budget, fallback strategies, prompt-injection defences, and observability hooks.

**One-paragraph:** Hardens prompts for production: model pinning, prompt-cache hits, latency budget, fallback strategies, prompt-injection defences, and observability hooks. The methodology assumes the inputs in Prerequisites and produces a `spec` artefact validated by `scripts/validate-prompt-engineering-production.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers deploying prompts to customer-facing latency-sensitive systems with cost and reliability SLOs.

## Applies If (ALL must hold)

- Any LLM call in a production pipeline where reliability matters.
- Structured output use cases where the downstream system depends on schema correctness.
- Tool-use and agent architectures where the model selects and calls external functions.
- Multi-turn agentic workflows where intermediate prompts are generated programmatically.
- Pipelines where prompt changes must be reviewed via git diff and rolled back if needed.

## Skip If (ANY kills it)

- Exploratory one-off prompts — versioning overhead is not justified.
- Prompts that are user-authored at runtime — manage as user content, not code artifacts.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-security]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `gather-requirements` | sonnet | Structured interview-style extraction. |
| `synthesize-spec` | opus | Cross-section trade-off synthesis. |
| `lint-output` | haiku | Schema validation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/spec.md.tmpl` | Markdown spec skeleton with the required sections + placeholders. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-engineering-production.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-security]]
- [[prompt-changelog-discipline]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `prompt-engineering-production` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
