---
name: spec-to-code-pipeline
description: Transform a completed design.md into an implementation-plan.md, task files, and a first merged PR — the full handoff from design to running code.
tier: solo
group: sdd-workflow
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have taken a finished `design.md` for one feature all the way through to a merged pull request: a concrete `implementation-plan.md` with token-estimated tasks, individual `TASK-NN.md` files in `.aidocs/<feature>/todo/`, a Claude Code or Cursor session that implements the first task, and a PR whose description links back to the spec and design docs.

## Prerequisites

- A completed `spec.md` for the feature (acceptance criteria written and reviewed). See `writing-first-spec` if you have not done this yet.
- A completed `design.md` covering approach, API/data contract, and key files to change.
- A feature folder already created at `.aidocs/in-progress/feature-<slug>/` with `todo/`, `in-progress/`, and `done/` subdirs.
- Git installed, repo on a remote (GitHub), and a branch strategy in place (feature branch off `main`).
- Optional: `faion-cli` installed (`pip install faion-cli`) for SDD scaffolding commands.

## Steps

### Step 1 — Re-read design.md and extract the work units

Open `.aidocs/in-progress/feature-<slug>/design.md` and read the "Key files" table and "Approach" section. For the favourites feature example used throughout this playbook, the design says:

```
Approach: Add a boolean `is_favourite` field to the Task model (per-user via a
join table), expose it through the existing REST endpoint, and update the React
task card to show a toggle star icon with optimistic UI.

Key files:
| File | Change |
|------|--------|
| taskapp/models.py | add Favourite join-table model |
| taskapp/serializers.py | expose is_favourite field |
| taskapp/views.py | filter endpoint for favourites tab |
| frontend/src/components/TaskCard.tsx | star toggle with optimistic update |
| frontend/src/pages/FavouritesTab.tsx | new page, filtered task list |
```

Write down each distinct work unit on paper or in a scratch file. Each unit should be completable and committable in one sitting without blocking any other work.

### Step 2 — Write implementation-plan.md

Create `.aidocs/in-progress/feature-<slug>/implementation-plan.md`:

```markdown
# Implementation Plan: Favourites

## Tasks

| ID | Description | Deps | Est. tokens |
|----|-------------|------|-------------|
| TASK-01 | Add Favourite join-table model + migration | — | ~8k |
| TASK-02 | Expose is_favourite in TaskSerializer + filter endpoint | TASK-01 | ~12k |
| TASK-03 | Star toggle component (TaskCard.tsx) with optimistic UI | — | ~18k |
| TASK-04 | FavouritesTab page + route | TASK-03 | ~15k |
| TASK-05 | Integration tests (API + React Testing Library) | TASK-02, TASK-04 | ~20k |

## Build order

TASK-01 → TASK-02 → TASK-05
TASK-03 → TASK-04 → TASK-05

## Parallelisable

TASK-01 and TASK-03 have no shared deps — they can be started in parallel by
separate sessions if needed.
```

Rules for this table:
- Token estimates should reflect the size of the reading context + expected output, not wall-clock work.
- Dependencies list only hard blockers (TASK-02 needs the model TASK-01 creates).
- Keep tasks ≤20k tokens each; split if larger.

### Step 3 — Create TASK-NN.md files in todo/

For each row in the plan, create a file at `.aidocs/in-progress/feature-<slug>/todo/TASK-NN.md`. Use this template for each:

```markdown
# TASK-01: Add Favourite join-table model + migration

## Context

Feature: Favourites (spec: `../spec.md`, design: `../design.md`)
Branch: feat/favourites

## What to do

1. Add `Favourite` model to `taskapp/models.py`:
   - fields: `user` (FK → User), `task` (FK → Task), `created_at` (auto_now_add)
   - Meta: `unique_together = [["user", "task"]]`
2. Generate migration: `python manage.py makemigrations taskapp`
3. Run migration locally: `python manage.py migrate`
4. Add `FavouriteInline` to `TaskAdmin` in `taskapp/admin.py`

## Acceptance

- [ ] `python manage.py migrate` exits 0 on a clean DB
- [ ] `Favourite.objects.create(user=u, task=t)` works in Django shell
- [ ] Duplicate user+task raises `IntegrityError`

## Files to change

| File | Change |
|------|--------|
| taskapp/models.py | add Favourite model |
| taskapp/admin.py | register FavouriteInline |

## Commit message

`feat(TASK-01): add Favourite join-table model + migration`
```

Repeat for TASK-02 through TASK-05. The key discipline: every task file is self-contained enough that an LLM agent can execute it by reading only the task file + the files listed in "Files to change".

### Step 4 — Create the feature branch

```bash
git checkout main && git pull
git checkout -b feat/taskapp-favourites
```

### Step 5 — Spawn a Claude Code or Cursor session for the first task

Move the task to in-progress:

