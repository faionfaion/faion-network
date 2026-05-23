---
slug: test-tdd-red-green-split-agents
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces two scoped sub-agent SKILL files (RED writes tests only, GREEN edits sources only) so the TDD loop runs across disjoint tool permissions and a single agent cannot edit the test to pass.
content_id: "774b380a74dd4f1f"
complexity: medium
produces: config
est_tokens: 4200
tags: [tdd, red-green, sub-agents, tool-permissions, sdlc-ai]
---
# TDD with Red and Green in Separate Agents

## Summary

**One-sentence:** Split the TDD loop: RED sub-agent can write tests/ + read sources but not edit; GREEN sub-agent can edit sources + read failing test output but not modify the test file; orchestrator asserts a real RED→GREEN transition.

**One-paragraph:** When an AI coding agent runs the TDD loop, the test-writer (RED) and the implementer (GREEN) must execute in separate sub-agents with non-overlapping tool permissions: RED can write to `tests/` and read sources but cannot edit them; GREEN can edit sources and read the failing test output but cannot modify the test file. The orchestrator passes only the acceptance criterion to RED, only the test diff and pytest/jest failure to GREEN, and asserts a real RED→GREEN transition before merging. Without the split, a single agent that owns both files cheats by editing the test to pass.

**Ефективно для:**

- Coding-agent TDD, де single-agent любить cheat editing tests.
- Sub-agent infra: Claude Code, Cursor background, Devin.
- Compliance: split-identity audit trail для critical paths.
- Onboarding agent fleet — clean RED/GREEN responsibility split.

## Applies If (ALL must hold)

- TDD discipline expected for the change.
- Sub-agent infrastructure available (Claude Code sub-agents, Cursor agents, etc.).
- Test file and source file live in clearly separable directories.

## Skip If (ANY kills it)

- No sub-agent infra — single-agent fleet only.
- Test and source intermixed (e.g., doctests) where the split is not enforceable.
- Change is a one-line bugfix where a single existing test already covers it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Sub-agent infra (Claude Code SKILL.md or equivalent) | config | team setup |
| Acceptance criterion (one sentence) | Markdown | ticket |
| Test runner (pytest / jest / etc.) | binary | repo deps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tdd-red.skill.md` | SKILL.md for the RED sub-agent with disjoint tool whitelist. |
| `templates/tdd-green.skill.md` | SKILL.md for the GREEN sub-agent with disjoint tool whitelist. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-tdd-red-green-split-agents.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-property-based-llm-invariants]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
