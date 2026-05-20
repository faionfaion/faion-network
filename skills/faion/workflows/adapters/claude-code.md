# Claude Code Workflow Adapter

Use this adapter for all workflows when running in Claude Code.

| Neutral primitive | Claude Code implementation |
|-------------------|----------------------------|
| `platform user-choice primitive` | `AskUserQuestion` with 2-3 options and explicit trade-offs. |
| `platform subagent-dispatch primitive` | Agent/Task dispatch, preferably pointing at versioned prompt files. |
| `platform quota-state source` | `/tmp/claude-session-state.json` plus any statusline quota files. |
| `platform wakeup primitive` | Claude Code wakeup/reminder capability when available. |
| `platform cross-session memory store` | `~/.claude/projects/.../memory/` or project-local `.aidocs/memory/`. |
| `platform worktree isolation path` | `.claude/worktrees/` or workflow-provided `git worktree` paths. |

Claude-specific rules:

- `/faion` is the user-visible workflow entrypoint.
- Keep Claude hook behavior in `hooks/hooks.json`; Codex does not consume those hooks.
- Subagent prompt files should remain English and self-contained.
- Use Ukrainian for user-facing choices and confirmations.
- For SDD batch dispatch, map `agent_role` to `subagent_type` (`general-purpose`, `faion-sdd-executor-agent`, or `nero-sdd-executor-agent`), `model_strength` to the configured Claude model, `isolation` to worktree dispatch, and `background` to `run_in_background`.
