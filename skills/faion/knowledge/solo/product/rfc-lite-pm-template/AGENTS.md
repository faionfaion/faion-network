---
slug: rfc-lite-pm-template
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Opinionated short RFC-lite template (problem → evidence → scope → open questions) that engineering will actually read; produces a versioned, owner-signed feature brief with evidence anchors and an outcome-review date.
content_id: "aa882584982cf9df"
complexity: light
produces: spec
est_tokens: 3500
tags: [product, rfc, template, spec-writing]
---
# Rfc Lite Pm Template

## Summary

**One-sentence:** Opinionated short RFC-lite template (problem → evidence → scope → open questions) that engineering will actually read; produces a versioned, owner-signed feature brief with evidence anchors and an outcome-review date.

**One-paragraph:** Opinionated short RFC-lite template (problem → evidence → scope → open questions) that engineering will actually read; produces a versioned, owner-signed feature brief with evidence anchors and an outcome-review date. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Rfc Lite Pm Template on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- PM writes ≥1 feature brief per week and the corpus has none today.
- Engineering has refused to read previous specs (too long / vague).
- Specs are not tied to outcome IDs and become orphaned.
- Owner has authority to enforce a template and review cadence.

## Skip If (ANY kills it)

- RFCs need full ADR depth (security, architecture) — use ADR template.
- Pre-discovery work — no problem statement yet.
- Single-line backlog ticket — RFC-lite is overkill.
- Team already has a working spec template they enforce.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature problem statement | 1-2 sentences | Discovery |
| Evidence anchors | transcripts / metrics / tickets | Inbox / Linear |
| Outcome ID this serves | OKR / outcome doc reference | Roadmap |
| Named owner + reviewer | @handle pair | Team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/spec-writing` | Generic spec craft; this pins the lite shape. |
| `solo/product/product-planning/outcome-based-roadmaps` | Source of outcome IDs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-rfc-lite-pm-template` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-rfc-lite-pm-template` | haiku | Schema check + threshold checks; deterministic. |
| `review-rfc-lite-pm-template` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rfc-lite-pm-template.json` | JSON skeleton conforming to the output contract schema. |
| `templates/rfc-lite-pm-template.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rfc-lite-pm-template.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-writing]]
- [[outcome-based-roadmaps]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
