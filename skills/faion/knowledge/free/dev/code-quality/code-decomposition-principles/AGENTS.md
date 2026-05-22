---
slug: code-decomposition-principles
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLMs produce partial or incorrect diffs when a file plus its tests exceed the effective context window (~20–50k tokens).
content_id: "dfd14751b485235b"
tags: [decomposition, refactoring, architecture, maintainability, code-organization]
---
# Code Decomposition Principles

## Summary

**One-sentence:** LLMs produce partial or incorrect diffs when a file plus its tests exceed the effective context window (~20–50k tokens).

**One-paragraph:** LLMs produce partial or incorrect diffs when a file plus its tests exceed the effective context window (~20–50k tokens). Humans review poorly past ~300 lines. Modular architectures correlate with 973× higher deployment frequency (2024 DORA report). The DORA findings and Addy Osmani's LLM workflow both confirm that small, single-responsibility files unlock both human and agent productivity.

## Applies If (ALL must hold)

- A target file exceeds ~300 lines and a subagent must edit it under a tight context budget.
- LLM keeps producing partial/incorrect diffs because it cannot hold the full file plus tests in one window.
- Designing a new module from a spec and laying out the file tree from the start.
- Onboarding an LLM to an unfamiliar repo: split first, then have the agent read the new tree.

## Skip If (ANY kills it)

- File is under 100 lines and tightly cohesive — splitting adds indirection without context savings.
- Hot path with a measured performance cost from indirection (rare in app code).
- Generated code (migrations, protobuf stubs) — apply rules to the source, not the output.
- Throwaway scripts and one-shot notebooks where the file is the unit of thought.

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

- parent skill: `free/dev/code-quality/`
