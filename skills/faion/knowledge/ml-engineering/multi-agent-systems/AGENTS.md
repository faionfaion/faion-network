# Multi-Agent Systems

## Summary

**One-sentence:** Specifies a production multi-agent system: agent roster, message contract, shared state, error-recovery, observability, and termination conditions.

**One-paragraph:** Specifies a production multi-agent system: agent roster, message contract, shared state, error-recovery, observability, and termination conditions. The methodology assumes the inputs in Prerequisites and produces a `spec` artefact validated by `scripts/validate-multi-agent-systems.py`. Five testable rules in `content/01-core-rules.xml` gate the work; failure modes in `content/03-failure-modes.xml` cover the most common ways the application goes wrong. The decision tree in `content/06-decision-tree.xml` routes the agent from the input shape to the right rule, so the methodology is safe to skip when preconditions do not hold.

**Ефективно для:** AI engineers building production multi-agent systems with explicit orchestration, retry policies, and tracing.

## Applies If (ALL must hold)

- Task requires parallel specialized work: research + coding + review happening simultaneously
- Problem is too large for a single context window
- Workflow has natural role boundaries (planner, executor, critic, verifier)
- Iterative refinement loops benefit from adversarial agents (generator vs. critic)
- Long-running pipelines where intermediate outputs need validation checkpoints

## Skip If (ANY kills it)

- Simple, linear task a single agent completes in one pass
- Low latency required — multi-agent adds orchestration overhead (2-5x latency)
- Budget is tight — multiple agents multiply token spend
- Team lacks observability tooling — debugging multi-agent failures is hard without traces

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[multi-agent-design-patterns]]` | Adjacent context the agent normally already has when this methodology fires. |

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
| `scripts/validate-multi-agent-systems.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- [[multi-agent-design-patterns]]
- [[agents-production-deployment]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `multi-agent-systems` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.
