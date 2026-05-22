---
slug: continuous-discovery
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Integrate discovery as a recurring operational cadence rather than a one-time project-start activity.
content_id: "09d2bd7b60d51b4e"
tags: [discovery, product-research, opportunity-solution-tree, user-interviews, cadence]
---
# Continuous Discovery

## Summary

**One-sentence:** Integrate discovery as a recurring operational cadence rather than a one-time project-start activity.

**One-paragraph:** Integrate discovery as a recurring operational cadence rather than a one-time project-start activity. Allocate 15-20% of team capacity to discovery every sprint. Run three loops in parallel: daily behaviour-watcher (analytics diffs), weekly user-interview cycle with synthesis into a tagged research repository, and sprint-cadence opportunity-mapper updating the opportunity-solution tree. Every shipped feature must be traceable to a tagged opportunity; leakage above 30% is a signal that delivery has decoupled from discovery.

## Applies If (ALL must hold)

- Product is past initial PMF and decisions have started feeling arbitrary; recurring discovery is needed to keep direction grounded.
- A delivery team has bandwidth to allocate ~15-20% to discovery without halting feature work.
- High-velocity environment (multiple releases per week) where one-off discovery cycles cannot keep pace.
- After a major launch, to monitor activation/retention while iterating.

## Skip If (ANY kills it)

- Pre-PMF: continuous discovery dilutes effort across a wide problem space; concentrated discovery sprints work better.
- Solo founder with no recurring user pool yet — there is nothing to continuously sample.
- Frozen feature scope with imminent contractual deadline; findings cannot be acted on.
- Teams without analytics and a research repository; insights evaporate without structured storage.

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
