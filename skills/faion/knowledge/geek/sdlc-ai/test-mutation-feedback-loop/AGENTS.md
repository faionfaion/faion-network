---
slug: test-mutation-feedback-loop
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Coverage percent is a near-useless signal for AI-written tests — agents can hit 90% line coverage with assertions that never observe a mutation.
content_id: "bb5fe34dbe9b00b6"
tags: [mutation-testing, stryker, agent-feedback, ci-gate, test-quality]
---
# Mutation Testing as the Agent Feedback Signal

## Summary

**One-sentence:** Coverage percent is a near-useless signal for AI-written tests — agents can hit 90% line coverage with assertions that never observe a mutation.

**One-paragraph:** Coverage percent is a near-useless signal for AI-written tests — agents can hit 90% line coverage with assertions that never observe a mutation. Replace coverage gates with mutation testing (Stryker, mutmut, PIT) scoped to changed files, and feed the surviving-mutants report back into the agent's next iteration. The gate passes only when the mutation score on the diff clears a threshold (typical: 70 break / 80 high). Meta's ACH (FSE 2025) extended the pattern: an LLM both generates targeted mutants for a domain (privacy, compliance, payments) and writes the tests that kill them — 73% of ACH-suggested tests merged at Messenger and WhatsApp.

## Applies If (ALL must hold)

- Critical business logic where a wrong answer is expensive: payments, auth, pricing, rules engines, tax/refund logic.
- CI quality gates on PRs authored or co-authored by coding agents.
- Retrofitting a test suite onto legacy code that has shipped without one.
- Per-file gates on libraries where the public API surface is small and well bounded.

## Skip If (ANY kills it)

- Slow test suites where mutation cost (N_mutants x test_time) makes CI unaffordable — fix the suite first.
- Generated/serialization code where most mutants are equivalent (a + b vs b + a on a commutative op).
- Greenfield prototypes still discovering the spec — the test set churns too fast to gate on.
- UI/visual code where behavior is "looks right" rather than a checkable invariant.

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
