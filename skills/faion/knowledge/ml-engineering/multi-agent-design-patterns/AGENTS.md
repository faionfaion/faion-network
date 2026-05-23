# Multi-Agent Design Patterns

## Summary

**One-sentence:** Picks the multi-agent topology (orchestrator-worker, hierarchical, sequential, parallel, debate) for a given workflow and emits a versioned design decision-record.

**One-paragraph:** Picks the multi-agent topology (orchestrator-worker, hierarchical, sequential, parallel, debate) for a given workflow and emits a versioned design decision-record. The methodology assumes the inputs in Prerequisites and produces a `decision-record` artefact validated by `scripts/validate-multi-agent-design-patterns.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** AI agent architects choosing between hand-off, supervisor, and committee patterns for production multi-agent systems.

## Applies If (ALL must hold)

- Single agent context window is insufficient for the full task
- Tasks have parallelizable subtasks (research + writing + validation can run concurrently)
- Domain expertise must be isolated — a billing agent must not have access to CRM tools
- Enterprise workflows map naturally to organizational units (teams, departments, roles)
- Reliability requires cross-checking: parallel agents can validate each other's outputs

## Skip If (ANY kills it)

- Simple single-step tasks — multi-agent adds coordination overhead with no benefit
- Latency is critical (<2s) — agent-to-agent round trips add 500ms–2s each
- The problem is not well-decomposed yet — build a working single agent first, then extract workers
- Token budget is constrained — multi-agent systems use significantly more tokens per task

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[multi-agent-systems]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `score-options` | sonnet | Rubric application. |
| `recommend` | opus | Multi-criterion trade-off. |
| `format-record` | haiku | Template bind. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/decision-record.md.tmpl` | Markdown decision-record skeleton with criteria, scores, recommendation. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-design-patterns.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[multi-agent-systems]]
- [[ai-agent-patterns]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `multi-agent-design-patterns` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
