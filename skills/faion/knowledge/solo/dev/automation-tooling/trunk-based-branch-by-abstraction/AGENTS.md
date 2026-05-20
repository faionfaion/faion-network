---
slug: trunk-based-branch-by-abstraction
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Replace a component incrementally on trunk without a long-lived branch: create a Protocol/interface over the old implementation, add a new implementation behind that interface, use a feature flag to route between them, validate the new one, then remove the old and collapse the abstraction.
content_id: "088636516a152c4b"
tags: [trunk-based-development, refactoring, branch-by-abstraction, protocol, incremental]
---
# Branch by Abstraction for Trunk-Based Development

## Summary

**One-sentence:** Replace a component incrementally on trunk without a long-lived branch: create a Protocol/interface over the old implementation, add a new implementation behind that interface, use a feature flag to route between them, validate the new one, then remove the old and collapse the abstraction.

**One-paragraph:** Replace a component incrementally on trunk without a long-lived branch: create a Protocol/interface over the old implementation, add a new implementation behind that interface, use a feature flag to route between them, validate the new one, then remove the old and collapse the abstraction. Five discrete steps, each mergeable in one day.

## Applies If (ALL must hold)

- Replacing a backend service, data layer, or third-party integration that affects many callers.
- Migrating from one API client to another while keeping existing behaviour unchanged during rollout.
- Any refactor estimated to take more than one day — break it into five abstraction steps instead of one long branch.
- When compliance requires a stable trunk and audit trail for each change step.

## Skip If (ANY kills it)

- Tiny one-file renames or argument signature changes — overhead exceeds benefit; refactor directly.
- Purely cosmetic refactors (rename, format) — no abstraction needed, rename inline and merge.
- Cases where the interface cannot be defined until the new implementation is written — sketch the interface first or use a simpler flag-wrap approach.
- Codebases with no tests on the callsites — you cannot validate the swap without a safety net.

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
