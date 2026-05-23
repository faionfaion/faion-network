---
slug: release-planning
tier: solo
group: product
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six-step release plan (goal → contents → readiness → communication → execution → post-release) with rollback gate, named owner per channel, and a 14-day stability check.
content_id: "68460e3733a2e87f"
complexity: medium
produces: spec
est_tokens: 4200
tags: [release-planning, release-management, rollback, communication]
---
# Release Planning

## Summary

**One-sentence:** Six-step release plan (goal → contents → readiness → communication → execution → post-release) with rollback gate, named owner per channel, and a 14-day stability check.

**One-paragraph:** Six-step release plan (goal → contents → readiness → communication → execution → post-release) with rollback gate, named owner per channel, and a 14-day stability check. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Release Planning on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Release contains ≥1 user-visible change (not a silent infra deploy).
- Release affects ≥1 stakeholder group (customers, partners, support).
- Owner has authority over ship / rollback decision.
- Instrumentation captures error rate + key business metric.

## Skip If (ANY kills it)

- Silent infra change behind a flag — use feature-flag playbook.
- Hotfix during incident — incident-response runs the show.
- Pre-PMF iteration where every commit is a 'release'.
- Single-customer custom build — handoff playbook applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release scope | ticket list | Backlog |
| Readiness checklist | test, docs, support | QA |
| Communication plan | channel + audience matrix | Marketing / support |
| Rollback runbook | steps + owner | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/product-launch` | Major releases that are also launches. |
| `pro/infra/cicd-engineer/release-engineering` | Pipeline that ships the release. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-release-planning` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-release-planning` | haiku | Schema check + threshold checks; deterministic. |
| `review-release-planning` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-planning.json` | JSON skeleton conforming to the output contract schema. |
| `templates/release-planning.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-release-planning.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[product-launch]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
