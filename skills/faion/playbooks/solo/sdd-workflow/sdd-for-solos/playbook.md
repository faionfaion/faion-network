---
name: sdd-for-solos
description: Apply lightweight Spec-Driven Development as a solo builder — create spec, design, and plan only when a feature takes a day or more, then move it through backlog → todo → in-progress → done.
tier: solo
group: sdd-workflow
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
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

### Step 4 — Write design.md (how to build it)

Create `.aidocs/$FEATURE/design.md`:

```markdown
# design: <feature name>

## Approach
Two sentences: the core technical decision and why you chose it over alternatives.

## Data / API contract
Table or list: new fields, endpoints, or events this feature introduces.

## Key files
| File | Change |
|------|--------|
| src/... | add / modify / delete |

## Risks
- <anything that could go wrong and how you'll handle it>
```

Aim for 30–60 lines. Diagrams are optional; plain text tables work fine. The design doc is your future-self's memory — write what will be non-obvious in three months.

### Step 5 — Write plan.md (task breakdown)

Create `.aidocs/$FEATURE/todo/plan.md`:

```markdown
# plan: <feature name>

## Tasks
| ID | Description | Deps |
|----|-------------|------|
| T-01 | <first concrete task> | — |
| T-02 | <second task> | T-01 |
| T-03 | <third task> | T-01 |

## Build order
T-01 → T-02 → T-03
```

Each task should be a unit of work you can complete and commit in one sitting. Three to seven tasks covers most solo features. If you have more than ten, split the feature.

### Step 6 — Move the feature to todo, then in-progress

When you are ready to start:

```bash
# Feature becomes active
mv .aidocs/$FEATURE .aidocs/in-progress/$FEATURE
```

As you work through each task, move individual task files (or check them off in `plan.md`). When a task is complete, commit its changes with a message referencing the task ID:

```bash
git add src/stripe/webhook.py
git commit -m "feat(T-01): add webhook signature verification"
```

### Step 7 — Close the feature

When all acceptance criteria in `spec.md` are checked and all tasks in `plan.md` are done:

```bash
mv .aidocs/in-progress/$FEATURE .aidocs/done/$FEATURE
```

Add a one-line summary to your `CHANGELOG.md` under `## [Unreleased]`:

```
- feat: stripe-webhook-handler — signature verification + idempotency
```

No retro, no ceremony. The done/ folder is your audit trail.

## Verify

Open `.aidocs/done/` and confirm the feature folder contains `spec.md` with all acceptance criteria checked:

```bash
grep -c '\- \[x\]' .aidocs/done/$FEATURE/spec.md
```

The count must equal the number of acceptance criteria you wrote in Step 3. If any remain unchecked, the feature is not done — move it back to `in-progress/`.

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

- [knowledge/solo/sdd/sdd/sdd-workflow-overview](../../../knowledge/solo/sdd/sdd/sdd-workflow-overview) — defines the four-state lifecycle (backlog → todo → in-progress → done) and the one-day threshold that determines when SDD applies; Steps 1, 2, and 7 in this playbook map directly to that lifecycle model.
- [knowledge/solo/sdd/sdd-planning/spec-requirements](../../../knowledge/solo/sdd/sdd-planning/spec-requirements) — provides the acceptance-criteria schema (observable, checkable, user-facing) used in Step 3; the three-section spec template above is a minimal adaptation of that schema for a solo context.
- [knowledge/solo/sdd/sdd-planning/impl-plan-components](../../../knowledge/solo/sdd/sdd-planning/impl-plan-components) — defines task granularity rules (one sitting = one commit) and the dependency table format used in Step 5; the plan.md template in this playbook is a stripped-down version of that component model.
