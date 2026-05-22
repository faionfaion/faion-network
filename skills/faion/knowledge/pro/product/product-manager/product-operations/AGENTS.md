---
slug: product-operations
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When a Product Ops function exists, the PM is a consumer and partner — not its operator.
content_id: "da83746a670250be"
tags: [product-operations, product-manager, raci, governance, hand-off]
---
# Product Operations (PM-side)

## Summary

**One-sentence:** When a Product Ops function exists, the PM is a consumer and partner — not its operator.

**One-paragraph:** When a Product Ops function exists, the PM is a consumer and partner — not its operator. PM-side agents are pure readers of the canonical store (Linear/Jira/Productboard rollups) and authors of narrative artifacts (specs, decision memos, discovery memos). Hand-offs are explicit: PM drafts land in a Product Ops queue (PR, Slack thread, Notion draft) where the Product Ops agent applies the write. The PM never bypasses that queue.

## Applies If (ALL must hold)

- PM onboarding into an org with an existing Product Ops function — needs explicit RACI between own subagents and Product Ops automations.
- Multiple PMs requesting inconsistent artifacts — route through the Product Ops canonical store.
- Preparing a board/exec/portfolio review — consume Product Ops outputs instead of re-deriving.
- PM proposes a new ceremony or template — hand off the converged output to Product Ops to ship org-wide.
- PM receives a Product Ops insight and needs to convert it into a discovery or kill decision.

## Skip If (ANY kills it)

- Solopreneur / single-PM team with no Product Ops function — use solo-tier skills directly.
- Product Ops charter is undefined — drive brainstorm on the charter first.
- Strategic decisions (pricing, positioning, kill/scale, hiring) — the PM owns these, not Product Ops.
- Customer-facing comms (release notes, interviews, positioning copy) — PM owns the content.
- First 30 days of a new product where the workflow is unstable.

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

- parent skill: `pro/product/product-manager/`
