---
slug: test-tdd-red-green-split-agents
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When an AI coding agent runs the TDD loop, the test-writer (RED) and the implementer (GREEN) must execute in separate sub-agents with non-overlapping tool permissions: RED can write to `tests/` and read sources but cannot edit them; GREEN can edit sources and read the failing test output but cannot modify the test file.
content_id: "af6052a4ff2ccc2d"
tags: [tdd, red-green, sub-agents, tool-permissions, sdlc-ai]
---
# TDD with Red and Green in Separate Agents

## Summary

**One-sentence:** When an AI coding agent runs the TDD loop, the test-writer (RED) and the implementer (GREEN) must execute in separate sub-agents with non-overlapping tool permissions: RED can write to `tests/` and read sources but cannot edit them; GREEN can edit sources and read the failing test output but cannot modify the test file.

**One-paragraph:** When an AI coding agent runs the TDD loop, the test-writer (RED) and the implementer (GREEN) must execute in separate sub-agents with non-overlapping tool permissions: RED can write to `tests/` and read sources but cannot edit them; GREEN can edit sources and read the failing test output but cannot modify the test file. The orchestrator passes only the acceptance criterion to RED, only the test diff and pytest/jest failure to GREEN, and asserts a real RED→GREEN transition before merging. Without the split, a single agent that owns both files cheats by editing the test to pass.

## Applies If (ALL must hold)

- Agent-driven feature work whose spec is testable in pure functions or HTTP responses (parsers, validators, calculators, API endpoints).
- Bug-fix tickets with a clear regression scenario — RED reproduces, GREEN fixes.
- Greenfield modules where the public API surface is known up front.
- Hard-spec migrations (port library X to language Y) — golden-master tests fit the same split.

## Skip If (ANY kills it)

- Pure UI styling, layout work, exploratory spikes — TDD overhead is wasted there.
- Tasks whose acceptance criterion is not testable (research notes, prose docs, design artifacts).
- Throwaway scripts and demo code.
- Refactors of code that already has full test coverage — the existing tests are the RED of choice; no new test cycle needed.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
