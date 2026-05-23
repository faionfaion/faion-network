# Prompt Changelog Discipline

## Summary

**One-sentence:** Pairs every prompt edit with a versioned changelog entry (hash + intent + eval delta + rollback hash) so production regressions can be traced to a specific change in minutes.

**One-paragraph:** Pairs every prompt edit with a versioned changelog entry (hash + intent + eval delta + rollback hash) so production regressions can be traced to a specific change in minutes. The methodology assumes the inputs in Prerequisites and produces a `spec` artefact validated by `scripts/validate-prompt-changelog-discipline.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** ML ops teams treating prompts as code: one file per prompt, eval-gated PRs, MTTR-optimised rollback paths.

## Applies If (ALL must hold)

- Working on a task whose output is `spec` aligned with prompt-changelog-discipline
- Have the inputs listed in Prerequisites available
- Need a reproducible, versioned artefact rather than ad-hoc notes

## Skip If (ANY kills it)

- Prototype throwaway code where the methodology overhead exceeds the regression risk
- Methodology preconditions cannot be met (no eval suite, no traffic, no team)

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[prompt-engineering-evaluation]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `scripts/validate-prompt-changelog-discipline.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[prompt-engineering-evaluation]]
- [[prompt-version-pinning-runbook]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `prompt-changelog-discipline` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
