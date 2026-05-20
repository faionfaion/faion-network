---
slug: rust-testing-antipatterns
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A review checklist and anti-pattern catalogue for Rust test suites, focusing on the failure modes that AI agents introduce most frequently: Utc::now() in assertion paths, sleep-driven async waits, shared global state, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse.
content_id: "672d3afd401eb954"
tags: [rust, testing, antipatterns, agent-gotchas, code-review]
---
# Rust Testing Anti-Patterns and Agent Gotchas

## Summary

**One-sentence:** A review checklist and anti-pattern catalogue for Rust test suites, focusing on the failure modes that AI agents introduce most frequently: Utc::now() in assertion paths, sleep-driven async waits, shared global state, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse.

**One-paragraph:** A review checklist and anti-pattern catalogue for Rust test suites, focusing on the failure modes that AI agents introduce most frequently: Utc::now() in assertion paths, sleep-driven async waits, shared global state, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse.

## Applies If (ALL must hold)

- Reviewing any Rust test PR authored or modified by an AI agent.
- Running the anti-pattern lint script (rust-test-lint.sh) in pre-commit or CI.
- During test suite audits on codebases that have grown without a formal testing standard.
- When onboarding a new agent that will generate tests for a Rust codebase.

## Skip If (ANY kills it)

- Non-test production code — these checks are scoped to #[test] and tests/ paths only.
- Benchmark modules under benches/ — the rules around sleep and Utc::now do not apply there.

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

- parent skill: `pro/dev/backend-systems/`
