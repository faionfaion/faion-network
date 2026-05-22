---
slug: tdd-workflow
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Red-Green-Refactor: write failing test, write minimal code, refactor without changing behaviour.
content_id: "27ccc09764ef490f"
complexity: light
produces: code
est_tokens: 3300
tags: [tdd, testing, red-green-refactor, verification, workflow]
---
# TDD Workflow

## Summary

**One-sentence:** Red-Green-Refactor: write failing test, write minimal code, refactor without changing behaviour.

**One-paragraph:** Red-Green-Refactor cycle for test-driven development: write one failing test, write minimal code to pass it, then improve structure without changing behaviour. Agents skip the RED step and write implementation first, then tests that validate what they wrote — this is rationalization, not verification. Without an enforced cycle, code is untestable by design and refactors break silently. TDD forces the interface to be designed from the consumer's perspective before any implementation exists.

**Ефективно для:** інженера/агента, який імплементує bugfix або pure-logic feature — закриває петлю між специфікацією і кодом через failing test as the spec.

## Applies If (ALL must hold)

- Bug-fix workflow: reproduce the bug as a failing test before touching production code.
- Pure-function or business-logic implementation where requirements are precise (validators, calculators, parsers).
- Refactoring with safety net: regression tests first, then change internals.
- Defining a new public API where the interface should be designed from consumer perspective.

## Skip If (ANY kills it)

- Exploratory spike — discard code afterwards.
- UI work where the assertion is visual (use Storybook + Chromatic).
- Infrastructure / config work where tests cost more than they protect.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Working test runner | config | pytest/jest/vitest/go test |
| Spec / acceptance criteria | text | ticket |
| Empty source file or hook point | code | src/ |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/unit-testing` | AAA pattern this cycle produces. |
| `free/dev/software-developer/testing` | Choice of test runner. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: red first, minimal green, refactor green-to-green, one assertion per RED, never skip RED. | ~800 |
| `content/02-output-contract.xml` | essential | Output: commit graph showing red → green → refactor commits. Forbidden: green-then-test, retroactive RED, RED with multiple assertions. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: tests-after, multi-assertion red, skip refactor, refactor while red. | ~700 |
| `content/04-procedure.xml` | medium | Steps: write failing test → confirm RED → minimal code → confirm GREEN → refactor → confirm STILL GREEN. | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: is requirement precise? → TDD. Spike? → no TDD. UI? → visual regression instead. Else: TDD. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-failing-test` | sonnet | Translate spec to a single failing assertion. |
| `implement-minimal` | haiku | Smallest code to pass. |
| `refactor` | opus | Structural improvement with judgement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tdd-cycle.md` | Step list: spec → RED → GREEN → REFACTOR with commit conventions. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tdd-workflow.py` | Inspect commit history for red-green-refactor triplets; flag green-only sequences without prior RED. | Pre-commit and PR review. |

## Related

- [[unit-testing]]
- [[testing]]
- [[python-pytest-setup]]

## Decision tree

The tree at content/06-decision-tree.xml decides TDD vs no-TDD per task type (bugfix → always; spike → never; UI → visual regression instead). Walk it before starting any non-trivial coding session.
