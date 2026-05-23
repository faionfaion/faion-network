# Structured Output Basics

## Summary

**One-sentence:** Reliable LLM JSON output: provider-native structured outputs (OpenAI response_format=json_schema, Anthropic tool-as-schema), Pydantic validation, retry-on-parse-fail.

**One-paragraph:** Provides the smallest production pattern for getting structured data out of an LLM without parser thrash: define a Pydantic model, pass it via the provider's structured-output mode (OpenAI `response_format` with json_schema, Anthropic tool-as-schema), validate the response, and on parse failure retry once with the validation error injected into the prompt. Covers OpenAI / Anthropic / Gemini differences, when JSON mode is enough vs json_schema, and the strict=true escape hatch.

**Ефективно для:** Backend дев, що тягне LLM-відповідь в БД і ловить раз на день «expected dict, got list», має закрити цикл за один захід.

## Applies If (ALL must hold)

- you need the LLM to return a known-shape JSON object
- Pydantic (or zod / dataclass) is available in the runtime
- task quality is sensitive to schema validity (DB insert, downstream agent)
- provider supports either response_format=json_schema or tool-as-schema
- you can retry once on parse failure

## Skip If (ANY kills it)

- output is genuinely free-form prose (essay, draft, response)
- schema not yet stable — design schema first, then return here
- you can't afford the extra latency of `strict=true` mode (rare)
- downstream consumer tolerates raw markdown — no schema needed

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-structured-output-basics.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/extraction-schema.py` | Pydantic schema template for extraction |
| `templates/claude-extract.py` | Anthropic tool-as-schema extraction example |
| `templates/openai-extract.py` | OpenAI response_format=json_schema extraction example |
| `templates/retry-on-parse-fail.py` | 1-shot retry helper injecting validation error |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-output-basics.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-schema-first`, `r2-provider-native`, `r3-validate-on-receipt`, `r4-retry-on-parse-fail`, `r5-strict-when-stakes-high` from `content/01-core-rules.xml`.
