# Refactoring Patterns

## Summary

Catalog of structural code transformations that improve readability and maintainability without changing external behavior: Extract Method/Function, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Numbers, Decompose Conditional, Rename for Clarity, Move Method. Each is applied one at a time, with tests green before and after.

## Why

Refactoring in small, test-verified steps lowers the risk of introducing regressions. Naming the pattern (e.g. "Extract Method") makes the change reviewable and reversible. The Boy Scout Rule — leave code better than you found it — applied incrementally prevents accumulation of complexity that eventually blocks feature delivery.

## When To Use

- Preparatory refactoring before a feature ("make the change easy, then make the easy change").
- Reducing cyclomatic complexity or function length flagged by linters.
- Eliminating duplication detected by `jscpd` or `pylint duplicate-code`.
- Modernizing legacy modules: replacing magic constants, decomposing god classes.
- Pre-test refactoring to create seams for mocks before adding tests.

## When NOT To Use

- During the same commit as a behavior modification — refactoring requires tests unchanged.
- When tests do not cover the affected code paths — add characterization tests first.
- Hot paths where "messy" form is intentional (manual loop unrolling, allocation reuse).
- Right before a release window — defer to next cycle.
- Generated code, vendored libraries, or migration scripts.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Extract Method, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Replace Magic Numbers, Decompose Conditional, Rename, Move Method — with before/after examples. |
| `content/02-workflow.xml` | Safe refactoring steps: ensure coverage, micro-edit loop, IDE tools, verify behavior, clean up. |
| `content/03-antipatterns.xml` | Big-bang refactoring, refactoring without tests, mixing with features, over-engineering, incomplete refactoring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refactor-scope-guard.sh` | Pre-commit hook: fail if a `refactor:` commit touches more than 5 files. |
