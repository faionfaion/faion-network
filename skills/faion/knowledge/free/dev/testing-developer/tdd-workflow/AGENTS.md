---
slug: tdd-workflow
tier: free
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Covers the Red-Green-Refactor loop adapted for LLM-assisted development, why tests-as-spec reduce total tokens, PostToolUse hooks that enforce the RED step, per-behavior TDD cycle scripting, and the conditions under which TDD costs more than it saves (exploratory spikes, UI prototypes).
content_id: "27ccc09764ef490f"
tags: [tdd, testing, red-green-refactor, llm-assisted, workflow]
---
# TDD Workflow

## Summary

**One-sentence:** Covers the Red-Green-Refactor loop adapted for LLM-assisted development, why tests-as-spec reduce total tokens, PostToolUse hooks that enforce the RED step, per-behavior TDD cycle scripting, and the conditions under which TDD costs more than it saves (exploratory spikes, UI prototypes).

**One-paragraph:** Covers the Red-Green-Refactor loop adapted for LLM-assisted development, why tests-as-spec reduce total tokens, PostToolUse hooks that enforce the RED step, per-behavior TDD cycle scripting, and the conditions under which TDD costs more than it saves (exploratory spikes, UI prototypes).

## Applies If (ALL must hold)

- Starting a new feature or module where behavior is well-defined
- Writing business logic where correctness is critical
- Enforcing RED step discipline when an agent tends to skip it
- Setting up CLAUDE.md PostToolUse hooks for TDD enforcement
- Explaining TDD workflow to an agent working on Python/JS/Go code

## Skip If (ANY kills it)

- Exploratory spikes or prototypes where spec is unknown
- UI/layout work where visual feedback drives design
- Performance optimization (benchmark-driven, not test-driven)
- Rapid throwaway scripts

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

- parent skill: `free/dev/testing-developer/`
