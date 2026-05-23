---
slug: help-documentation
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design contextual, searchable, task-oriented help — tooltips, inline guides, knowledge base — so users solve their own problems without leaving the flow.
content_id: "b671f2e6b5bbc8a0"
complexity: medium
produces: spec
est_tokens: 3600
tags: ["heuristic", "documentation", "help", "self-service", "nielsen"]
---
# Help and Documentation

## Summary

**One-sentence:** Design contextual, searchable, task-oriented help — tooltips, inline guides, knowledge base — so users solve their own problems without leaving the flow.

**One-paragraph:** Design contextual, searchable, task-oriented help — tooltips, inline guides, knowledge base — so users solve their own problems without leaving the flow.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Support volume is high on questions answerable by self-service.
- Users abandon flows at the same step and never reach support.
- Documentation exists but is not surfaced in context.
- Content team can write task-oriented help (not feature lists).
- Engineering can add in-app help surfaces (tooltip, drawer, link).

## Skip If (ANY kills it)

- Product is so simple that no help is required — invest in the UI instead.
- Documentation is owned by a separate team that will not collaborate.
- Audience is internal experts who consult external runbooks.
- Compliance forbids inline guidance (e.g., regulated finance script).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Support-ticket top-50 by volume | csv | Support tool |
| Inventory of existing help content | csv | Knowledge base |
| In-app help component catalogue | storybook | Design system |
| Editorial style guide | markdown | Content team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/error-recovery` | Error messages link into the same help system. |
| `solo/ux/ux-ui-designer/consistency-standards` | Help patterns must align with the system. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

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

- [[error-recovery]]
- [[consistency-standards]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
