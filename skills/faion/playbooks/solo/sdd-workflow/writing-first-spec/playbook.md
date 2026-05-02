---
name: writing-first-spec
description: Turn a one-line feature idea into a complete spec.md with Goal, Non-Goals, Functional Requirements, and Acceptance Criteria.
tier: solo
group: sdd-workflow
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `spec.md` that fully describes one feature — its Goal, Non-Goals, numbered Functional Requirements (F1-Fn), and Acceptance Criteria (AC1-ACn) — ready to hand to an implementation agent or a developer without further clarification.

## Prerequisites

- A one-line description of the feature you want to build (rough is fine).
- A project repo with an `.aidocs/` directory or any folder where you keep design docs.
- Familiarity with Markdown; no special tooling required.
- Optional: faion-cli installed (`pip install faion-cli`) to run SDD scaffolding commands.

## Steps

1. **Write the one-liner in plain English.** Start from the raw idea, for example: "Add favourites to TaskApp so users can star tasks and view them in a dedicated list."

2. **Create the spec file.** In your project, create `docs/specs/taskapp-favourites.md` (or `.aidocs/in-progress/feature-taskapp-favourites/spec.md` if you follow the SDD lifecycle).

3. **Write the Goal section.** One sentence: what problem does this solve for whom?

   ```
   ## Goal
   Allow TaskApp users to mark any task as a favourite and access their starred
   tasks from a persistent "Favourites" tab, reducing time spent re-finding
   high-priority items.
   ```

4. **Write the Non-Goals section.** List what is explicitly out of scope to prevent scope creep during review.

   ```
   ## Non-Goals
   - Sharing favourites between users or team workspaces.
   - Sorting or grouping within the Favourites tab (phase 2).
   - Syncing favourites across devices (handled separately by offline-sync feature).
   ```

5. **Write Functional Requirements (F1-Fn).** Number each requirement. Use "The system shall" for system behaviour and "The user can" for user actions. Keep each requirement atomic — one behaviour per line.

   ```
   ## Functional Requirements
   F1. The user can toggle the favourite state of any task by clicking a star icon.
   F2. The system shall persist favourite state across page reloads and sessions.
   F3. The system shall display a "Favourites" tab in the main navigation.
   F4. The Favourites tab shall list all starred tasks in reverse-favourited order.
   F5. The system shall update the Favourites tab in real time when a star is toggled.
   F6. The user can un-favourite a task from either the task list or the Favourites tab.
   ```

6. **Write Acceptance Criteria (AC1-ACn).** Each AC maps to one or more FRs and is written as a testable Given/When/Then statement. Number them to match reviewers' references.

   ```
   ## Acceptance Criteria
   AC1. Given a logged-in user, when they click the star on any task, then the
        star icon toggles to filled and the task appears in Favourites tab within
        500ms — covers F1, F2, F5.
   AC2. Given a user with 3 starred tasks, when they reload the page, then all 3
        tasks remain starred and the Favourites tab count shows 3 — covers F2.
   AC3. Given the Favourites tab is open, when the user un-stars a task from the
        main list, then that task disappears from Favourites tab without a page
        reload — covers F5, F6.
   AC4. Given a user with no starred tasks, when they open the Favourites tab,
        then they see an empty state message "No favourites yet. Star a task to
        save it here." — covers F3, F4.
   ```

7. **Add a Context section (optional but recommended).** One paragraph on why now, any constraints (API limits, browser support), and any open questions to resolve before implementation starts.

   ```
   ## Context
   TaskApp v2.3 uses a Django REST backend and a React 18 SPA. The task model
   has a `favourited_by` many-to-many field already planned in the schema but not
   yet exposed. Open question: should favourites be per-device (localStorage) or
   per-account (server-side)? Decision needed before F2 implementation.
   ```

8. **Review against the quality bar.** Read every requirement and ask: (a) Is it testable? (b) Does it have a corresponding AC? (c) Is there anything a developer could misinterpret? Revise until all answers are yes.

## Verify

Open the spec file and confirm each of the following is present and non-empty:

```
grep -c "^## " docs/specs/taskapp-favourites.md
```

Expected output: at least `4` (Goal, Non-Goals, Functional Requirements, Acceptance Criteria). Then verify every `F[0-9]` has a corresponding `AC` that mentions it:

```
grep "F[0-9]" docs/specs/taskapp-favourites.md
```

Each functional requirement number (F1, F2, …) should appear both in the requirements list and in at least one AC line.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| ACs reference requirements not in the spec | FRs were added to the AC section without being listed in Functional Requirements | Audit each AC line; for every `covers Fn` reference, confirm `Fn.` exists in the Functional Requirements section |
| Requirements keep growing during review | The Goal is too broad — it allows many different features | Rewrite the Goal to name one specific user action and one specific outcome; move everything else to a separate spec |
| Developer asks "what exactly should happen when X?" | AC is written as a behaviour assertion without a trigger condition | Rewrite as Given/When/Then; the Given captures preconditions, When captures the trigger, Then captures the observable outcome |
| Non-Goals section is empty | Author skipped it thinking "obvious" | Always write at least 2 non-goals; they are scope anchors for implementation and review, not optional metadata |

## Next

- `sdd-for-solos` — apply the full SDD lifecycle (spec → design → implementation-plan → tasks) to the spec you just wrote.
- `scope-cutting` — when your requirements list exceeds 8 items, use this playbook to cut to an MVP set before planning starts.

## References

- [knowledge/solo/sdd/sdd-planning/writing-specifications](../../../knowledge/solo/sdd/sdd-planning/writing-specifications) — provides the canonical SDD spec structure (Goal, Non-Goals, FRs, ACs) that Steps 3-6 directly implement, including the numbering convention used in this playbook.
- [knowledge/solo/sdd/sdd-planning/spec-structure](../../../knowledge/solo/sdd/sdd-planning/spec-structure) — defines the internal section ordering and field-level rules (atomic requirements, Given/When/Then ACs) applied in Steps 5-6 and the Verify check.
