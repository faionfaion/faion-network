# Prompt Patterns for Common Dev Tasks

## Summary

**One-sentence:** A reusable rubric of 6 named prompt patterns (Refactor, Explain-Diff, Bug-Repro, Spec-to-Test, Doc-from-Code, Reverse-Stack-Trace) with required slots and a quality score.

**One-paragraph:** A reusable rubric of 6 named prompt patterns (Refactor, Explain-Diff, Bug-Repro, Spec-to-Test, Doc-from-Code, Reverse-Stack-Trace) with required slots and a quality score. Each pattern lists the required slots (intent, inputs, format, success criterion) and a score 0-3 the operator self-rates before sending. Scores <2 are blocked. Decision tree, output contract, failure modes, and the decision tree live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Developer issues 5+ prompts per day to a coding agent and wants reusable shapes.
- Team has no shared prompt vocabulary; everyone reinvents.
- Quality of agent output varies wildly because intent and inputs are inconsistent.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Developer issues 5+ prompts per day to a coding agent and wants reusable shapes.
- Team has no shared prompt vocabulary; everyone reinvents.
- Quality of agent output varies wildly because intent and inputs are inconsistent.

## Skip If (ANY kills it)

- Developer uses only ghost-text completion — patterns don't apply.
- Task is one-off creative exploration where bounded shape is counterproductive.
- Team already runs an internal prompt library with equivalent rubric — adopt theirs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent prompt log | chat transcript | Claude Code / Cursor history |
| Pattern catalogue | this methodology's rubric | content/01-core-rules.xml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pair-with-ai-agent-protocol]] | Session protocol the patterns slot into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-prompt` | haiku | Mechanical rubric scoring against the 4 slots. |
| `rewrite-low-score` | sonnet | Rewrite a sub-2 prompt to satisfy all slots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt_template.md` | Markdown skeleton for the artefact. |
| `templates/rubric.json` | JSON template scaffolding the artefact contract. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-patterns-for-common-dev-tasks.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[pair-with-ai-agent-protocol]]
- [[code-review-process]]
- [[prompt-engineering]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the prompt asking for code, tests, docs, or a structured artefact?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
