---
slug: feedback-management
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pipeline to turn scattered feedback into product decisions with fixed taxonomy, weighted by segment ARR and retention risk.
content_id: "3dd1a9ef38c7b0c4"
tags: [feedback-management, user-feedback, product-research, feedback-triage, customer-input]
---
# Feedback Management

## Summary

**One-sentence:** Pipeline to turn scattered feedback into product decisions with fixed taxonomy, weighted by segment ARR and retention risk.

**One-paragraph:** Pipeline to turn scattered feedback into product decisions with fixed taxonomy, weighted by segment ARR and retention risk.

## Applies If (ALL must hold)

- Inbound feedback volume exceeds human triage capacity (greater than 20 items/day across channels).
- Multiple disconnected sources (support tickets, app store, in-app widget, social, sales) need a single canonical store.
- Recurring monthly review cycle must surface patterns, rank by segment and revenue, and link to backlog items.
- Close-loop emails to specific requesters are repetitive but high-leverage.
- Pre-roadmap sessions where PM needs "top 10 themes from last 90 days with verbatim citations."

## Skip If (ANY kills it)

- Pre-PMF with less than 5 feedback items/week — direct human reading is faster and richer.
- High-stakes strategic decisions (pivot, kill) where verbatim nuance matters more than count.
- Compliance-bound feedback (HIPAA, GDPR DSAR text) where LLM ingestion needs DPA review first.
- Sentiment-only loops with no commitment to act — automation amplifies noise without closing the loop.
- Single-channel products where the channel tool's native AI (Intercom Fin, Zendesk QA) already handles categorization.

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
