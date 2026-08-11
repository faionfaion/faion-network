# research-first-build

## Purpose
Build something whose shape is not decided yet: catalog three research axes, pick one concept against quantified criteria, design it, plan it, implement the tasks in parallel, produce assets, prove the toolchain, review and fix.

## Invoke
```
faion workflow build {recipe.json} --var brief={file} --var repo_path={repo} --var docs_dir={dir} --var feature_folder={dir} --var project_dir={dir} --var diff_base={sha} [--var axis_one={text}] [--var axis_two={text}] [--var axis_three={text}] [--var default_branch={branch}] [--var verify={cmds}] [--var gates={cmds}] [--target claude|codex|both] [--out-dir {dir}]
```

## Inputs
- `brief` — product brief every stage is grounded in; also the reviewer's guardrail doc. Required.
- `repo_path` — repo the pipeline builds in. Required.
- `docs_dir` — where the three research catalogs are written and read back from. Required.
- `feature_folder` — SDD feature folder for `spec.md` and the plan. Required.
- `project_dir` — toolchain directory the gate commands run against. Required: a var, never a literal, so a second product from this recipe cannot collide with the first.
- `diff_base` — sha the repo was at before the run; a greenfield repo's root commit is `git rev-list --max-parents=0 HEAD`. Required.
- `axis_one` / `axis_two` / `axis_three` — the research axes. Optional; defaults are domain mechanisms, market and audience, business model and unit economics.
- `default_branch` — branch the executors merge into. Optional, default `main`.
- `verify` — verify commands for executors and the fix applier, one per line. Optional, default empty.
- `gates` — gate commands, one per line; `{file}` becomes the path under verification. Optional, default empty — empty gates clean.

## Outputs
- Files: `.claude/workflows/research-first-build.js`, `research-first-build.codex.sh`, `research-first-build.lock.json`.
- Eleven stages: three `research_*` catalogs → `concept` (JSON pick with runner-up) → `design` → `plan` (JSON task list) → `implement` (fan-out, ≤6 worktrees) → `assets` → `bootstrap` (gated) → `review` (JSON verdict) → `fix` (gated, ≤2 rounds).
- The run writes `{docs_dir}/*-catalog.md`, `{feature_folder}/spec.md`, code commits on `default_branch`, and assets under the repo.

## When NOT to use
- The what is already decided and written down — that is `sdd-feature`, and paying for three research stages to re-derive a settled answer is waste.
- Content production: the catalogs feed a build, not an article. Use `article-pipeline`.
- Offline or air-gapped runs: the three research stages are the only stages in the catalog that need the network.

## Cost
The most expensive recipe here: eleven stages, three of them network research, plus one agent per planned task and per gate round. Budget accordingly; `concept` is the stage that decides how much the rest costs.
