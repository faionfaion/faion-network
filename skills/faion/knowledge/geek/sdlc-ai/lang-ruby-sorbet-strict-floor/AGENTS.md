---
slug: lang-ruby-sorbet-strict-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For any Ruby file an AI agent is allowed to modify autonomously, declare # typed: true (or stricter), generate Tapioca RBIs for every gem and Rails DSL, and require bundle exec srb tc plus bundle exec tapioca check-shims to pass before a PR is opened.
content_id: "f08be690f8c8a48e"
tags: [ruby, sorbet, tapioca, static-types, rails]
---
# Ruby Sorbet Strict Floor with Tapioca RBI

## Summary

**One-sentence:** For any Ruby file an AI agent is allowed to modify autonomously, declare # typed: true (or stricter), generate Tapioca RBIs for every gem and Rails DSL, and require bundle exec srb tc plus bundle exec tapioca check-shims to pass before a PR is opened.

**One-paragraph:** For any Ruby file an AI agent is allowed to modify autonomously, declare # typed: true (or stricter), generate Tapioca RBIs for every gem and Rails DSL, and require bundle exec srb tc plus bundle exec tapioca check-shims to pass before a PR is opened. Sorbet's typecheck becomes the deterministic refusal channel: agent-hallucinated method calls and wrong arities fail at compile-equivalent time, not at runtime in production.

## Applies If (ALL must hold)

- Rails monoliths over ~50 KLOC where agents author non-trivial PRs.
- Multi-team Ruby orgs where a shared type contract reduces cross-team breakage.
- Any gem or service consumed by other internal projects (RBI doubles as the consumer-facing type spec).
- Codebases ratcheting strictness: start at # typed: false baseline, promote files to true then strict per PR.

## Skip If (ANY kills it)

- Toy gems, single-file Sinatra services, and one-off scripts — Sorbet bootstrap and Tapioca regen costs exceed the value.
- Spike or exploratory branches where the file shape is intentionally fluid.
- Codebases pinned to Ruby below 3.0 — Sorbet's runtime requires 3.0+ for current versions.

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
