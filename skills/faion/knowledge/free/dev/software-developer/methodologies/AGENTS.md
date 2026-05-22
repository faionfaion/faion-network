---
slug: methodologies
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A dispatcher index for the software-developer skill.
content_id: "a7ff26270f86b502"
tags: [routing, index, dispatcher, methodology-selector]
---
# Software Developer Methodology Index

## Summary

**One-sentence:** A dispatcher index for the software-developer skill.

**One-paragraph:** A dispatcher index for the software-developer skill. Not a standalone methodology — maps task keywords to canonical sibling methodology folders under free/dev/software-developer/. Each sibling contains full, authoritative content; this index provides a starting routing point only.

## Applies If (ALL must hold)

- The user gives a coarse task ("implement a Django service", "scaffold a Go API", "write tests for X") and you have not yet selected a sibling methodology folder.
- You need the canonical execution order for a multi-language task: Python to JS/TS to backend to DevOps to docs.
- You need to verify which methodology slugs actually exist before dispatching parallel subagents.

## Skip If (ANY kills it)

- Implementing from this file directly — every entry is a routing pointer, not a spec.
- Treating it as authoritative best-practices guidance — pull current guidance from each sibling.
- Citing it as the source of any rule — cite the sibling folder instead.

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

- parent skill: `free/dev/software-developer/`
