# Codex Adapter

Use this adapter when Faion runs inside Codex.

## Invocation

- There is no slash-command requirement. Treat Faion as an auto-invoked skill when the task matches `SKILL.md`.
- Ignore Claude-only frontmatter fields such as `allowed-tools`; they are preserved for Claude Code compatibility.
- Prefer local repository reads with `rg`, `find`, and `sed` to load only the relevant knowledge/playbook/workflow files.

## User Choice

Map `platform user-choice primitive` to Codex user interaction:

- In Plan mode, use the available structured user-input tool when present.
- In Default mode, ask a concise plain-text question only when a reasonable assumption would be risky.
- For approvals, state the exact action, target, and consequence before asking.

## Subagents

Map `platform subagent-dispatch primitive` to Codex `spawn_agent` only when the user explicitly asks for subagents, delegation, or parallel agent work.

- If the user did not authorize subagents, execute the workflow locally and keep the same phase semantics.
- When spawning, pass bounded, self-contained tasks and disjoint write scopes.
- For write tasks, tell workers they are not alone in the codebase and must not revert others' changes.

## Retrieval

Do not use `scripts/retrieve.py` by default; it depends on Claude session paths and `claude_agent_sdk`.

Codex default retrieval:

1. Read `skills/faion/SKILL.md`.
2. Read `skills/faion/adapters/codex.md`.
3. If a workflow trigger matches, read `skills/faion/workflows/AGENTS.md`, then the selected workflow `AGENTS.md`, then the specific `content/*.xml` files for the current phase.
4. For methodology lookup, search `skills/faion/knowledge/` with `rg` and load only the best-fitting files under the active tier boundary.
5. For playbooks, search `skills/faion/playbooks/<tier>/` and load the selected `playbook.md` plus cited methodologies if needed.

## Quota And Memory

- Map `platform quota-state source` to the current Codex session constraints; if no machine-readable quota file is available, use conservative parallelism and avoid launching background pools without explicit user approval.
- Map `platform wakeup primitive` to a plain user-facing pause/resume instruction unless the environment exposes a scheduler.
- Map `platform cross-session memory store` to project-local `.aidocs/memory/` unless the user names another memory location.
- Map `platform worktree isolation path` to `git worktree` directories chosen by the workflow or current repository conventions.
