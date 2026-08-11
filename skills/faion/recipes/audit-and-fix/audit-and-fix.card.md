# audit-and-fix

## Purpose
Find out what is wrong with an existing tree and repair exactly that: bootstrap the toolchain, run the project's own checks into a machine verdict, review the diff against its intent, then fix under a bounded gate.

## Invoke
```
faion workflow build {recipe.json} --var repo_path={repo} --var project_dir={dir} --var scope_folder={dir} --var diff_base={ref} [--var gates={cmds}] [--var verify={cmds}] [--var guardrails={paths}] [--target claude|codex|both] [--out-dir {dir}]
```

## Inputs
- `repo_path` — repo under audit. Required.
- `project_dir` — toolchain directory the check commands run against. Required: a var, never a literal, so auditing a second service cannot bootstrap the first one's tree.
- `scope_folder` — folder holding the intent the audit checks against (SDD feature folder, spec directory). The reviewer cites it; the fixer is bound by it. Required.
- `diff_base` — diff base the audit reads the tree against: a sha, a tag or a release ref. Required.
- `gates` — check commands, one per line; `{file}` is replaced with the path under verification. Optional, default empty — empty checks report clean.
- `verify` — verify commands the fixer runs over its own repair, one per line. Optional, default empty.
- `guardrails` — project spec / constitution paths the reviewer cites blockers against. Optional, default empty.

## Outputs
- Files: `.claude/workflows/audit-and-fix.js`, `audit-and-fix.codex.sh`, `audit-and-fix.lock.json`.
- Four stages, no fan-out: `bootstrap` → `checks` (JSON `{clean, findings}`) → `review` (JSON verdict with cited blockers) → `fix` (gated, ≤2 rounds).
- Both audit stages report and never repair; `review` is capability read-only, `checks` gets workspace-write because a real test command writes caches and scratch databases.
- The run commits repairs into `repo_path`. No push, no deploy.

## When NOT to use
- Building something new — nothing here plans or implements a feature. Use `sdd-feature`.
- A tree with no recorded intent: the reviewer must cite a spec line or a guardrail rule, so with an empty `scope_folder` every finding degrades to a nit and nothing gets fixed.
- Broad refactors: the fixer repairs cited blockers only, and treats scope creep as a defect.

## Cost
The cheapest recipe here: four stages, no fan-out, at most two gate rounds — six model calls in the worst case. `checks` and the gate cost the project's own suite runtime.
