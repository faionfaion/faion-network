---
slug: feedback-management
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Systematic pipeline for collecting feedback from multiple channels, categorizing it against a locked taxonomy, aggregating patterns by topic and segment, linking top clusters to backlog items, and closing the loop with users when their requests ship.
content_id: "3dd1a9ef38c7b0c4"
tags: [feedback, customer-research, triage, product-signals]
---
# Feedback Management

## Summary

**One-sentence:** Systematic pipeline for collecting feedback from multiple channels, categorizing it against a locked taxonomy, aggregating patterns by topic and segment, linking top clusters to backlog items, and closing the loop with users when their requests ship.

**One-paragraph:** Systematic pipeline for collecting feedback from multiple channels, categorizing it against a locked taxonomy, aggregating patterns by topic and segment, linking top clusters to backlog items, and closing the loop with users when their requests ship. The pipeline runs: Collect → Categorize → Analyze → Prioritize → Act → Close Loop. Taxonomy is code-versioned; changes require a migration and re-tag run.

## Applies If (ALL must hold)

- Feedback arriving from 3+ channels and a human can no longer triage in real time.
- You want a daily/weekly digest of categorized, deduplicated, prioritized requests linked to backlog items.
- Automated close-the-loop emails needed when a requested feature ships.
- Sentiment tracking against a release or pricing change is required.

## Skip If (ANY kills it)

- Fewer than 20 feedback items per week — manual handling beats pipeline overhead.
- High-stakes B2B accounts where every quote requires named-customer context — keep human in the loop end-to-end.
- Regulated industries (medical, finance) where verbatim handling has compliance constraints — PII redaction first.

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

- parent skill: `solo/product/product-operations/`
