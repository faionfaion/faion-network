# Claude Code Hooks Reference

## Summary

**One-sentence:** Spec for lifecycle-event hooks: PreToolUse, PostToolUse, SessionStart, Stop. Block dangerous tools, auto-approve safe ops, format on edit, inject session context.

**One-paragraph:** Hooks execute at lifecycle events to enforce policy without human intervention. Misuse — wrapping complex logic in a 60s-timeout sync hook, mutating state non-reversibly, treating hooks as a general-purpose automation channel — produces flaky deploys and lost work. This methodology codifies the supported event set, the matcher syntax, the timeout cap, the side-effect rule (reversible only), and the per-event use-case table. Output is a settings.json hooks block validated by the schema.

**Ефективно для:**

- Security policy enforcement: block `rm -rf`, `DROP TABLE` за PreToolUse ще до execution.
- Auto-approve safe operations: reduce permission prompts у автоматичних pipelines.
- Post-edit formatting: prettier/ruff/eslint після кожного Write/Edit.
- Session-context injection (git branch, env) у SessionStart — агент не запитує.

## Applies If (ALL must hold)

- Action must run automatically at a lifecycle event.
- Logic is &lt; 60s synchronous (default hook timeout).
- Action's side effects are reversible if the hook fails mid-run.

## Skip If (ANY kills it)

- Hook logic complex enough to warrant a standalone agent — hooks are sync + blocking + 60s timeout.
- Need to modify model's text response (hooks operate on tool calls, not text).
- Action should be user-triggered, not automatic — use Command or Agent.
- Side effects irreversible (deploys, billing) — hooks run before confirmation dialogs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Event + matcher choice | PreToolUse / PostToolUse / SessionStart / Stop + regex | policy spec |
| Hook script | Bash / Python / Node script | ops |
| Settings.json access | write access to ~/.claude/settings.json or project settings.local.json | user |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: event-matcher-explicit, timeout-cap-60s, reversible-side-effects, exit-code-discipline, audit-log-discipline | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-event-and-matcher` | sonnet | Light judgment from policy. |
| `write-script` | haiku | Bash/Python boilerplate. |
| `wire-audit-log` | haiku | Template logging. |

## Templates

| File | Purpose |
|------|---------|
| `templates/settings-hooks-block.json` | settings.json hooks block template |
| `templates/pretooluse-block-dangerous.sh` | PreToolUse hook blocking rm -rf / DROP TABLE / sudo |
| `templates/posttooluse-format.sh` | PostToolUse hook running prettier / ruff format on edited files |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-hooks.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[agents]]
- [[commands]]
- [[skills]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
