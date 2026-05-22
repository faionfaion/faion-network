---
slug: qa-test-pyramid-vs-trophy-decision
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0f5719c77bf3f96f"
summary: A decision framework for choosing test pyramid vs Kent C. Dodds testing trophy per module — based on stack, change frequency, integration risk, and runtime cost — so the team stops the "too many e2e and too slow CI" failure mode without overcorrecting.
tags: [test-pyramid, testing-trophy, test-strategy, integration-tests, decision-framework]
---

# Test Pyramid vs Testing Trophy: Per-Module Decision

## Summary

**One-sentence:** Decide per module whether the test pyramid (unit-heavy) or the testing trophy (integration-heavy) is the right shape, using a 5-question diagnostic on stack, change frequency, integration risk, runtime cost, and AC-shape.

**One-paragraph:** Faion's testing methodologies do not give the user a model for choosing between unit-heavy (pyramid) and integration-heavy (trophy). The default failure mode is opposite per stack: backend teams over-invest in unit tests with heavy mocking that prove nothing; frontend teams over-invest in e2e tests that are slow and flaky. The decision is not global — different modules in the same repo justify different shapes. This methodology pins a 5-question diagnostic: (1) is the module mostly orchestration or mostly pure logic? (2) how often does the module change? (3) does integration with external services dominate the risk? (4) what is the existing unit-test runtime budget? (5) do ACs describe behavior at the unit level or at the workflow level? Answers map to one of: pyramid-heavy, trophy-heavy, or hybrid. Primary output: a per-module decision recorded in `test-strategy.yaml`, refreshed quarterly.

## Applies If (ALL must hold)

- repo has at least 5 distinct modules with non-trivial test investment
- team has experienced one of: e2e too slow, integration gap not caught by units, unit-test-only suite that misses bugs caught by humans
- team has authority to adopt different test-shape per module (no organisation-wide mandate forcing one shape)
- at least one engineer can spend 1-2 hours on the per-module decision

## Skip If (ANY kills it)

- team works on a single mostly-pure-logic library — pyramid is the obvious answer
- team works on a single end-to-end SaaS UI with no internal modules — trophy is the obvious answer
- compliance environment with mandated test-shape — apply the mandate, this decision does not apply
- pre-MVP — test shape is over-engineering before the architecture stabilises

## Prerequisites

- a list of modules at the same granularity used by the risk matrix
- recent CI runtime breakdown per test type
- recent incident data: which incidents were "unit tests passed but feature broken"

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-risk-matrix-method` | Risk matrix produces the module list and impact scores |
| `pro/dev/code-quality/mutation-testing-ci-gate` | Mutation testing reveals whether unit suite is shallow |
| `solo/dev/testing-developer/qa-changed-lines-coverage-dashboard` | Coverage data feeds the decision |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules built around the diagnostic; pyramid / trophy / hybrid mappings | ~900 |
| `content/02-output-contract.xml` | essential | test-strategy.yaml schema with per-module decisions | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: org-wide-mandate, never-revisit, unit-test-snobbery, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diagnostic_per_module` | sonnet | Cross-input judgment from 5 questions |
| `summarise_existing_test_distribution_per_module` | haiku | Mechanical analysis of test files per module |
| `propose_re_balancing_plan` | opus | Cross-module synthesis: how to migrate without breaking CI |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-strategy.yaml` | Per-module record with the 5 answers + decision + chosen shape |
| `templates/diagnostic-form.md` | The 5-question diagnostic for human use |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/analyse-current-shape.py` | Counts unit / integration / e2e tests per module, computes current shape | Pre-quarterly review |
| `scripts/runtime-breakdown.py` | Pulls CI runtime per test type per module | Pre-quarterly review |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-risk-matrix-method`, `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist`
- external: [Mike Cohn, Succeeding with Agile (Addison-Wesley, 2009) — original pyramid] · [Kent C. Dodds "The Testing Trophy" 2018] · [Martin Fowler, TestPyramid (2012) bliki] · [Test-shape research in Google Testing Blog]
