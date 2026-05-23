---
slug: ai-pair-coding-prompt-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-net]
summary: Picks one of seven canonical prompt patterns for AI pair-coding (spec-first, test-first, repo-grep, diff-review, refactor-isolate, plan-then-execute, branch-canary) and emits a per-task prompt scaffold with stop conditions.
content_id: "169941c0e21258eb"
complexity: medium
produces: playbook-step
est_tokens: 4100
tags: [ai-pair-coding, prompt-engineering, claude-code, patterns]
---
# AI Pair-Coding Prompt Patterns

## Summary

**One-sentence:** Picks one of seven canonical prompt patterns for AI pair-coding (spec-first, test-first, repo-grep, diff-review, refactor-isolate, plan-then-execute, branch-canary) and emits a per-task prompt scaffold with stop conditions.

**One-paragraph:** Generic AI coding prompts produce drifting, large, untested diffs. This methodology selects from seven named prompt patterns based on the task shape and emits a per-task prompt with explicit stop conditions and an acceptance checklist. Each pattern names its inputs, the expected artefact shape, and the failure mode it prevents (e.g. spec-first prevents code-before-design; test-first prevents post-hoc-justification tests).

**Ефективно для:**

- Solo dev wiring Claude Code / Cursor into a daily coding loop.
- Onboarding a new contributor whose AI prompts produce sprawling diffs.
- Repo-grep tasks where the AI keeps inventing imports that don't exist.
- Refactor-isolate tasks where the AI keeps bundling features into the refactor.

## Applies If (ALL must hold)

- AI pair (Claude Code / Cursor / Continue / Aider) is the primary code author for the task.
- Task can be named (feature / refactor / fix / spike).
- Repo has tests OR will have tests by end of task.
- Author has authority to revert or split the AI's diff.

## Skip If (ANY kills it)

- Pure conversation / Q&A without code emission.
- Throwaway one-shot prompt (a script to run once).
- Multi-day epic where prompt pattern is the wrong granularity — use SDD.
- Codegen / proto regeneration — pattern is fixed by the tool.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task description | free text | issue / TODO / pairing notes |
| Repo context | tree + relevant files | Claude Code / Cursor index |
| Cap policy | ai-diff-size-discipline config | team defaults |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-diff-size-discipline]] | Caps the diff each pattern emits. |
| [[ai-generated-test-validation]] | Validates the tests the pattern requires. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules (named pattern, stop condition, acceptance checklist, repo-grep before invent, no-bundle) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for prompt-scaffold + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: vague-prompt, no-stop, invented-imports, bundled-tasks | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure (classify task → pick pattern → fill scaffold → run with gates → close) | 700 |
| `content/05-examples.xml` | essential | Worked example: spec-first pattern for a new /pricing endpoint | 600 |
| `content/06-decision-tree.xml` | essential | Routes task type → pattern → stop conditions | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ai_pair_coding_prompt_patterns_classify` | haiku | Pattern-match task description to pattern. |
| `ai_pair_coding_prompt_patterns_fill_scaffold` | sonnet | Compose stop conditions + acceptance checklist. |
| `ai_pair_coding_prompt_patterns_review_output` | sonnet | Verify pattern was followed in the AI's diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the prompt-scaffold artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in prompt-scaffold |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pair-coding-prompt-patterns.py` | Validate ai-pair-coding-prompt-patterns artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[ai-diff-size-discipline]]
- [[ai-generated-test-validation]]
- [[exploratory-testing-charters]]
- [[deterministic-test-data-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) task type, (b) existing spec / tests, and (c) pattern-specific stop conditions. Every leaf references a rule in `01-core-rules.xml`.
