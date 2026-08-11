# sdd-feature

## Purpose
Carry one SDD feature folder from intake to reviewed, gated implementation: analyze readiness, plan tasks, bootstrap the toolchain, build the planned tasks in parallel worktrees, review independently, fix only what the review blocks.

## Invoke
```
faion workflow build {recipe.json} --var feature_folder={dir} --var repo_path={repo} --var project_dir={dir} [--var default_branch={branch}] [--var verify={cmds}] [--var gates={cmds}] [--var guardrails={paths}] [--var clarifications={text}] [--var diff_base={ref}] [--target claude|codex|both] [--out-dir {dir}]
```

## Inputs
- `feature_folder` — SDD feature folder holding `spec.md` / `plan.md` / `TASK_*.md`. Required.
- `repo_path` — repo the feature is built in. Required.
- `project_dir` — directory the toolchain lives in and the gate commands run against (`backend/`, the repo root, one service subdir). Required: it is a var, not a literal, so two features never bootstrap the same tree by accident.
- `default_branch` — branch the executors merge into. Optional, default `main`.
- `verify` — verify commands for executors and the fix applier, one per line, run from the worktree root. Optional, default empty.
- `gates` — gate commands, one per line; `{file}` is replaced with the path under verification. Optional, default empty — an empty list gates clean.
- `guardrails` — project spec / constitution paths handed to the analyzer and the reviewer. Optional, default empty.
- `clarifications` — answers to the intake's open questions, fed to the planner. Optional, default empty.
- `diff_base` — diff base the reviewer reads the feature against. Optional, default `HEAD`.

## Outputs
- Files: `.claude/workflows/sdd-feature.js` and `sdd-feature.codex.sh` (or `{out-dir}/`), plus `sdd-feature.lock.json`.
- Six stages: `intake` → `plan` (JSON task list) → `bootstrap` (gated) → `implement` (fan-out, ≤4 concurrent worktrees) → `review` (JSON verdict) → `fix` (gated, ≤2 rounds).
- The run itself writes SDD artifacts into `feature_folder`, commits into `repo_path`, and merges each task into `default_branch` locally. No push.
- stdout: the compile envelope naming every stage, its fragment id and its composed id.

## When NOT to use
- A feature with no written spec — intake reports open questions, it does not invent intent. Answer them and re-run.
- Greenfield work whose shape is still unknown: use `research-first-build`, which decides what to build before planning it.
- A repo-wide cleanup with no feature folder: use `audit-and-fix`.
- Anything needing a push, a deploy or a release — every stage is local-only.

## Cost
Six stages plus two gate loops; one model call per stage, per fan-out item, and per gate round. Dominated by `implement` — one agent per planned task, four at a time.