```bash
mv .aidocs/in-progress/feature-taskapp-favourites/todo/TASK-01.md \
   .aidocs/in-progress/feature-taskapp-favourites/in-progress/TASK-01.md
```

Open Claude Code (or Cursor) and give it a single prompt:

```
Read .aidocs/in-progress/feature-taskapp-favourites/in-progress/TASK-01.md
and implement everything listed in "What to do". After each file change, run
the acceptance checks listed in the task. Commit with the message in the task
file when all checks pass.
```

Let the session run. Do not context-switch until it commits or reports a blocker.

### Step 6 — Verify the task, then close it

After the session commits, run the acceptance checks manually:

```bash
python manage.py migrate --run-syncdb
python manage.py shell -c "
from taskapp.models import Favourite, Task
from django.contrib.auth.models import User
u = User.objects.first(); t = Task.objects.first()
f = Favourite.objects.create(user=u, task=t)
print('created:', f.pk)
"
```

If all checks pass, move the task to done:

```bash
mv .aidocs/in-progress/feature-taskapp-favourites/in-progress/TASK-01.md \
   .aidocs/in-progress/feature-taskapp-favourites/done/TASK-01.md
```

Repeat Steps 5–6 for TASK-02, then TASK-03, TASK-04 (which can run in parallel on separate branches if you wish), then TASK-05.

### Step 7 — Open the pull request

Once all tasks are in `done/`, push the branch and open a PR:

```bash
git push -u origin feat/taskapp-favourites
gh pr create \
  --title "feat: favourites feature (star tasks, dedicated tab)" \
  --body "$(cat <<'EOF'
## Summary

Implements the Favourites feature as specified in spec.md and design.md.

- TASK-01: Favourite join-table model + migration
- TASK-02: is_favourite field in serializer + filter endpoint
- TASK-03: Star toggle in TaskCard (optimistic UI)
- TASK-04: FavouritesTab page + route
- TASK-05: Integration tests

Closes #42

## Acceptance criteria

See .aidocs/in-progress/feature-taskapp-favourites/spec.md — all ACs verified.

## Docs

- spec: .aidocs/in-progress/feature-taskapp-favourites/spec.md
- design: .aidocs/in-progress/feature-taskapp-favourites/design.md
EOF
)"
```

After the PR merges, close the feature:

```bash
mv .aidocs/in-progress/feature-taskapp-favourites \
   .aidocs/done/feature-taskapp-favourites
```

## Verify

Run this after the PR is merged and all tasks are in `done/`:

```bash
ls .aidocs/done/feature-taskapp-favourites/done/
```

Expected output: `TASK-01.md  TASK-02.md  TASK-03.md  TASK-04.md  TASK-05.md` — one file per task. If any task file is missing from `done/`, that task was not closed; find it in `todo/` or `in-progress/` and resolve the blocker before calling the feature done.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Claude Code session drifts and implements things not in the task file | Prompt included too much context; LLM over-reached | Restart session with a tighter prompt: "Read only TASK-NN.md. Implement only what is listed there. Stop after committing." |
| TASK-NN.md "What to do" is too vague and the agent asks clarifying questions | Task was written as a goal, not a step-by-step instruction | Rewrite the task with numbered steps and explicit file paths; reference the design.md section that contains the API contract |
| Two tasks with no declared dependency conflict on the same file | Parallelisation assumption was wrong | Add the blocking task as a dependency; run them sequentially |
| Token estimate was too low; session runs out of context mid-task | Task scope underestimated during planning | Split the task into two at the natural boundary (e.g., model + migration as TASK-01a, serializer as TASK-01b); update the plan |
| PR description does not link back to spec | Step 7 prompt was customised and the template was stripped | Always include the spec path and a "Closes #N" reference in the PR body; reviewers need the spec to evaluate acceptance criteria |

## Next

- `sdd-for-solos` — understand the full lifecycle (backlog → todo → in-progress → done) that this pipeline sits inside.
- `writing-first-spec` — if your spec is still weak, tighten it before generating tasks; a vague spec produces vague tasks.

## References

- [knowledge/solo/sdd/sdd/writing-implementation-plans](../../../knowledge/solo/sdd/sdd/writing-implementation-plans) — defines the token-estimate convention and the dependency table format used in Step 2; the `Est. tokens` column in this playbook's plan directly applies those rules.
- [knowledge/solo/sdd/sdd-planning/impl-plan-task-format](../../../knowledge/solo/sdd/sdd-planning/impl-plan-task-format) — specifies the TASK-NN.md file structure (Context, What to do, Acceptance, Files to change, Commit message sections) that Step 3 implements for each task file.
- [knowledge/solo/sdd/sdd-planning/task-creation-principles](../../../knowledge/solo/sdd/sdd-planning/task-creation-principles) — explains why each task must be self-contained enough for an agent to execute without cross-reading other tasks; backs the "agent-readable" constraint enforced in Steps 3 and 5.
