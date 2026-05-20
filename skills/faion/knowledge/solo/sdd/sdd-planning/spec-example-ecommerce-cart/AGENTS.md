---
slug: spec-example-ecommerce-cart
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A fully-populated SDD spec for a shopping cart feature — covering personas, user stories, functional and non-functional requirements, Given/When/Then acceptance criteria, out-of-scope table, and a preliminary data model.
content_id: "688d626918a656b4"
tags: [spec, example, ecommerce, sdd, reference]
---
# Spec Example: E-commerce Cart

## Summary

**One-sentence:** A fully-populated SDD spec for a shopping cart feature — covering personas, user stories, functional and non-functional requirements, Given/When/Then acceptance criteria, out-of-scope table, and a preliminary data model.

**One-paragraph:** A fully-populated SDD spec for a shopping cart feature — covering personas, user stories, functional and non-functional requirements, Given/When/Then acceptance criteria, out-of-scope table, and a preliminary data model. Use as a few-shot reference when generating or reviewing specs for similar features.

## Applies If (ALL must hold)

- Agent or developer needs to see what a fully-populated spec looks like in practice.
- Calibrating spec-writing output quality — compare agent output against this example.
- Bootstrapping a new e-commerce cart-adjacent feature (persistence, guest-vs-logged-in, quantity limits, session merge patterns recur across cart-related features).
- Onboarding a new contributor to the SDD workflow.

## Skip If (ANY kills it)

- Starting a new spec by editing this file directly — use template-spec instead.
- Non-e-commerce domains: guest cart, localStorage, product-catalog dependency are domain-specific and transfer poorly without significant reframing.
- Taking NFR targets (200ms p95, 50k concurrent) as real project targets — they have no measurement source and must be replaced.

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

- parent skill: `solo/sdd/sdd-planning/`
