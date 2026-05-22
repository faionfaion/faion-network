---
slug: backlog-management
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Maintain a prioritized, healthy list of work connected to product goals using the DEEP principle (Detailed at top, Emergent at bottom, Estimated, Prioritized) and four buckets: Ready, Upcoming, Backlog, Icebox.
content_id: "501ac9dc9ceae54b"
tags: [backlog, product-management, grooming, prioritization, deep-invest]
---
# Backlog Management

## Summary

**One-sentence:** Maintain a prioritized, healthy list of work connected to product goals using the DEEP principle (Detailed at top, Emergent at bottom, Estimated, Prioritized) and four buckets: Ready, Upcoming, Backlog, Icebox.

**One-paragraph:** Maintain a prioritized, healthy list of work connected to product goals using the DEEP principle (Detailed at top, Emergent at bottom, Estimated, Prioritized) and four buckets: Ready, Upcoming, Backlog, Icebox. Every item must have a type tag (feature/bug/tech_debt/research), a user story in As-a/I-want/So-that format, and Given/When/Then acceptance criteria before it can enter the Ready bucket. Run weekly grooming; archive items with 180+ days of inactivity.

## Applies If (ALL must hold)

- Backlog has crossed ~80 items and signal is degrading; weekly grooming has lapsed.
- Multiple input streams (support, sales, eng, ideas) need triaging into a single ranked list.
- Refining the top of backlog into Ready items before sprint planning.
- Auditing backlog health (DEEP/INVEST compliance) before a quarterly review.

## Skip If (ANY kills it)

- Pre-PMF prototype phase with fewer than 20 items — a simple Trello/Notion list is sufficient.
- One-off project with fixed scope and end date — use a WBS or kanban board instead.
- When the team will not run weekly grooming; an unmaintained managed backlog is a longer dumping ground.
- Replacing prioritization frameworks — backlog management organizes items; RICE/MoSCoW prioritizes them. Run prioritization first.

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

- parent skill: `solo/product/product-manager/`
