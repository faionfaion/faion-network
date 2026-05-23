---
slug: backlog-management
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Maintain a single-source backlog with weekly grooming, age caps per state, and a refusal-to-publish guardrail when the backlog exceeds the team's capacity by ≥3×.
content_id: "d35dc1c0a5f22bee"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["backlog", "grooming", "prioritisation", "wishlist-prevention", "ops"]
---
# Backlog Management

## Summary

**One-sentence:** Maintain a single-source backlog with weekly grooming, age caps per state, and a refusal-to-publish guardrail when the backlog exceeds the team's capacity by ≥3×.

**One-paragraph:** A managed backlog has ≤3 states (Now/Next/Icebox), age caps per state, and a weekly grooming ritual that closes/merges drift. The capacity ratio (backlog items ÷ weekly throughput) is the health signal: above 3× it stops being a plan and becomes a wishlist.

**Ефективно для:**

- Solo founder watching a 200-item backlog grow weekly without ever shipping anything — needs a forcing function to keep the backlog meaningful instead of cathartic.

## Applies If (ALL must hold)

- Backlog exists and is consulted ≥weekly.
- Team throughput is measurable (items/week).
- Backlog has ≥10 items in some kind of order.

## Skip If (ANY kills it)

- Pre-product phase; no backlog yet.
- Team uses kanban with WIP=1 and no backlog visible.
- Single-developer fire-and-forget mode (use a plain task list).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backlog source-of-truth URL | url | Linear / GitHub / Notion |
| Weekly throughput estimate | integer | Historical data |
| Capacity ratio policy | table | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/feature-prioritization-rice` | Within-state ranking when items contend. |
| `solo/product/product-manager/roadmap-design` | Backlog feeds horizons of the roadmap. |

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
| `draft-backlog-management` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-backlog-management` | haiku | Schema check + threshold checks; deterministic. |
| `review-backlog-management` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-management.json` | JSON skeleton conforming to the output contract schema. |
| `templates/backlog-management.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backlog-management.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[feature-prioritization-rice]]
- [[roadmap-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
