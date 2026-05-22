<!--
purpose: TDD-discipline reminder block to append to project CLAUDE.md
consumes: nothing — agent reads it on session start
produces: in-context TDD rules that bias the model toward RED-first
depends-on: project CLAUDE.md exists
token-budget-impact: ~120 tokens
-->

## TDD Workflow

For every new function or method:

1. Write the failing test FIRST. Run it.
2. Confirm: test output shows FAILED with the expected error (not an import error).
3. Write minimal implementation. Run tests again: must show PASSED.
4. Refactor if needed. Tests must still pass.
5. Commit both test and implementation together.

NEVER write implementation before a failing test exists.
