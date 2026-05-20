---
slug: test-property-based-llm-invariants
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For any pure function with a docstring, type signature, or one example call, run an agent that proposes invariants — round-trip, idempotence, oracle-equivalence, metamorphic, monotonicity — and writes them as @given Hypothesis (Python), fast-check (TS), or proptest (Rust) tests before writing example-based tests.
content_id: "915bebe3b6a1fa69"
tags: [property-based-testing, llm-invariants, hypothesis, test-automation, sdlc-ai]
---
# Property-Based Tests From LLM-Inferred Invariants

## Summary

**One-sentence:** For any pure function with a docstring, type signature, or one example call, run an agent that proposes invariants — round-trip, idempotence, oracle-equivalence, metamorphic, monotonicity — and writes them as @given Hypothesis (Python), fast-check (TS), or proptest (Rust) tests before writing example-based tests.

**One-paragraph:** For any pure function with a docstring, type signature, or one example call, run an agent that proposes invariants — round-trip, idempotence, oracle-equivalence, metamorphic, monotonicity — and writes them as @given Hypothesis (Python), fast-check (TS), or proptest (Rust) tests before writing example-based tests. The agent must justify each property from the source text and reject any property it cannot ground there. Anthropic's own red-team agent ran this loop on 100 popular Python packages (NumPy, SciPy, Pandas) and produced 984 bug reports across 786 modules with 56% true-bug rate on a manual sample (86% on top-ranked).

## Applies If (ALL must hold)

- Pure logic: serialization, parsing, math, sorting, dedup, schema validators, anything with an inverse or algebraic property.
- Code with a clear oracle (a slow reference implementation, a previous version, a spec equivalent).
- Stateless API endpoints whose request/response can be modelled as types.
- After example tests pass — properties find the cases the developer did not write.

## Skip If (ANY kills it)

- Stateful side-effecting code without clear invariants (use stateful PBT only with care; see Hypothesis RuleBasedStateMachine).
- UI rendering / "looks right" code — there is no algebraic property.
- Code where the spec is "whatever the current output is" — properties become tautologies.
- Tight CI windows where shrinking time exceeds the budget — gate properties on a nightly job instead.

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
