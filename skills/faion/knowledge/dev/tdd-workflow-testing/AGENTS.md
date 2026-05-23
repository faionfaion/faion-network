# TDD Workflow

## Summary

**One-sentence:** Produces a TDD-workflow config (per-behavior RED-GREEN-REFACTOR cycle, PostToolUse hook, CLAUDE.md snippet) for LLM-assisted development.

**One-paragraph:** LLMs naturally skip the RED step — they write implementation and tests together, producing tests that prove the implementation rather than specify behavior. This methodology emits a per-behavior loop script, a PostToolUse hook that auto-runs pytest after a file write, and a CLAUDE.md snippet that pins the discipline. Result: failing test first, minimal implementation second, refactor third — verifiable in CI.

**Ефективно для:** solopreneur using Claude Code who keeps catching themselves letting the model write tests after the implementation lands.

## Applies If (ALL must hold)

- Starting a new feature or module where behavior is well-defined.
- Writing business logic where correctness is critical.
- Enforcing RED-step discipline when an agent tends to skip it.
- Setting up PostToolUse hooks for TDD enforcement.

## Skip If (ANY kills it)

- Exploratory spikes or prototypes where spec is unknown.
- UI/layout work — visual feedback drives design.
- Performance optimization — benchmark-driven, not test-driven.
- Throwaway scripts with no production use.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `behavior-list.yaml` | list of {behavior, signature, happy_path, edge_cases} | operator |
| `test_command` | string (e.g., `pytest tests/test_x.py -x`) | repo |
| `claude_md_path` | path | repo |
| `settings_json_path` | path (Claude Code settings.json) | user config |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[testing-pytest]] | RED-GREEN cycle assumes pytest semantics. |
| [[code-review-basics]] | Refactor step uses review heuristics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: RED before GREEN, one behavior per cycle, minimal GREEN, no behavior change in REFACTOR, commit test+impl together, no TDD on UI/spike. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tdd-workflow-config artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: write tests after, batch behaviors, generalize too early, add behavior in REFACTOR, skip the failing-run step. | ~800 |
| `content/04-procedure.xml` | recommended | 7-step per-behavior loop (write RED → run RED → write GREEN → run all → refactor → run all → commit). | ~700 |
| `content/05-examples.xml` | recommended | One worked behavior end-to-end + sample CLAUDE.md snippet + PostToolUse hook JSON. | ~700 |
| `content/06-decision-tree.xml` | essential | Picks TDD vs spike-first vs benchmark-driven based on behavior_known + visual_feedback_drives. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_behavior_list` | haiku | Mechanical YAML→typed list. |
| `prioritize_behaviors` | sonnet | Sequencing happy path vs edge cases. |
| `audit_for_red_skip` | opus | Detecting silent test-after-implementation in agent transcripts. |
| `emit_workflow_config` | sonnet | Mechanical JSON emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/tdd-cycle.sh` | Shell script: run failing test → implement → run passing test → prompt refactor. |
| `templates/claude-md-snippet.md` | TDD-discipline reminder block to append to CLAUDE.md. |
| `templates/posttool-hook.json` | Settings.json fragment that runs pytest after Write/Edit on test_*.py. |
| `templates/_smoke-test.yaml` | Minimum behavior list (one happy path). |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-tdd-workflow.py` | Validates emitted config against the JSON schema. | Pre-commit. |

## Related

- [[testing-pytest]]
- [[unit-testing]]
- [[code-review-basics]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on `behavior_known` (no → spike-first, then tests; yes → continue), then on `visual_feedback_drives` (yes → screenshot-driven, defer TDD; no → continue), then on `performance_dominant` (yes → benchmark-driven; no → strict RED-GREEN). Each leaf cites a rule id.
