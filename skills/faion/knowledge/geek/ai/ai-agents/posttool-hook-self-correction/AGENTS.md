# PostToolUse Hook as Self-Correction Loop

## Summary

Wire `PostToolUse` hooks (matcher `"Write|Edit"`) to run linters, formatters, and typecheckers automatically after every file mutation. Hook stderr is fed back to the agent as a tool-result error message, so the model SEES the failure on its next turn and rewrites the bad change without needing a manual "now run lint" prompt. This turns a code-editing agent into a self-correcting loop using the deterministic hook layer instead of relying on the model to remember.

## Why

Code-editing agents that "remember to run lint" are unreliable — the model omits the check exactly when it matters (long contexts, after a tricky edit). Wiring lint/typecheck into a PostToolUse hook makes the verification deterministic and invisible: the agent emits `Write` or `Edit`, the hook runs `ruff check $CLAUDE_FILE_PATH`, and on failure stderr is injected into the next turn as a tool-result error. The agent is fine-tuned to react to tool errors by retrying with corrections — so the hook converts a manual "lint then fix" cycle into one auto-corrected turn at zero prompt cost.

## When To Use

- Any code-editing agent run with Claude Code's hook system (Bash, Edit, Write tools).
- CI bots and headless runs where no human is around to catch a missed lint.
- Strict-format pipelines: doc generators that must obey markdownlint, JSON producers that must validate against a schema.
- Prepush gates: typecheck on every Edit prevents shipping `any` or unused imports.

## When NOT To Use

- Read-only research agents — there's no mutation to validate, hooks add latency for nothing.
- Slow validators (>5s per call) — hook stalls every Edit; move slow checks to a background job and gate on commit instead.
- Model-driven exploratory tasks where lint failures are expected mid-flight (refactors that span many files) — relax the hook with `matcher: ""` or scope it to specific paths.

## Content

| File | What's inside |
|------|---------------|
| `content/01-feedback-loop.xml` | The PostToolUse rule, hook config shape, why stderr feedback closes the loop. |

## Templates

| File | Purpose |
|------|---------|
| `templates/settings.json` | Reference `.claude/settings.json` snippet wiring PostToolUse hooks for Python (ruff) and TypeScript (eslint+tsc). |
