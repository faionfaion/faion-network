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
- Pattern choice is not yet locked in — still architecting, not implementing
- The decision will be persisted as an SDD design.md / ADR entry

## Skip If (ANY kills it)

- Simple single-step tasks — multi-agent adds coordination overhead with no benefit
- Latency is critical (<2s) — agent-to-agent round trips add 500ms–2s each
- The problem is not well-decomposed yet — build a working single agent first, then extract workers
- Token budget is constrained — multi-agent systems use significantly more tokens per task
- Implementation already committed and the pattern is locked in — go straight to the relevant impl methodology

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Task brief | markdown | upstream agent or human |
| Constraints | yaml | project config |
| Acceptance criteria | list | spec / ticket |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[multi-agent-systems]]` | Adjacent context the agent normally already has when this methodology fires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Ten testable rules with rationale and source — five on mesh operation (tiering, handoff contracts, termination, tracing), five on topology selection and the decision record. | ~1600 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples; payload carries the 8-pattern enum with conditional requirements (blackboard needs a concurrency plan, router needs classifier accuracy ≥0.85). | ~1000 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom / root-cause / fix — infinite loop, token explosion, shared-state race, pattern stacking, router without a classifier, blackboard without locking, same-model generator and critic, missing HITL gates. | ~1400 |
| `content/04-procedure.xml` | medium | Five-step procedure with decision-gates. | ~700 |
| `content/05-examples.xml` | medium | One end-to-end worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Topology-selection tree on observable signals (irreversible actions, classifier accuracy, shared mutable state, critique, iteration, parallelisability, manager need), each leaf naming the pattern and its rule ref. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-options` | sonnet | Rubric application. |
| `recommend` | opus | Multi-criterion trade-off. |
| `format-record` | haiku | Template bind. |

## Templates

| File | Purpose |
|------|---------|
| `templates/_smoke-test.md.j2` | Minimum-viable filled-in example used by the validator self-test. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example used by the validator self-test. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decision-record.md.tmpl` | Markdown decision-record skeleton with criteria, scores, recommendation. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-multi-agent-design-patterns.py` | Validate an output artefact against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[multi-agent-systems]]
- [[ai-agent-patterns]]
- parent skill: `geek/ai/ml-engineer/`

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` walks the agent from the input shape to a concrete rule id in `01-core-rules.xml`. Use it before applying any rule: the root question filters whether `multi-agent-design-patterns` applies at all; branches narrow on observable input fields; every leaf is a `<conclusion ref="...">` pointing at a rule id, so the agent never lands on free-text guidance.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/decision-record.md.tmpl`

```markdown
-->

# multi-agent-design-patterns — decision-record skeleton

> Replace every `TODO` block before handing off. The skeleton is wired to the schema in `content/02-output-contract.xml`; run `scripts/validate-multi-agent-design-patterns.py` after filling.

## Inputs

- Task brief: <link>
- Constraints: <link>

## Body

- TODO — section 1
- TODO — section 2
- TODO — section 3

## Acceptance

- All required keys present per the output contract.
- `forbidden_seen` is empty.
- Validator exits 0.

## Signature

- `signature: sha1(slug + version + date)[:16]`
```
