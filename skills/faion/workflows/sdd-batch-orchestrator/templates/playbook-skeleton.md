# Playbook: <Delivery Surface>

<One paragraph: what this surface is, when this playbook applies, what the canonical run looks like. Pick from: faion-net-be, faion-net-fe, faion-net-e2e, faion-network knowledge, faion-network-storybook, mediamanager_fe, mediamanager_be, neromedia/pashtelka/longlife/ender content pipelines, custom.>

## Trigger

<How a user typically asks for this batch (example phrasings or feature folder shapes under .aidocs/<project>/todo/).>

## Repo and branch

- Repo path: `<absolute path>`
- Default branch: `main` | `master` (specify exactly one — the monorepo `faion-net` uses `master`, most nested repos use `main`).
- Worktree root prefix: `/tmp/wt-<feature-id>-<short>`
- Merge lock: `/tmp/<repo-slug>-merge.lock` (e.g. `/tmp/faion-network-merge.lock`).

## End-to-end flow

```
PHASE 1 — INTAKE & CLARIFY
  ├─ <surface-specific intake notes>
  └─ <surface-specific clarification themes>

PHASE 2 — PLAN
  └─ Feature folders live under: <.aidocs/<project>/todo/<feature-id>/>

PHASE 3 — SETUP LOCAL ENV
  ├─ Commands to bring the local stack up: <list>
  └─ Data fixtures or env overrides: <list>

PHASE 4 — BASELINE CAPTURE (visual surfaces only)

PHASE 5 — WAVE EXECUTION
  └─ Wave-grouping heuristics for this surface: <which directories signal a shared file-set>

PHASE 6 — VERIFY & REVIEW LOOP
  ├─ Build / test commands: <list>
  ├─ Lint commands: <list>
  └─ Review focus points specific to this surface: <list>

PHASE 7 — RECAPTURE & DELIVER (visual surfaces only)
  └─ Delivery channel: <`tg-send` chat | SDD `done/` attachment>

PHASE 8 — CLOSE & DEPLOY
  └─ Deploy mechanism for this surface: <deploy-*.sh script + post-deploy verification>
```

## Parallelism heuristics

| Variant / area | Files typically touched |
|----------------|-------------------------|
| <area A> | `<file A>` |
| <area B> | `<file B>` |

## Pitfalls

1. <observed pitfall 1 + mitigation>
2. <observed pitfall 2 + mitigation>

## Checklist before declaring done

- [ ] Every feature folder moved `todo/ → done/`.
- [ ] Every `TASK_*.md` moved through its lifecycle.
- [ ] `CHANGELOG.md` updated with one `## [Unreleased]` entry per commit.
- [ ] Visual evidence (before + after) delivered for every visual feature.
- [ ] All commits ≤50-char title, no `Co-Authored-By`, no emojis.
- [ ] Pre-commit passed without `--no-verify`.
- [ ] Deploys / pushes performed only after explicit user authorization (`AskUserQuestion`).
