---
slug: verbatim-to-backlog-pattern
tier: solo
group: product
domain: pm
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Four-step transform (extract → cluster → frame → prioritise) bridging Mom-Test verbatim customer quotes to RICE-scored Job-Story backlog cards with verbatim attached to every card.
content_id: "5f41f355a092bf27"
complexity: medium
produces: spec
est_tokens: 4200
tags: [continuous-discovery, mom-test, backlog, prioritisation, solo-saas]
---
# Verbatim To Backlog Pattern

## Summary

**One-sentence:** Four-step transform (extract → cluster → frame → prioritise) bridging Mom-Test verbatim customer quotes to RICE-scored Job-Story backlog cards with verbatim attached to every card.

**One-paragraph:** Four-step transform (extract → cluster → frame → prioritise) bridging Mom-Test verbatim customer quotes to RICE-scored Job-Story backlog cards with verbatim attached to every card. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Verbatim To Backlog Pattern on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS post-launch with ≥5 paying / active users.
- ≥20 customer touchpoints (interviews, support tickets, Discord) in trailing 60 days.
- Backlog tool with custom-field support (Linear / GitHub Projects / Notion).
- Operator wants prioritisation defensible by quote evidence.

## Skip If (ANY kills it)

- Pre-launch — no real customer voice; use problem-validation.
- Internal tool with no external users — backlog driven by stakeholders.
- Single-customer wedge B2B engagement — N=1 doesn't cluster.
- Operator has >200 cards in backlog — clean backlog first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Touchpoint corpus | transcripts / tickets / DMs | Inbox / Discord / Intercom |
| Backlog tool with quote field | config | Linear / Notion |
| Embedding model access | API key | OpenAI / Voyage / Anthropic |
| ≥30d historical touchpoints | archive | Inbox |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/continuous-discovery` | Provides the touchpoint stream this consumes. |
| `pro/product/product-manager/backlog-management` | Destination format. |

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
| `draft-verbatim-to-backlog-pattern` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-verbatim-to-backlog-pattern` | haiku | Schema check + threshold checks; deterministic. |
| `review-verbatim-to-backlog-pattern` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verbatim-to-backlog-pattern.json` | JSON skeleton conforming to the output contract schema. |
| `templates/verbatim-to-backlog-pattern.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-verbatim-to-backlog-pattern.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[continuous-discovery]]
- [[backlog-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
