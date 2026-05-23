---
slug: rust-testing-antipatterns
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Review checklist catching Utc::now() in assertions, sleep-driven async waits, shared global state, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse.
content_id: "4fce5ac9486a812a"
complexity: medium
produces: checklist
est_tokens: 4300
tags: [rust, testing, antipatterns, agent-gotchas, code-review]
---
# Rust Testing Anti-Patterns and Agent Gotchas

## Summary

**One-sentence:** Review checklist catching Utc::now() in assertions, sleep-driven async waits, shared global state, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse.

**One-paragraph:** A review checklist and anti-pattern catalogue for Rust test suites, focusing on the failure modes AI agents introduce most frequently: Utc::now() in assertion paths, sleep-driven async waits, shared global state via static mut, hardcoded ports, hallucinated mockall predicates, and flake quarantine misuse. Output is a per-PR review checklist + clippy denies + a CI gate flagging the common patterns.

**Ефективно для:**

- PR reviews on test code authored by AI agents.
- Tightening CI to deny known flaky patterns (sleep+now in assertions).
- Auditing existing test suites for shared global state breakage.
- Replacing tokio::time::sleep with tokio::time::pause in unit tests.

## Applies If (ALL must hold)

- Rust crate has ≥1 integration test using tokio runtime.
- Agents author or modify test files in the repo.
- Test suite has recent flakes attributed to timing or shared state.
- Team can enforce clippy denies in CI.

## Skip If (ANY kills it)

- Test suite is tiny (<10 tests) and not under active development.
- All tests are pure value-in-value-out; no async, no shared state.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent CI flake report | md / log | ops |
| Test file inventory | list | team |
| CI runner | config | ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/backend-systems/rust-error-handling/AGENTS.md` | shared AppError pattern affects test setup |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | Antipatterns (symptom / root-cause / fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `review-pr-tests` | sonnet | Pattern matching against test code needs judgement. |
| `rewrite-sleeps-to-pause` | sonnet | Rewriting async timing benefits from sonnet. |
| `validate-output` | haiku | Schema check is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/review-checklist.md` | Per-PR test review checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing-antipatterns.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/backend-systems/`
- [[rust-backend]]
- [[rust-error-handling]]
- [[rust-http-handlers]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
