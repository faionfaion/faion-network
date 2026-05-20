---
slug: trunk-based-challenges
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: TBD adoption fails at three predictable points: "trunk is always broken" (insufficient gates), "we need long-lived branches" (large features with no flag infrastructure), and "code review is the bottleneck" (large PRs and few reviewers).
content_id: "091912f0d83fb182"
tags: [trunk-based-development, troubleshooting, code-review, sdd, adoption]
---
# Trunk-Based Development: Challenges and Solutions

## Summary

**One-sentence:** TBD adoption fails at three predictable points: "trunk is always broken" (insufficient gates), "we need long-lived branches" (large features with no flag infrastructure), and "code review is the bottleneck" (large PRs and few reviewers).

**One-paragraph:** TBD adoption fails at three predictable points: "trunk is always broken" (insufficient gates), "we need long-lived branches" (large features with no flag infrastructure), and "code review is the bottleneck" (large PRs and few reviewers). Each has a concrete fix. The SDD task lifecycle maps cleanly onto TBD: one task = one trunk-merged increment.

## Applies If (ALL must hold)

- Trunk is red more than once per week and developers have lost trust in main — apply the "broken trunk" fixes first.
- Team keeps creating week-long feature branches despite wanting to do TBD — apply the long-lived branch solutions.
- PRs sit unreviewed for more than four hours — apply the review bottleneck solutions.
- Adopting SDD task lifecycle alongside TBD and need a mapping between the two.

## Skip If (ANY kills it)

- Greenfield projects that have not yet experienced these failure modes — apply good practices up front rather than fixing problems after they appear.
- Teams not using TBD — some of these solutions (e.g. feature flags for branch elimination) only make sense in a TBD context.

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

- parent skill: `solo/dev/automation-tooling/`
