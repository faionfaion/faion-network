# Workflow Platform Adapters

Workflow docs describe orchestration with platform-neutral primitives. Before executing any workflow, read the adapter for the active agent:

| Platform | Read | Applies to |
|----------|------|------------|
| Claude Code | `claude-code.md` | Slash entrypoint, `AskUserQuestion`, Agent dispatch, Claude quota files, Claude hooks. |
| Codex | `codex.md` | Skill use, direct questions, optional `spawn_agent`, local quota assumptions, project memory. |

Workflow content should not hard-code one agent runtime unless the workflow is explicitly about that runtime. Use:

- `platform user-choice primitive`
- `platform subagent-dispatch primitive`
- `platform quota-state source`
- `platform wakeup primitive`
- `platform cross-session memory store`
- `platform worktree isolation path`
