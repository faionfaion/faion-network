# Mutation Testing as the Agent Feedback Signal

## Summary

Coverage percent is a near-useless signal for AI-written tests — agents can hit 90% line coverage with assertions that never observe a mutation. Replace coverage gates with mutation testing (Stryker, mutmut, PIT) scoped to changed files, and feed the surviving-mutants report back into the agent's next iteration. The gate passes only when the mutation score on the diff clears a threshold (typical: 70 break / 80 high). Meta's ACH (FSE 2025) extended the pattern: an LLM both generates targeted mutants for a domain (privacy, compliance, payments) and writes the tests that kill them — 73% of ACH-suggested tests merged at Messenger and WhatsApp.

## Why

Mutation testing measures whether tests actually detect behavior changes — the only "truth-bearing" signal cheap enough to put behind a CI gate. One DEV.to teardown reported "93% line coverage, 34% mutation score" on AI-written tests: the assertions existed but trivial mutants survived. Agents that consume the mutation report converge on stronger assertions because each surviving mutant is a concrete, reproducible failure — far better feedback than a coverage delta.

## When To Use

- Critical business logic where a wrong answer is expensive: payments, auth, pricing, rules engines, tax/refund logic.
- CI quality gates on PRs authored or co-authored by coding agents.
- Retrofitting a test suite onto legacy code that has shipped without one.
- Per-file gates on libraries where the public API surface is small and well bounded.

## When NOT To Use

- Slow test suites where mutation cost (`N_mutants × test_time`) makes CI unaffordable — fix the suite first.
- Generated/serialization code where most mutants are equivalent (`a + b` vs `b + a` on a commutative op).
- Greenfield prototypes still discovering the spec — the test set churns too fast to gate on.
- UI/visual code where behavior is "looks right" rather than a checkable invariant.

## Content

| File | What's inside |
|------|---------------|
| `content/01-changed-file-gate.xml` | Run mutation only on changed files; thresholds; CI wiring. |
| `content/02-feedback-loop.xml` | Pipe surviving-mutants report back to the agent until score clears. |

## Templates

| File | Purpose |
|------|---------|
| `templates/stryker.conf.json` | Stryker config with break/high thresholds and incremental mode. |
| `templates/mutation-prompt.txt` | Prompt fragment that consumes a surviving-mutants list and asks for targeted assertions. |
