# hooks/

Claude Code plugin hooks shipped with `faion-network`.

## Registration

Only `hooks.json` is loaded by the runtime. It registers three `UserPromptSubmit` commands, each `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/<file>` with `timeout: 5`. A file present here but absent from `hooks.json` does not run — `track-wakeup.sh` (PostToolUse for `ScheduleWakeup`) is currently unregistered and invoked elsewhere.

| File | Effect |
|------|--------|
| `context-compact-gate.py` | ctx >40% blocks the prompt unless it starts with `compact` or contains `КРИТИЧНО`; 30-40% injects a soft warning; <=30% silent |
| `stop-improver-check.py` | Injects an improver suggestion once the transcript passes ~25% context |
| `quota-guard.py` | Parks work at 5h quota >=95%, resumes below 90% |

## Conventions

- stdout is contract, not logging. Emit either nothing or one JSON object with `hookSpecificOutput.additionalContext`; any stray `print()` lands in the model's context.
- Exit 0 to allow, exit 2 to block. `quota-guard.py` uses exit 2.
- Stay well under the 5s timeout. Read pre-computed state from `/tmp/claude-*.json` written by the statusline; never call a network or `op`.
- Never crash a session: wrap all I/O so a missing state file degrades to a silent pass-through.
- Hooks read machine-local paths (`/tmp/claude-session-state.json`, `~/.claude/parked-*.json`). They are NERO-runtime specific and are not portable to a customer install.

## Gotchas

- `quota-guard.py`'s docstring says "PreToolUse hook" while `hooks.json` registers it under `UserPromptSubmit`. The registration wins; treat the docstring as stale.
- `__pycache__/` is checked into the working tree here. Do not import from it.
