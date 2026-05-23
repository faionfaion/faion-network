# Refusal Field Strict Schema

## Summary

**One-sentence:** Produces a structured-output spec that forces a `refusal` field at top level with strict schema mode so safety refusals surface in JSON instead of breaking the parse.

**One-paragraph:** When models refuse a request under structured output mode, they often emit free-form text that breaks JSON parsing. Adding an explicit top-level `refusal` field with strict mode forces the model to use it; downstream code can branch cleanly on present/absent refusal.

**Ефективно для:** team whose JSON schema agents hit JSONDecodeError once a week because the model refused mid-stream.

## Applies If (ALL must hold)

- Using OpenAI structured-output strict mode or Anthropic tool_use.
- Production agent encounters safety refusals.
- Downstream code expects JSON shape.

## Skip If (ANY kills it)

- Free-text completions (no schema).
- Internal agents on trusted prompts only.
- Refusals not expected (e.g., math).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `output-schema.json` | JSON Schema for the agent output | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-top-level-refusal; r2-strict-mode; r3-branch-on-refusal; r4-log-refusal-text; r5-no-refusal-in-prompt. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with detector + repair. | ~700 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | Worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision branches mapped to rule ids. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_input` | haiku | Mechanical. |
| `classify_drivers` | sonnet | Subjective tradeoffs. |
| `audit_output` | opus | Cross-cutting subtleties. |
| `emit_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/refusal-field-strict-schema-spec.md` | Markdown wrapper for the JSON spec. |
| `templates/_smoke-test.yaml` | Minimum input fixture. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-refusal-field-strict-schema.py` | Validates spec against the schema. | Pre-commit. |

## Related

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
