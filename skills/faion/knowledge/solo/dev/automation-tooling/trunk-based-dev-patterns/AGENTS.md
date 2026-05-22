---
slug: trunk-based-dev-patterns
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implement multi-step features safely on trunk by using feature flags to hide incomplete work, branch by abstraction to refactor without long-lived branches, and dark launching to test new implementations against production traffic before exposure.
content_id: "2b458a0ca1aec74e"
tags: [trunk-based-development, feature-flags, patterns, continuous-delivery, branching]
---
# Trunk-Based Development: Patterns

## Summary

**One-sentence:** Implement multi-step features safely on trunk by using feature flags to hide incomplete work, branch by abstraction to refactor without long-lived branches, and dark launching to test new implementations against production traffic before exposure.

**One-paragraph:** Implement multi-step features safely on trunk by using feature flags to hide incomplete work, branch by abstraction to refactor without long-lived branches, and dark launching to test new implementations against production traffic before exposure.

## Applies If (ALL must hold)

- Agent is implementing a multi-step feature behind a flag (Keystone Interface, Branch by Abstraction) — give it this reference for the pattern shape.
- Setting up the pre-commit hook + CI pipeline so trunk stays releasable; the YAML/.pre-commit-config.yaml blocks are copy-pastable.
- Dark-launch a new implementation in parallel and diff results — the snippet is the canonical shape.
- Migrating a long-lived feature branch to a series of trunk-merged increments; agent uses Branch-by-Abstraction to chunk it.

## Skip If (ANY kills it)

- Branching/lifetime principles, DORA metrics, GitFlow comparison — see sibling trunk-based-dev-principles.
- Feature flag infrastructure itself (provider choice, evaluation engine) — see feature-flags methodology.
- Release engineering for mobile/desktop where store review breaks daily-merge cadence.
- Codebases with no test gate — TBD without tests is "trunk is always broken".

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
