---
slug: product-explainability
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: PM-specific lens: this methodology is a communication discipline, not a marketing artifact.
content_id: "821658e3a1f4baf5"
tags: [product-explainability, feature-narrative, stakeholder-communication, story-extraction, audience-render]
---
# Product Explainability (PM Angle)

## Summary

**One-sentence:** PM-specific lens: this methodology is a communication discipline, not a marketing artifact.

**One-paragraph:** PM-specific lens: this methodology is a communication discipline, not a marketing artifact. The PM owns the bridge between what engineering shipped and how non-technical stakeholders understand it. Explainability fails when the PM lets feature lists, demo videos, and release notes substitute for an articulated, repeatable story of purpose → behavior → limit → impact.

## Applies If (ALL must hold)

- Pre-roadmap-review: an exec asks "what does this product actually do?" and three PMs answer with three different framings — you need a single canonical explanation.
- Pre-launch story prep: enabling sales, support, customer success, and partner teams who must explain the feature without watching a Loom.
- Board / investor / all-hands narrative: distilling six months of work into a 90-second answer to "what shipped, what changed for users, what's next".
- Cross-team feature-to-impact mapping: every release should answer "which OKR / customer outcome moved, by how much, because of which capability".
- Post-mortem on miscommunication: customer expected X, got Y, churned — gap is in the story, not the product.
- Onboarding a new PM, designer, or engineer: the explainability artifact is the fastest path to shared mental model.
- Quarterly product review: forcing yourself to re-articulate purpose surfaces drift you cannot see day-to-day.

## Skip If (ANY kills it)

- Inside the engineering loop: explainability framing slows iteration on technical specs; use ADRs and design docs there.
- For experiment-stage features behind a flag with less than 5% rollout — premature explainability hardens hypotheses you should still be testing.
- When the org already has rigorous PMM (product marketing) ownership and the PM is duplicating that artifact — collaborate, do not re-author.
- For deeply technical APIs whose only audience is engineers with the OpenAPI spec; story prose adds noise.
- Weekly tactical standups — it is a strategy and stakeholder artifact, not a status update.

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
