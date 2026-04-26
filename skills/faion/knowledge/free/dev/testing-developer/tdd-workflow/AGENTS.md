# TDD Workflow

Test-Driven Development with LLM assistance: Red-Green-Refactor cycle, agent hooks, and when TDD pays off vs costs more.

## Summary

Covers the Red-Green-Refactor loop adapted for LLM-assisted development, why tests-as-spec reduce total tokens, PostToolUse hooks that enforce the RED step, per-behavior TDD cycle scripting, and the conditions under which TDD costs more than it saves (exploratory spikes, UI prototypes).

## Why

LLMs naturally skip the RED step — they write implementation and tests together, producing tests that prove the implementation rather than specify behavior. A structured TDD hook and per-behavior loop forces correct ordering: failing test first, minimal implementation second, refactor third. This yields higher-confidence suites with less total rework.

## When To Use

- Starting a new feature or module where behavior is well-defined
- Writing business logic where correctness is critical
- Enforcing RED step discipline when an agent tends to skip it
- Setting up CLAUDE.md PostToolUse hooks for TDD enforcement
- Explaining TDD workflow to an agent working on Python/JS/Go code

## When NOT To Use

- Exploratory spikes or prototypes where spec is unknown
- UI/layout work where visual feedback drives design
- Performance optimization (benchmark-driven, not test-driven)
- Rapid throwaway scripts

## Content

| File | What it covers |
|------|---------------|
| `content/01-red-green-refactor.xml` | The three phases with LLM-specific guidance, token savings rationale, common agent failure modes |
| `content/02-agent-hooks.xml` | PostToolUse hook config, CLAUDE.md TDD enforcement snippet, per-behavior loop structure |

## Templates

| File | Purpose |
|------|---------|
| `templates/tdd-cycle.sh` | Shell script: run failing test → implement → run passing test → prompt refactor |
