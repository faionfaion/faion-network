# Claude Code Hooks

## Summary

**One-sentence:** Claude Code hook configuration: PreToolUse, PostToolUse, UserPromptSubmit, SubagentStop, Notification — wired to project pre-commit, secrets blocking, telemetry routing.

**One-paragraph:** Claude Code hook configuration: PreToolUse, PostToolUse, UserPromptSubmit, SubagentStop, Notification — wired to project pre-commit, secrets blocking, telemetry routing. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`config`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Project uses Claude Code with custom workflows or skills.
- Need to enforce 'when X happens, run Y' automatically — pre-commit, secrets block, telemetry.
- Settings.json is editable at user or project scope.

## Skip If (ANY kills it)

- Memory-only preferences suffice (no automated triggers needed).
- Default hooks satisfy current needs.
- Hook would only run rarely — a slash command is simpler.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Claude Code installed | version | user |
| settings.json path | filesystem | user/project |
| Hook target action | shell command / script | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/claude-code/skills-and-plugins` | How Claude Code skills + plugins relate to hooks. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `hook_yaml_compose` | haiku | Bounded fill of settings.json hooks block. |
| `hook_target_design` | sonnet | Design the action script. |
| `hook_failure_diagnose` | opus | Diagnose multi-hook interaction issues. |

## Templates

| File | Purpose |
|------|---------|
| `templates/settings.json.snippet` | Hooks block snippet for settings.json. |
| `templates/pre-tool-use.sh` | Sample PreToolUse hook (e.g. secrets gate). |
| `templates/post-tool-use.sh` | Sample PostToolUse hook (e.g. linter). |
| `templates/subagent-stop.sh` | Sample SubagentStop hook (e.g. notify). |
| `templates/_smoke-test.sh` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-code-hooks.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[skills-and-plugins]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether claude-code-hooks applies: root question — "Is the automation needed for every X event AND a simpler memory preference cannot suffice?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
