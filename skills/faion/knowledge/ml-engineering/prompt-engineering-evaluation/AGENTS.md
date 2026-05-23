# Prompt Engineering — Evaluation and Debugging

## Summary

**One-sentence:** Evaluates a prompt against a frozen eval suite with deterministic metrics, LLM-as-judge, regression tests, and per-iteration diff reports.

**One-paragraph:** Evaluates a prompt against a frozen eval suite with deterministic metrics, LLM-as-judge, regression tests, and per-iteration diff reports. The methodology assumes the inputs in Prerequisites and produces a `report` artefact validated by `scripts/validate-prompt-engineering-evaluation.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML engineers iterating on production prompts with quantitative regression gates rather than vibes-based promotion.

## Applies If (ALL must hold)

- Before deploying any prompt to production — all prompts need a minimum test coverage.
- After modifying an existing prompt — regression testing prevents new failures.
- When outputs are inconsistent across runs — debugging workflow identifies root cause.
- When comparing prompt variants — A/B framework gives a structured decision.
- When quality degrades in production — evaluation metrics quantify the regression.

## Skip If (ANY kills it)

- One-off exploratory prompts — full evaluation overhead is not justified.
- Prompts used only for synthetic data generation where output correctness is manually reviewed.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-fundamentals]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `compute-metrics` | sonnet | Deterministic metric computation. |
| `synthesize-narrative` | opus | Cross-metric story with caveats. |
| `format-report` | haiku | Template binding. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/report.md.tmpl` | Markdown report skeleton: metrics table, narrative, caveats, attachments. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-engineering-evaluation.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-fundamentals]]
- [[prompt-changelog-discipline]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `prompt-engineering-evaluation` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
