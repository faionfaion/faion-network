---
slug: testing-django-pytest
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use pytest function-style tests with @pytest.
content_id: "5309055fa03bac76"
tags: [testing, pytest, django, python, factory-boy]
---
# Django Testing with pytest

## Summary

**One-sentence:** Use pytest function-style tests with @pytest.

**One-paragraph:** Use pytest function-style tests with @pytest.mark.django_db for Django services. Anchor tests to factory_boy factories for object graphs, parametrize to remove duplication, and feed failures back immediately with pytest -x before moving on.

## Applies If (ALL must hold)

- Bootstrapping a test suite for a new Django service — use this reference as the style anchor.
- Filling coverage holes on an existing module — feed source + this reference and ask for unit/integration tests in the project idiom.
- Producing first-cut tests during SDD in-progress/ so review focuses on logic, not boilerplate.
- Standardising test style across a Django monorepo where engineers reinvent layouts per app.

## Skip If (ANY kills it)

- Performance / load testing — see perf-test-basics, perf-test-tools.
- Browser E2E — see playwright-automation / puppeteer-automation.
- Specifying what to test (acceptance criteria) — that belongs in test-plan.md of an SDD feature.
- When the project already has a strong test convention with custom factories — agent will drift into the generic style here and create churn.
- Non-Django Python projects — the @pytest.mark.django_db marker and DRF fixtures are irrelevant; use plain pytest patterns instead.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/automation-tooling/`
