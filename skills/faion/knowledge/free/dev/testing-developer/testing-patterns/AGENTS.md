---
slug: testing-patterns
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Produces a language-agnostic test-strategy rubric: AAA / Given-When-Then structure, Builder / Object Mother data, Test Pyramid layering, Page Object Model UI selection."
content_id: "eecdde02f42a7f18"
complexity: medium
produces: rubric
est_tokens: 4500
tags: [testing, patterns, aaa, given-when-then, test-pyramid, page-object-model, test-doubles]
---

# Testing Patterns (Cross-Language)

## Summary

**One-sentence:** Produces a language-agnostic test-strategy rubric: AAA / Given-When-Then structure, Builder / Object Mother data, Test Pyramid layering, Page Object Model UI selection.

**One-paragraph:** Proven structural and data patterns for writing maintainable, reliable tests — applicable across Python, TypeScript, and Go. Covers test structure (AAA / GWT), data creation (Builder / Object Mother), test doubles, architecture strategy (pyramid), UI patterns (POM), isolation, and property-based testing. Tests without a consistent structure are hard to debug, slow down CI when the wrong layer is over-tested, and drift toward false positives.

**Ефективно для:** establishing a test strategy for a new codebase, reviewing an existing test suite for systemic issues, onboarding a new engineer to a team's test conventions, deciding whether a new behavior belongs at unit / integration / E2E layer.

## Applies If (ALL must hold)

- Establishing or reviewing a test strategy for a new project
- A code review where reviewer must judge if the right layer is being tested
- Diagnosing a slow or flaky suite where the pyramid looks inverted
- Picking between Builder, Object Mother, and inline fixtures for test data

## Skip If (ANY kills it)

- Language-specific runner setup — use `[[testing-pytest]]`, `[[testing-javascript]]`, `[[testing-go]]`
- E2E browser automation — use `[[e2e-testing]]`
- Mocking technique selection — use `[[mocking-strategies]]`

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Existing test suite OR product spec | Code repo OR spec doc | team backlog |
| Language-runner choice | decision | previously resolved |
| CI feedback time target | number (minutes) | engineering policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[unit-testing]]` | FIRST principles inform pattern application |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale and source | ~900 |
| `content/02-output-contract.xml` | essential | JSON-schema output shape + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Audit existing suite by layer | sonnet | Counting and pattern-matching. |
| Author strategy rubric | sonnet | Compositional from template + decisions. |
| Diagnose flake root cause | opus | Cross-cuts ordering, state, async, env. |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy.md.tmpl` | 1-page test strategy rubric: pyramid + data + UI + isolation. |
| `templates/builder.py.tmpl` | Builder pattern skeleton for Python test data. |
| `templates/builder.ts.tmpl` | Builder pattern skeleton for TypeScript test data. |
| `templates/pr-checklist.md.tmpl` | Code-review checklist mapping rubric to PR review. |
| `templates/_smoke-test.md` | Minimal filled rubric example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-patterns.py` | Validates an output document against the 02-output-contract schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `free/dev/testing-developer/`
- `[[unit-testing]]`
- `[[testing-pytest]]`
- `[[testing-javascript]]`
- `[[testing-go]]`
- `[[mocking-strategies]]`
- `[[e2e-testing]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether testing-patterns applies: root question — "Does this codebase have a written test strategy?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip:` conclusion when it does not.
