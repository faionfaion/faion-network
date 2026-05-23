---
slug: solo-go-no-go-criteria
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pre-ship go / hold / no-op gate with five concrete questions (build-quality, scope-vs-promise, comms-ready, rollback-tested, success-metric-instrumented) — produces a signed go/no-go record before any release.
content_id: "8db522ea00795e0e"
complexity: light
produces: checklist
est_tokens: 2900
tags: [release, go-no-go, solo, pre-ship-gate]
---
# Solo Go No Go Criteria

## Summary

**One-sentence:** Pre-ship go / hold / no-op gate with five concrete questions (build-quality, scope-vs-promise, comms-ready, rollback-tested, success-metric-instrumented) — produces a signed go/no-go record before any release.

**One-paragraph:** Pre-ship go / hold / no-op gate with five concrete questions (build-quality, scope-vs-promise, comms-ready, rollback-tested, success-metric-instrumented) — produces a signed go/no-go record before any release. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Solo Go No Go Criteria on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS ships ≥1 release per month.
- Releases touch user-visible surface area.
- Owner is sole signer (no committee).
- Owner wants a kill switch the day-of.

## Skip If (ANY kills it)

- Hotfix during incident — incident runs the gate.
- Pre-launch iteration where every commit ships.
- Silent infra deploy behind a flag.
- Team of ≥3 with a release manager — formal RFC applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release scope frozen | ticket list | Backlog |
| Readiness checklist completed | doc | QA |
| Rollback runbook tested | log | Engineering |
| Instrumentation green | dashboard URL | BI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/release-planning` | Parent release plan. |
| `solo/dev/code-quality/pre-merge-checks` | Build quality upstream. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-solo-go-no-go-criteria` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-solo-go-no-go-criteria` | haiku | Schema check + threshold checks; deterministic. |
| `review-solo-go-no-go-criteria` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-go-no-go-criteria.json` | JSON skeleton conforming to the output contract schema. |
| `templates/solo-go-no-go-criteria.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-go-no-go-criteria.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[release-planning]]
- [[solo-bug-triage-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
