# TDD Workflow

## Summary

Red-Green-Refactor cycle for test-driven development: write one failing test, write minimal code to pass it, then improve structure without changing behavior. The cycle runs per behavior, not per feature. The orchestrating agent must verify test failure before allowing implementation (preventing the "skip RED" failure mode).

## Why

Agents skip the RED step and write implementation first, then tests that validate what they wrote — this is rationalization, not verification. Without an enforced cycle, code is untestable by design and refactors break silently. TDD forces the interface to be designed from the consumer's perspective before any implementation exists.

## When To Use

- Bug-fix workflow: reproduce the bug as a failing test before touching production code.
- Pure-function or business-logic implementation where requirements are precise (validators, calculators, parsers).
- API contract design — tests document the public surface before any handler exists.
- Library / SDK work where consumers depend on a stable interface.
- Onboarding an agent to an unfamiliar codebase — writing tests first forces reading the existing API.

## When NOT To Use

- Exploratory spikes or research code — feedback loop is faster without tests.
- UI prototypes where the design changes hourly.
- Glue scripts and one-off migrations.
- Code intrinsically hard to test (rendering, hardware drivers, framework internals).
- Hot-fix under outage pressure — write the fix, add the regression test in a follow-up PR.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cycle.xml` | RED / GREEN / REFACTOR rules; prompt patterns per phase; triangulation rule to prevent hardcoded returns. |
| `content/02-examples.xml` | Python password validator walked through full cycle; TypeScript email service; bug-fix reproduction pattern. |
| `content/03-antipatterns.xml` | Skip-RED failure mode, mock-everything, weak assertions (`assert result is not None`), gold-plating, skipped refactor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tdd.sh` | Single-behavior loop driver: asserts RED, waits for impl, asserts GREEN, runs full suite for REFACTOR. |
