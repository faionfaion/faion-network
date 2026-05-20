# Claude Code Adapter

Use this adapter when Faion runs inside Claude Code.

## Invocation

- Primary entry point: `/faion`.
- Keep `SKILL.md` frontmatter such as `allowed-tools`; it is part of Claude Code packaging.
- `CLAUDE.md` files are valid entrypoints and normally contain `@AGENTS.md`.

## User Choice

Map `platform user-choice primitive` to `AskUserQuestion`.

- Use it for brainstorm consent gates, ambiguous phase selection, deploy/destructive confirmations, and Phase 3.5 improvement approvals.
- Prefer 2-3 concrete options with explicit trade-offs.
- If the question is open text, ask plainly instead of forcing a choice UI.

## Subagents

Map `platform subagent-dispatch primitive` to Claude Code's Agent/Task dispatch.

- Use versioned prompt files where workflows reference them.
- Keep subagent prompts in English.
- For isolated write work, dispatch in a worktree when the workflow requires isolation.

## Retrieval

For default knowledge retrieval, run:

```bash
python3 ~/workspace/projects/faion-net/faion-network/skills/faion/scripts/retrieve.py "${CLAUDE_SESSION_ID:-}"
```

The script reads Claude session JSONL from `~/.claude/projects/`, uses `claude_agent_sdk`, and returns either `<faion_knowledge>` or `<faion_clarification>`.

## Quota And Memory

- Map `platform quota-state source` to `/tmp/claude-session-state.json` when it exists.
- Map `platform wakeup primitive` to Claude Code's wakeup/reminder capability when available.
- Map `platform cross-session memory store` to Claude project memory under `~/.claude/projects/` or project-local `.aidocs/memory/`, depending on the workflow.
- Claude hooks are configured in `hooks/hooks.json` and are Claude-only.
