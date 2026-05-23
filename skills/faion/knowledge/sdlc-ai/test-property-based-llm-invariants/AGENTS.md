# Property-Based Tests From LLM-Inferred Invariants

## Summary

**One-sentence:** For any pure function with a docstring, type signature, or example call, run an agent that proposes grounded invariants (round-trip, idempotence, oracle, metamorphic, monotonicity) and writes them as @given Hypothesis / fast-check / proptest tests before example-based tests.

**One-paragraph:** For any pure function with a docstring, type signature, or one example call, run an agent that proposes invariants — round-trip, idempotence, oracle-equivalence, metamorphic, monotonicity — and writes them as @given Hypothesis (Python), fast-check (TS), or proptest (Rust) tests before writing example-based tests. The agent must justify each property from the source text and reject any property it cannot ground there. Anthropic's own red-team agent ran this loop on 100 popular Python packages (NumPy, SciPy, Pandas) and produced 984 bug reports across 786 modules with 56% true-bug rate on a manual sample (86% on top-ranked).

**Ефективно для:**

- Pure stdlib-style functions з тривіальними типами.
- Numeric / scientific libraries (NumPy / SciPy / Pandas analogs).
- Refactor pure modules: invariants ловлять regressions.
- Bug-hunt mode: Anthropic 86% top-ranked true-bug rate.

## Applies If (ALL must hold)

- Function under test is pure (no I/O, no global state).
- Docstring, type signature, or example call exists as grounding source.
- Language has a property-based testing library (Hypothesis / fast-check / proptest).

## Skip If (ANY kills it)

- Function is impure (network calls, DB writes, global mutation).
- No docstring / types / example — nothing to ground invariants against.
- Property-based testing infra not yet wired into CI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Function source + docstring | code | repo |
| Property-based testing library | Hypothesis / fast-check / proptest | deps |
| Property rubric prompt | text | templates/property-rubric.txt |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hypothesis-skeleton.py` | Python Hypothesis property-test scaffold with @given + pinned seed. |
| `templates/property-rubric.txt` | Rubric prompt steering the agent through the five families with grounding requirement. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-property-based-llm-invariants.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-tdd-red-green-split-agents]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
