---
slug: trade-off-build-vs-buy
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Evaluate whether to build a capability in-house, buy a vendor solution, or adopt a hybrid approach.
content_id: "fb1ee2a5f186523e"
tags: [build-vs-buy, trade-off, vendor-evaluation, tco, architecture]
---
# Build vs Buy Decision Framework

## Summary

**One-sentence:** Evaluate whether to build a capability in-house, buy a vendor solution, or adopt a hybrid approach.

**One-paragraph:** Evaluate whether to build a capability in-house, buy a vendor solution, or adopt a hybrid approach. The framework covers strategic fit (core vs context), 3-year TCO comparison, vendor evaluation, risk assessment, and exit strategy documentation. Organizations with proprietary core technology see ~2x stronger revenue growth (Deloitte 2025).

## Applies If (ALL must hold)

- Evaluating any capability that requires significant investment: authentication, billing, search, notifications, analytics, storage.
- When the team is considering a SaaS solution with multi-year subscription costs.
- When open-source alternatives exist alongside commercial options.
- Before starting a major new subsystem build — always evaluate buy first.

## Skip If (ANY kills it)

- Core competitive differentiators — the capability that makes your product unique should almost always be built, not bought.
- When the buy option has no viable exit path — vendor lock-in without a documented exit strategy is a separate risk requiring explicit acceptance.
- Commodity infrastructure already standardized in your stack (e.g., "should we use Redis or build a cache?") — existing standards override the analysis.

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

- parent skill: `solo/dev/software-architect/`
