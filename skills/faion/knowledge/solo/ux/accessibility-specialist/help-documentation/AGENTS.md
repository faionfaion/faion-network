---
slug: help-documentation
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Nielsen Heuristic #10 applied: provide help that is task-focused, searchable, and reachable from the failing context — measured by deflection rate (questions resolved without contacting support) and time-to-answer.
content_id: "b671f2e6b5bbc8a0"
complexity: medium
produces: rubric
est_tokens: 3500
tags: [help-systems, documentation, ux, support, content]
---
# Help and Documentation

## Summary

**One-sentence:** Nielsen Heuristic #10 applied: provide help that is task-focused, searchable, and reachable from the failing context — measured by deflection rate (questions resolved without contacting support) and time-to-answer.

**One-paragraph:** Nielsen Heuristic #10 applied: provide help that is task-focused, searchable, and reachable from the failing context — measured by deflection rate (questions resolved without contacting support) and time-to-answer. The methodology pins the artefact: a help-coverage rubric scoring the product on task-page presence, in-context entry points, search quality, and freshness; remediation list per gap.

**Ефективно для:**

- SaaS products generating recurring support tickets.
- Reviewers measuring whether docs actually deflect support load.
- Onboarding flows where novices need contextual help.
- Audit surface: deflection rate + time-to-answer are measurable.

## Applies If (ALL must hold)

- Product surfaces tasks complex enough to need explanation.
- Support load is measurable.
- There is a docs / help surface to evaluate.

## Skip If (ANY kills it)

- Trivial single-screen product.
- No support load — users discover everything organically.
- No measurement surface for deflection.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Help surface | URL | Docs site |
| Support tickets sample | csv | Helpdesk |
| Task inventory | list | Product |

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
| `draft-help-documentation` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-help-documentation` | haiku | Schema check + threshold checks; deterministic. |
| `review-help-documentation` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/help-documentation.json` | JSON skeleton conforming to the output contract schema. |
| `templates/help-documentation.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-help-documentation.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[match-real-world]]
- [[recognition-over-recall]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
