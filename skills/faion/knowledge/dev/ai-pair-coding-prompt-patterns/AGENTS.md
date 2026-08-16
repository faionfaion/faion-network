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
| Task description | free text | issue / task-list / pairing notes |
| Repo context | tree + relevant files | Claude Code / Cursor index |
| Cap policy | ai-diff-size-discipline config | team defaults |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pair-coding-prompt-patterns.py` | Validate ai-pair-coding-prompt-patterns artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[ai-diff-size-discipline]]
- [[ai-generated-test-validation]]
- [[exploratory-testing-charters]]
- [[deterministic-test-data-pattern]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on (a) task type, (b) existing spec / tests, and (c) pattern-specific stop conditions. Every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/ai-pair-coding-prompt-patterns.json",
  "type": "object",
  "required": [
    "scaffold_id",
    "pattern",
    "task_summary",
    "stop_conditions",
    "acceptance_checklist",
    "unit"
  ],
  "properties": {
    "scaffold_id": {
      "type": "string",
      "pattern": "^PS-[A-Z0-9-]{2,40}$"
    },
    "pattern": {
      "type": "string",
      "enum": [
        "spec-first",
        "test-first",
        "repo-grep",
        "diff-review",
        "refactor-isolate",
        "plan-then-execute",
        "branch-canary"
      ]
    },
    "task_summary": {
      "type": "string",
      "minLength": 8
    },
    "stop_conditions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string"
      }
    },
    "acceptance_checklist": {
      "type": "array",
      "minItems": 3,
      "items": {
        "type": "string"
      }
    },
    "unit": {
      "type": "string",
      "enum": [
        "feature",
        "refactor",
        "fix",
        "spike",
        "docs",
        "test"
      ]
    },
    "repo_grep_targets": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "prompt_body": {
      "type": "string"
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "scaffold_id": "PS-PRICING-ENDPOINT",
  "pattern": "spec-first",
  "task_summary": "Add POST /pricing endpoint that returns total price for a cart payload",
  "stop_conditions": [
    "Stop when tests pass",
    "Stop if diff exceeds 200 LOC",
    "Stop if any new import is not present in the repo"
  ],
  "acceptance_checklist": [
    "Spec written in docs/pricing.md before code",
    "Endpoint has at least 3 table-driven tests",
    "OpenAPI schema updated",
    "No imports outside requirements.txt"
  ],
  "unit": "feature",
  "repo_grep_targets": [
    "app/api/",
    "tests/api/"
  ],
  "prompt_body": "Read docs/pricing.md, then implement POST /pricing in app/api/pricing.py..."
}
```
