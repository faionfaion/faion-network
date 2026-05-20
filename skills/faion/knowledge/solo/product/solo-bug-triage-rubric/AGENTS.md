---
slug: solo-bug-triage-rubric
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "01ab9ca12583631f"
summary: P0/P1/P2 + impact-reach scoring scaled for an ARR-honest solo founder — separates "fix now" from "fix never" in under 60 seconds per bug.
---
# Solo Bug Triage Rubric

## Summary

**One-sentence:** A two-axis triage rubric (severity × reach) tuned for solo founders, where every bug gets a P0/P1/P2 label, an action verdict, and a kill-or-keep call inside one minute.

**One-paragraph:** Team triage rubrics inherit from large-org severity definitions (P0 = "production-down, 50+ engineers paged"). Solo founders running on real ARR cannot afford that calibration: a P0 in their universe is "any paying customer cannot use the core flow"; many "P2"s in team-speak are kill-it items at solo scale. This methodology defines the solo rubric: a fixed severity ladder with concrete revenue and reach criteria, plus a forcing question ("is anyone affected paying?") that bypasses long debates. Anchored to "Friday bug-bash & tech-debt triage hour" — the rubric runs in the 60 minutes of triage every Friday.

## Applies If (ALL must hold)

- Solo founder with a live revenue-bearing product (≥1 paying customer).
- Bug backlog exists in a tracker (Linear, GitHub Issues, plain markdown).
- You can identify paying-customer vs free-user impact per bug (segment data accessible).
- Friday (or weekly) triage cadence is in place or will be.

## Skip If (ANY kills it)

- Pre-revenue prototype — everything is P2 by definition; use a different filter (does this block the demo?).
- Team product with on-call rotation — adopt a team-scale rubric instead.
- Operating in safety-critical domain (med, finance, life-systems) — use the regulated-domain severity ladder, not this one.

## Prerequisites

- Bug tracker with a `priority` field (or labels equivalent).
- A way to filter bug reporters by `is_paying` status (Stripe/segment join).
- A weekly triage block on the calendar.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/AGENTS.md` | Parent group context |
| `solo/product/kill-or-keep-criteria` if present | Sibling rubric for feature-scope kill calls |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules every triage pass enforces | ~900 |

## Related

- parent skill: `solo/product/`
- triggering activity: `p1-solo-saas-builder/Friday bug-bash & tech-debt triage hour`
- adjacent: `solo/product/kill-or-keep-criteria`, `solo/product/friction-to-backlog`
