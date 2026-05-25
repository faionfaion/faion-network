---
name: sdd-for-solos
description: Apply lightweight Spec-Driven Development as a solo builder — write spec and a single merged plan.md only when a feature takes a day or more, add conditional user-flows.md / ui-ux-design.md, gate the move to done with readiness.md.
tier: solo
group: sdd-workflow
status: active
owner: ruslan
last_verified: 2026-05-25
version: 2.0.0
---

## Goal

After this playbook you will have a repeatable solo SDD habit: every feature that takes one or more days gets three focused documents (`spec.md`, `design.md`, `plan.md`) under `.aidocs/<feature-slug>/`, moves through a four-state lifecycle, and closes with a verifiable done checklist — without the ceremony overhead of team processes.

## Prerequisites

- A project repo with a `.aidocs/` directory at the root (create it if absent: `mkdir -p .aidocs`).
- Git installed and the repo initialised (`git init` or already tracking a remote).
- Familiarity with Markdown editing (any editor — VS Code, Vim, Obsidian).
- A rough feature idea that you estimate will touch code across more than one session (≥1 day of focused work). If the change is a one-liner or a trivial config tweak, skip SDD entirely and commit directly.

## Steps

### Step 1 — Decide whether SDD applies

Ask two questions:

1. Will this change take more than one focused work session to complete?
2. Will it affect multiple files or introduce a new user-facing behaviour?

If both answers are yes → apply SDD. If either is no → commit directly, no docs needed.

This threshold keeps the process lean: a small bug fix or single-component change ships without ceremony. A new billing page, auth flow, or background job qualifies.

### Step 2 — Create the feature folder in backlog

```bash
FEATURE=feature-$(date +%Y%m%d)-<short-slug>
mkdir -p .aidocs/$FEATURE/todo
mkdir -p .aidocs/$FEATURE/in-progress
mkdir -p .aidocs/$FEATURE/done
```

Replace `<short-slug>` with a kebab-case name for the feature, e.g. `stripe-webhook-handler` or `user-profile-page`.

The folder lives in `.aidocs/` (not committed to source unless your team shares this repo). Add `.aidocs/` to `.gitignore` if you keep SDD docs local, or track them if you want a permanent audit trail.

### Step 3 — Write spec.md (what to build)

Create `.aidocs/$FEATURE/spec.md` with three sections:

```markdown
# spec: <feature name>

## Problem
One paragraph. What pain does this solve and for whom?

## Acceptance criteria
- [ ] AC-01: <observable outcome>
- [ ] AC-02: <observable outcome>
(3–7 criteria; each checkable by running the app or reading a file)

## Out of scope
- Anything you are explicitly NOT building now.
```

Keep it under one page. The spec answers "what done looks like", not "how to build it". If you cannot write three acceptance criteria, the feature is not yet scoped — keep it in backlog until it is.

### Step 4 — Write plan.md (one file, two H2 sections)

Create `.aidocs/$FEATURE/plan.md` with TWO top-level sections:

```markdown
# plan: <feature name>

## Design

### Approach
Two sentences: the core technical decision and why you chose it over alternatives.

### Data / API contract
Table or list: new fields, endpoints, or events this feature introduces. Feature-scoped contracts only; system-wide contracts belong in project-spec/.

### Key files
| File | Change |
|------|--------|
| src/... | add / modify / delete |

### Risks
- <anything that could go wrong and how you'll handle it>

## Execution Plan

### Tasks
| ID | Description | Deps | Est. tokens |
|----|-------------|------|-------------|
| T-01 | <first concrete task> | — | ~3k |
| T-02 | <second task>         | T-01 | ~2k |
| T-03 | <third task>          | T-01 | ~4k |

### Build order
T-01 → T-02 → T-03
```

ONE file, TWO H2 sections. Old `design.md` + `implementation-plan.md` split is gone — they drifted in practice. Aim 80–150 lines total. Skip plan.md entirely if the feature is ≤3 tasks AND introduces no new contract; the spec.md checkbox list is enough.

### Step 4a — Write user-flows.md (conditional)

ONLY if the feature has a user-facing flow (page, form, button, command):

Create `.aidocs/$FEATURE/user-flows.md` documenting each flow as actor + preconditions + happy path + negative paths. Each flow MUST have at least one positive AND one negative Playwright case. Skip entirely for backend-only / API-only / data work — those go through API tests in `tests/api/`.

### Step 4b — Write ui-ux-design.md (conditional)

ONLY if the feature touches UI (web, mobile, CLI TUI):

Create `.aidocs/$FEATURE/ui-ux-design.md` with sections Intent, Layout, States (empty / loading / error / success / disabled), Nielsen 5 audit (visibility, control, consistency, error prevention, recognition), Norman 2 audit (affordance, feedback), Copy & microcopy. Skip for pure backend / data / API features.

### Step 5 — Move the feature to in-progress

When you are ready to start:

```bash
# Feature becomes active
mv .aidocs/$FEATURE .aidocs/in-progress/$FEATURE
```

