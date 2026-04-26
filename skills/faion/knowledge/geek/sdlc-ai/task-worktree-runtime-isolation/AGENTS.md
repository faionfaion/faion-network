# One Task → One Branch → One Worktree → One Agent (with Runtime Isolation)

## Summary

Each parallel agent run gets its own git worktree, its own feature branch, its own scoped file-ownership manifest, AND its own runtime sandbox: distinct ports, database name, cache namespace, and secret bundle. The mapping is exactly one task → one branch → one worktree → one agent. The agent is forbidden from editing files outside its declared scope; collisions surface only at merge time, never at edit time. Crucially, worktrees alone do not isolate runtime — port and DB collisions are the documented 2026 failure mode — so the harness MUST allocate a runtime sandbox per worktree, not just a working directory.

## Why

`git worktree` shares the `.git` object store across worktrees but gives each worktree its own working tree and HEAD. That eliminates index-lock contention and silent overwrites between concurrent agents working on different branches in the same repo. But two agents that each spin up a dev server on port 3000 still collide; two agents that each run `pytest` against `localhost/test_db` still corrupt each other's data. The published failure mode (penligent.ai, devcenter.upsun.com, augmentcode.com 2026) is exactly this: teams adopt worktrees, see filesystem isolation, and assume runtime isolation came along — it didn't. Adding port/DB/cache namespace allocation per worktree closes the gap. The pattern is the foundation of every parallel-agent harness shipped in 2026 (Claude Code multi-agent, Cursor parallel composers, Windsurf Wave 13).

## When To Use

- Any time more than one agent runs concurrently on the same repository.
- Multi-feature parallel build (orchestrator dispatches N subagents on different branches).
- Fan-out / map-reduce subagent dispatch where each leaf does isolated work.
- Comparison / arena mode (run the same task with different models, compare diffs).
- Long-running agent jobs where the human still needs to use the main checkout.

## When NOT To Use

- A single agent doing sequential work — one worktree is enough; branching adds no value.
- Pure read-only research subagents that never write files — shared sandbox is fine, no isolation cost.
- Tiny scripts under ~50 LOC where the worktree setup overhead dominates the task.
- Repositories without local services (pure code-only, no DB, no port-bound dev server) — runtime isolation is a no-op there, but worktree isolation still applies.

## Content

| File | What's inside |
|------|---------------|
| `content/01-worktree-per-task.xml` | The 1:1:1:1 mapping (task → branch → worktree → agent) and the file-scope manifest rule. |
| `content/02-runtime-sandbox-allocation.xml` | Why worktrees alone are not enough; how to allocate ports, DB names, and cache namespaces per worktree. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wt-spawn.sh` | Reusable shell function `wt_spawn <slug>` that creates worktree + branch + per-worktree env file. |
| `templates/wt-env.example` | Per-worktree env file template (PORT, DATABASE_URL, REDIS_URL, SECRETS_PROFILE). |
