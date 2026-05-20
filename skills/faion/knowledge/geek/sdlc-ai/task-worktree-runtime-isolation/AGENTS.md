---
slug: task-worktree-runtime-isolation
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Each parallel agent run gets its own git worktree, its own feature branch, its own scoped file-ownership manifest, AND its own runtime sandbox: distinct ports, database name, cache namespace, and secret bundle.
content_id: "87d7620d2270dd77"
tags: [worktree, runtime-isolation, parallel-agents, sandbox, git-worktree]
---
# One Task → One Branch → One Worktree → One Agent (with Runtime Isolation)

## Summary

**One-sentence:** Each parallel agent run gets its own git worktree, its own feature branch, its own scoped file-ownership manifest, AND its own runtime sandbox: distinct ports, database name, cache namespace, and secret bundle.

**One-paragraph:** Each parallel agent run gets its own git worktree, its own feature branch, its own scoped file-ownership manifest, AND its own runtime sandbox: distinct ports, database name, cache namespace, and secret bundle. The mapping is exactly one task → one branch → one worktree → one agent. The agent is forbidden from editing files outside its declared scope; collisions surface only at merge time, never at edit time. Crucially, worktrees alone do not isolate runtime — port and DB collisions are the documented 2026 failure mode — so the harness MUST allocate a runtime sandbox per worktree, not just a working directory.

## Applies If (ALL must hold)

- Any time more than one agent runs concurrently on the same repository.
- Multi-feature parallel build (orchestrator dispatches N subagents on different branches).
- Fan-out / map-reduce subagent dispatch where each leaf does isolated work.
- Comparison / arena mode (run the same task with different models, compare diffs).
- Long-running agent jobs where the human still needs to use the main checkout.

## Skip If (ANY kills it)

- A single agent doing sequential work — one worktree is enough; branching adds no value.
- Pure read-only research subagents that never write files — shared sandbox is fine, no isolation cost.
- Tiny scripts under ~50 LOC where the worktree setup overhead dominates the task.
- Repositories without local services (pure code-only, no DB, no port-bound dev server) — runtime isolation is a no-op there, but worktree isolation still applies.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
