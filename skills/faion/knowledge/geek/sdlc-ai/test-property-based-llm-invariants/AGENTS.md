# Property-Based Tests From LLM-Inferred Invariants

## Summary

For any pure function with a docstring, type signature, or one example call, run an agent that proposes invariants — round-trip, idempotence, oracle-equivalence, metamorphic, monotonicity — and writes them as `@given` Hypothesis (Python), `fast-check` (TS), or `proptest` (Rust) tests *before* writing example-based tests. The agent must justify each property from the source text and reject any property it cannot ground there. Anthropic's own red-team agent ran this loop on 100 popular Python packages (NumPy, SciPy, Pandas) and produced 984 bug reports across 786 modules with 56% true-bug rate on a manual sample (86% on top-ranked).

## Why

LLMs are demonstrably better at *inferring* algebraic properties from a docstring than at *inventing* example-based tests — examples drift toward the implementation, properties drift toward the spec. Property-based runners then shrink failures to minimal counter-examples, producing a debug-friendly bug report instead of a long log of one-off cases. Combining the two — agent proposes properties, runner shrinks failures — closes a gap example-based tests structurally cannot: discovering edge cases the developer never considered.

## When To Use

- Pure logic: serialization, parsing, math, sorting, dedup, schema validators, anything with an inverse or algebraic property.
- Code with a clear oracle (a slow reference implementation, a previous version, a spec equivalent).
- Stateless API endpoints whose request/response can be modelled as types.
- After example tests pass — properties find the cases the developer did not write.

## When NOT To Use

- Stateful side-effecting code without clear invariants (use stateful PBT only with care; see Hypothesis `RuleBasedStateMachine`).
- UI rendering / "looks right" code — there is no algebraic property.
- Code where the spec is "whatever the current output is" — properties become tautologies.
- Tight CI windows where shrinking time exceeds the budget — gate properties on a nightly job instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-property-rubric.xml` | Closed list of property classes the agent must pick from; rejection rule. |
| `content/02-source-grounded-rule.xml` | Every property must cite the docstring/type/example that justifies it. |

## Templates

| File | Purpose |
|------|---------|
| `templates/property-rubric.txt` | Prompt fragment listing the 5 property classes and source-grounding rule. |
| `templates/hypothesis-skeleton.py` | Hypothesis test skeleton with the 5 canonical property classes wired up. |
