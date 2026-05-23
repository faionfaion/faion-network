---
slug: coverage-rebuild-playbook
tier: solo
group: testing
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six-week coverage rebuild playbook that lifts a legacy codebase from 30% to 70% test coverage by ranking files by risk × churn, writing characterization tests for the top risk band first, and gating future commits behind a ratcheted coverage floor.
content_id: "940c9a02ce3660b6"
complexity: deep
produces: playbook-step
est_tokens: 4200
tags: [coverage-rebuild, testing, tdd, regression, solo]
---
# Coverage Rebuild Playbook

## Summary

**One-sentence:** Six-week coverage rebuild playbook that lifts a legacy codebase from 30% to 70% test coverage by ranking files by risk × churn, writing characterization tests for the top risk band first, and gating future commits behind a ratcheted coverage floor.

**One-paragraph:** Six-week coverage rebuild playbook that lifts a legacy codebase from 30% to 70% test coverage by ranking files by risk × churn, writing characterization tests for the top risk band first, and gating future commits behind a ratcheted coverage floor. The methodology pins the artefact: a weekly milestone schedule, a risk-ranked file list, characterization test stubs, and a CI ratchet that prevents regression.

**Ефективно для:**

- Legacy codebases under refactor pressure that cannot land changes safely.
- Solo founders inheriting an untested codebase.
- Pipelines that need a coverage floor before continuous delivery.
- Audit surface: weekly milestones with measurable coverage delta.

## Applies If (ALL must hold)

- Current coverage is below the target floor (default 70%).
- Codebase compiles / runs (tests can attach to it).
- There is a working CI that can enforce a coverage floor.

## Skip If (ANY kills it)

- Greenfield project — write tests as you go, not via rebuild.
- Codebase about to be deprecated — rebuild ROI negative.
- No CI — coverage floor cannot be enforced.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current coverage report | lcov / json | Test runner |
| Git churn data | log | git log |
| Risk classification | spreadsheet | Operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | This methodology has no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-coverage-rebuild-playbook` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-coverage-rebuild-playbook` | haiku | Schema check + threshold checks; deterministic. |
| `review-coverage-rebuild-playbook` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage-rebuild-playbook.json` | JSON skeleton conforming to the output contract schema. |
| `templates/coverage-rebuild-playbook.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-coverage-rebuild-playbook.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[quality-gates-confidence]]
- [[ai-coding-agent-handoff-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
