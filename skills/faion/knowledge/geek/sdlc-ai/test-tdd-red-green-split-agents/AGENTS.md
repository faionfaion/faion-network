# TDD with Red and Green in Separate Agents

## Summary

When an AI coding agent runs the TDD loop, the test-writer (RED) and the implementer (GREEN) must execute in separate sub-agents with non-overlapping tool permissions: RED can write to `tests/` and read sources but cannot edit them; GREEN can edit sources and read the failing test output but cannot modify the test file. The orchestrator passes only the acceptance criterion to RED, only the test diff and pytest/jest failure to GREEN, and asserts a real RED→GREEN transition before merging. Without the split, a single agent that owns both files cheats by editing the test to pass.

## Summary continued

The orchestrator drives one cycle per acceptance criterion: AC → RED-subagent emits failing test, runner confirms RED, GREEN-subagent edits source until runner confirms green, refactor-subagent (optional, with both directories read-only) reviews the diff. If RED ever produces a passing test, the cycle aborts — passing tests on the first try mean the spec was already satisfied or the test is wrong.

## Why

Single-context TDD with an LLM degenerates into "edit the test until both pass" because the model has zero accountability for which file it changed. Separating the loop into sub-agents with disjoint tool permissions enforces the discipline mechanically: RED literally cannot edit `src/`, GREEN literally cannot edit `tests/`. This is the same separation-of-concerns argument that made TDD work for humans (writing tests first concentrates the mind) — re-applied at the tool-permission layer the agent is fine-tuned to respect. Reports from production Claude Code skill setups (alexop.dev, simonwillison.net) describe consistent convergence behavior under this split that single-context TDD never achieves.

## When To Use

- Agent-driven feature work whose spec is testable in pure functions or HTTP responses (parsers, validators, calculators, API endpoints).
- Bug-fix tickets with a clear regression scenario — RED reproduces, GREEN fixes.
- Greenfield modules where the public API surface is known up front.
- Hard-spec migrations (port library X to language Y) — golden-master tests fit the same split.

## When NOT To Use

- Pure UI styling, layout work, exploratory spikes — TDD overhead is wasted there.
- Tasks whose acceptance criterion is not testable (research notes, prose docs, design artifacts).
- Throwaway scripts and demo code.
- Refactors of code that already has full test coverage — the existing tests are the RED of choice; no new test cycle needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-permission-split.xml` | The disjoint-tools rule: RED writes tests-only, GREEN edits src-only. |
| `content/02-orchestrator-contract.xml` | What the orchestrator asserts between RED and GREEN turns and how it aborts on first-try-pass. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tdd-red.skill.md` | Frontmatter for the RED sub-agent skill (Read + Write on tests/ only). |
| `templates/tdd-green.skill.md` | Frontmatter for the GREEN sub-agent skill (Read + Edit on src/ only). |