As you work through each task, move individual task files (or check them off in `plan.md`). When a task is complete, commit its changes with a message referencing the task ID:

```bash
git add src/stripe/webhook.py
git commit -m "feat(F-NN-T01): add webhook signature verification"
```

### Step 6 — Fill readiness.md before moving to done

Before you mark the feature done, create `.aidocs/in-progress/$FEATURE/readiness.md` and tick all 10 items with evidence (per `readiness-checklist` methodology):

1. All ACs from spec.md have evidence (test id or screenshot reference).
2. tasks/todo/ and tasks/in-progress/ are empty.
3. Commits granular, `type(F-NN-T0N): ...` shape, no Co-Authored-By, no emoji.
4. CI green (lint + typecheck + unit).
5. API tests pass — if backend touched.
6. Playwright pos+neg pass — if user-facing flow.
7. ui-ux-design.md heuristics reviewed — if UI touched.
8. project-spec/ delta drafted OR "no spec impact" with reason.
9. Surface coupling reviewed (skill triggers, API paths, CLI flags).
10. Deployed to the host listed in project-spec/deploy.md.

Any unticked item BLOCKS the move to done/. The list is short on purpose — copy-paste it into readiness.md verbatim.

### Step 7 — Close the feature

When all 10 readiness items are ticked:

```bash
mv .aidocs/in-progress/$FEATURE .aidocs/done/$FEATURE
```

Add a one-line summary to your `CHANGELOG.md` under `## [Unreleased]`:

```
- feat: stripe-webhook-handler — signature verification + idempotency
```

No retro, no ceremony. The done/ folder is your audit trail.

## CR / BUG flow

Not every change is a feature. For one-off mutations or defects use the side-streams instead — `crs/{todo,done}/CR0NN-slug.md` and `bugs/{todo,in-progress,done}/BUG0NN-slug.md`. Numbering is global per repo, separate counters. Commit prefixes: `cr(CR0NN): ...` and `fix(BUG0NN): ...`. A BUG that exposes a missing business rule MUST update `project-spec/business-rules.md` in the same PR. Full shape in the `cr-bug-tracking` methodology.

## Verify

Open `.aidocs/done/$FEATURE/` and confirm:

```bash
# All ACs ticked in spec.md
grep -c '\- \[x\]' .aidocs/done/$FEATURE/spec.md

# All 10 readiness items ticked in readiness.md
grep -c '\- \[x\]' .aidocs/done/$FEATURE/readiness.md
```

The spec count must equal the number of acceptance criteria you wrote in Step 3. The readiness count must equal 10 (some items may resolve to "n/a with reason" — those count as ticked when justified). If any are unchecked, the feature is not done — move it back to `in-progress/`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `spec.md` has acceptance criteria you cannot test | Criteria written as internal implementation details, not observable outcomes | Rewrite as: "user can do X" or "endpoint returns Y with status Z" — something you can verify by running the app |
| Feature folder grows past 10 tasks and feels unmanageable | Feature scope is too large for solo SDD | Split into two feature folders; the first closes a shippable slice, the second captures the remainder in backlog |
| You skip SDD on a "small" change, then spend two sessions debugging scope creep | Threshold calibration too loose | For recurring problem areas (auth, payments, data migrations), lower your personal threshold to "more than 30 minutes" |
| Plan diverges from spec mid-build: new tasks appear that weren't in plan.md | Discovery work uncovered hidden complexity | Add tasks to plan.md in real time; SDD is a living document, not a contract |

## Next

- `writing-first-spec` — go deeper on writing acceptance criteria that are testable and unambiguous.
- `scope-cutting` — when features grow, use this playbook to make principled cuts before they derail your schedule.
- `roadmap-for-one-person` — once multiple features accumulate in backlog, use this playbook to sequence them into a coherent roadmap.

## References

- [knowledge/sdd/sdd-workflow-overview](../../../../knowledge/sdd/sdd-workflow-overview) — defines the five-phase lifecycle (spec → plan → tasks → readiness → done); Steps 1, 2, 5, 6, 7 map to those phases.
- [knowledge/sdd/plan-md-structure](../../../../knowledge/sdd/plan-md-structure) — the merged plan.md (two H2 sections) template used in Step 4.
- [knowledge/sdd/readiness-checklist](../../../../knowledge/sdd/readiness-checklist) — canonical 10-item readiness.md used in Step 6.
- [knowledge/sdd/project-spec-structure](../../../../knowledge/sdd/project-spec-structure) — the per-project source-of-truth folder referenced in Step 6 (item 8) and the CR/BUG flow.
- [knowledge/sdd/cr-bug-tracking](../../../../knowledge/sdd/cr-bug-tracking) — CR / BUG side-streams parallel to the feature lifecycle.
- [knowledge/sdd/spec-requirements](../../../../knowledge/sdd/spec-requirements) — acceptance-criteria schema (observable, checkable) used in Step 3.
