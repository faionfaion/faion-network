# Codex Workflow Adapter

Use this adapter for all workflows when running in Codex.

| Neutral primitive | Codex implementation |
|-------------------|----------------------|
| `platform user-choice primitive` | Ask a concise plain-text question in Default mode; use structured user input only when available in Plan mode. |
| `platform subagent-dispatch primitive` | Use `spawn_agent` only when the user explicitly authorized subagents, delegation, or parallel agent work. Otherwise execute locally. |
| `platform quota-state source` | No fixed file. Use conservative parallelism and avoid background pools without explicit approval. |
| `platform wakeup primitive` | Plain pause/resume instruction unless the environment exposes a scheduler. |
| `platform cross-session memory store` | Project-local `.aidocs/memory/` unless another path is specified. |
| `platform worktree isolation path` | `git worktree` paths under the repo or a workflow-specified temp/worktree root. |

Codex-specific rules:

- Do not require `/faion`; skill invocation is contextual.
- Do not assume subagents inherit context. When spawning, pass the prompt file path plus the parameter block explicitly.
- If subagents are not authorized, preserve the same workflow phases but run them in the parent session.
- Do not depend on Claude hook output, Claude statusline files, or Claude session JSONL.
- Keep user-facing questions Ukrainian when the current user is using Ukrainian.
- For SDD batch dispatch, map `agent_role` into the spawned agent task text, `model_strength` into the inherited/default Codex model unless the user requested otherwise, `isolation` into an explicit `git worktree` path, and `background` into `spawn_agent` only when delegation was explicitly authorized.
