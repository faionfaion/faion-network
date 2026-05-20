---
slug: test-golden-master-legacy-rewrite
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have current behaviour.
content_id: "06d7715a1c230bbe"
tags: [golden-master, legacy-rewrite, corpus, snapshot-testing, agent-testing]
---
# Golden-Master Corpus for AI-Driven Legacy Rewrites

## Summary

**One-sentence:** When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have current behaviour.

**One-paragraph:** When you ask a coding agent to rewrite a 5000-line legacy module, you have no spec — you have current behaviour. Capture inputs and outputs of the current implementation from production traffic, fixtures, or a fuzzer into a committed corpus of (input, expected_output) pairs; the agent's rewrite passes only when it reproduces every pair, byte-for-byte, or each diff is explicitly approved row-by-row. This is the only test that scales to AI-driven rewrites of untested legacy: it is the spec the legacy never had, captured automatically, and it gives the agent a deterministic GREEN signal that does not depend on human ability to read the old code.

## Applies If (ALL must hold)

- Rewriting a legacy module/service with poor or no test coverage that an agent will touch.
- Cross-language ports (Python to Rust, PHP to Go) where preserving exact output is the success criterion.
- Library upgrades where vendor changelogs hint at behavioural shifts (date parsing, timezone, locale).
- Any "I don't trust the existing tests but I do trust production" rewrite.
- Refactoring a deterministic transformer (parser, formatter, exporter) under agent control.

## Skip If (ANY kills it)

- Greenfield code with no prior behaviour to preserve — write unit tests against the spec instead.
- Pervasive nondeterminism without normalization (timestamps, UUIDs, random IDs, ORDER BY-less queries).
- Tiny modules under ~200 LOC where targeted unit tests are cheaper than capture infrastructure.
- Stateful interactive flows (UI, multiplayer game tick) where I/O shape isn't a function of input alone.

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
