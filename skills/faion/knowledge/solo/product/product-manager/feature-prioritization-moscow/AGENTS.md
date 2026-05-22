---
slug: feature-prioritization-moscow
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: MoSCoW categorizes requirements into Must Have, Should Have, Could Have, and Won't Have buckets for a fixed-timebox release.
content_id: "484836f43150b5a4"
tags: [prioritization, moscow, scoping, requirements, timebox]
---
# Feature Prioritization (MoSCoW)

## Summary

**One-sentence:** MoSCoW categorizes requirements into Must Have, Should Have, Could Have, and Won't Have buckets for a fixed-timebox release.

**One-paragraph:** MoSCoW categorizes requirements into Must Have, Should Have, Could Have, and Won't Have buckets for a fixed-timebox release. The core rule: every Must Have must pass the fail-test — "if we don't have this, does the product work?" — and Must + Should must not exceed 80% of capacity.

## Applies If (ALL must hold)

- Fixed-timebox release (sprint, milestone, MVP, contractual deadline) where capacity is the constraint
- Stakeholder workshop where the goal is shared vocabulary, not numerical optimization
- Scoping a vendor or contractor engagement: M/S/C/W maps cleanly to contract obligations
- Compliance and legal-driven work where "Must" carries a non-negotiable definition

## Skip If (ANY kills it)

- Cross-feature ROI comparison — MoSCoW does not encode effort or impact magnitude; use RICE
- Long-horizon roadmaps (greater than 1 quarter) — categories drift; rerun MoSCoW per release
- Many candidates (greater than 30 items) — categories collapse into "Must" by stakeholder pressure; use a numeric framework
- Strategic bets — MoSCoW cannot capture "this is a moat play, not viability"

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
