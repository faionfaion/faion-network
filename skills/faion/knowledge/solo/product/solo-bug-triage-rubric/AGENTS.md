---
slug: solo-bug-triage-rubric
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 5-question rubric mapping a bug to one of three queues (drop-everything / next-sprint / accept) within 5 minutes; named owner, retest threshold, and a decay rule for accepted bugs.
content_id: "01ab9ca12583631f"
complexity: light
produces: rubric
est_tokens: 2900
tags: [bug-triage, solo, rubric, support-ops]
---
# Solo Bug Triage Rubric

## Summary

**One-sentence:** 5-question rubric mapping a bug to one of three queues (drop-everything / next-sprint / accept) within 5 minutes; named owner, retest threshold, and a decay rule for accepted bugs.

**One-paragraph:** 5-question rubric mapping a bug to one of three queues (drop-everything / next-sprint / accept) within 5 minutes; named owner, retest threshold, and a decay rule for accepted bugs. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Solo Bug Triage Rubric on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS handles ≥3 bug reports per week.
- No team to delegate to — owner triages everything.
- Bugs come from ≥2 channels (email, Discord, in-app).
- Owner wants a defensible kill / accept policy under stakeholder pressure.

## Skip If (ANY kills it)

- Incident-grade outage — incident response runs the show.
- Single-user enterprise contract with SLA — use SLA matrix.
- Pre-launch with no users — bugs are dev tasks.
- Team of ≥3 — formal bug-triage process applies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inbound bug channels mapped | table | Support |
| Owner with triage authority | @handle | Self |
| Severity / scope dimensions | matrix | Internal |
| Test environment for retest | staging URL | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/code-quality/bug-reporting` | Provides the bug report intake shape. |

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
| `draft-solo-bug-triage-rubric` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-solo-bug-triage-rubric` | haiku | Schema check + threshold checks; deterministic. |
| `review-solo-bug-triage-rubric` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-bug-triage-rubric.json` | JSON skeleton conforming to the output contract schema. |
| `templates/solo-bug-triage-rubric.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-bug-triage-rubric.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[solo-go-no-go-criteria]]
- [[support-tool-pm-triage-spec]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
