---
slug: backlog-management
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for maintaining a prioritized, healthy backlog that connects work items to product goals.
content_id: "501ac9dc9ceae54b"
tags: [backlog, prioritization, grooming, deep, invest]
---
# Backlog Management

## Summary

**One-sentence:** Methodology for maintaining a prioritized, healthy backlog that connects work items to product goals.

**One-paragraph:** Methodology for maintaining a prioritized, healthy backlog that connects work items to product goals. Applies the DEEP principle (Detailed-top, Emergent-bottom, Estimated, Prioritized) and INVEST criteria for story quality. Weekly grooming, regular cleanup, and a clear "ready" definition prevent backlogs from becoming unactionable dumping grounds.

## Applies If (ALL must hold)

- Backlog has more than 100 items and "next sprint" is unclear or untrusted.
- Pre-grooming session: classify new items, flag stale ones for archive.
- After SDD spec/design lands: decompose into INVEST stories with acceptance criteria.
- Cross-project rollup: same person owns 5+ backlogs across Linear/Jira/GitHub Projects.
- Migrating between trackers (Trello to Linear, GitHub Issues to Jira).

## Skip If (ANY kills it)

- Solo founder with fewer than 30 items — a Markdown file beats agent automation.
- Backlog is a wishlist with no commitment system — fix process before adding agents.
- Compliance-bound product (medical, aviation) where every state change needs human signoff and audit trail.

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
