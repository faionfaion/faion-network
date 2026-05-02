---
name: mvp-scope-cutting
description: Reduce a 30-item MVP feature list to ≤5 shippable items using the must-have / nice-to-have / cut elimination algorithm.
tier: free
group: mvp-essentials
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a feature list trimmed to ≤5 items that are necessary and sufficient to validate your single core hypothesis, a written record of every cut item and the reason it was cut, and a ship date derived from honest capacity math rather than optimism.

## Prerequisites

- A written list of features you plan to build (any format: Notion doc, spreadsheet, sticky notes — does not matter yet).
- A clear one-sentence statement of the core problem you are solving (write it down before starting; if you cannot write it, do that first).
- Rough knowledge of your weekly available build hours (even an estimate like "10 hours/week on weekends" is sufficient).
- No prior product-management experience required.

## Steps

### Step 1 — Write every feature on its own row

Open a spreadsheet or a plain text file. Put each feature on a separate line. Do not group or filter yet. If your list has 30 items, you should have 30 rows.

Example starting list for **TaskApp** (a simple task manager for freelancers):

```
1.  User registration and login
2.  Task creation with title and due date
3.  Task completion toggle
4.  Project folders
5.  Recurring tasks
6.  Time tracking per task
7.  Invoicing from time logs
8.  Client portal (read-only view)
9.  Calendar sync (Google + Apple)
10. Mobile app (iOS)
11. Mobile app (Android)
12. Email reminders for due tasks
13. Drag-and-drop task ordering
14. Task tags and filters
15. Team member invitations
16. Per-task comments
17. File attachments
18. Reporting dashboard (hours by project)
19. CSV export
20. Zapier integration
21. Slack notifications
22. Dark mode
23. Keyboard shortcuts
24. Offline mode
25. Sub-tasks
26. Priority levels (urgent/normal/low)
27. Custom task statuses
28. Public task-sharing link
29. Onboarding checklist for new users
30. Two-factor authentication
```

### Step 2 — Label each feature M / N / C

Add a second column. Label each row with exactly one letter:

- **M** (Must-have) — Without this, a user cannot perform the single job the product is supposed to do. The product does not work at all without it.
- **N** (Nice-to-have) — Improves experience but the core job still works without it.
- **C** (Cut) — Out of scope for launch. Could be a V2 idea, a different product entirely, or a feature that implies a different audience.

Rules for assigning M:
1. Write your core job statement at the top of the sheet: "TaskApp lets a freelancer track what they owe clients and get paid."
2. Read each feature. Ask: "If I remove this, can a freelancer still track tasks and get paid?" If yes → N or C. If no → M.
3. Treat team/collaboration features as C unless your hypothesis explicitly requires multiple users to test.

Example labels for TaskApp:

```
1.  User registration and login         M
2.  Task creation with title/due date   M
3.  Task completion toggle              M
4.  Project folders                     N
5.  Recurring tasks                     N
6.  Time tracking per task              M
7.  Invoicing from time logs            M
8.  Client portal                       C
9.  Calendar sync                       C
10. Mobile app (iOS)                    C
11. Mobile app (Android)                C
12. Email reminders                     N
13. Drag-and-drop ordering              N
14. Tags and filters                    N
15. Team member invitations             C
16. Per-task comments                   C
17. File attachments                    C
18. Reporting dashboard                 N
19. CSV export                          N
20. Zapier integration                  C
21. Slack notifications                 C
22. Dark mode                           C
23. Keyboard shortcuts                  C
24. Offline mode                        C
25. Sub-tasks                           N
26. Priority levels                     N
27. Custom task statuses                N
28. Public task-sharing link            C
29. Onboarding checklist                N
30. Two-factor authentication           N
```

Result: 5 M items, 11 N items, 14 C items.

### Step 3 — Verify M count is ≤5; if not, apply the time-budget filter

Count your M items. If you have ≤5, skip to Step 4.

If you have more than 5 M items, apply the time-budget reverse-engineering filter:

1. Estimate your capacity: `weekly_hours × weeks_until_you_need_users = total_build_hours`. Example: 10 hours/week × 8 weeks = 80 hours.
2. Estimate build hours for each M item (rough: simple form = 4h, CRUD list = 8h, payment integration = 16h, auth = 8h).
3. Sum the M items. If the total exceeds `total_build_hours × 0.6` (leave 40% for bugs and integration), you have too many M items.
4. For each M item over budget, ask: "Is there a version of this feature that takes 80% less time?" If yes, scope it down and keep it. If no, move it to N.

Example: if TaskApp had added "invoicing with Stripe" (16h) and "PDF invoice download" (12h) as separate M items, the total would be 5+16+12 = 33h — within 80h×0.6 = 48h budget, so both stay.

### Step 4 — Record every cut and its reason

For every C item, write one sentence explaining why it was cut. This is not bureaucracy — it prevents scope creep from re-entering through "but we already discussed this" conversations.

Paste this block below your table:

```
CUT LIST — TaskApp MVP
8.  Client portal — requires multi-user auth; different product category
9.  Calendar sync — API integration doubles build time; no evidence users need it at signup
10. Mobile app (iOS) — web-responsive is sufficient to test the core hypothesis
11. Mobile app (Android) — same as iOS
15. Team invitations — MVP hypothesis is solo freelancer, not team
...
```

### Step 5 — Write the ≤5 M items as your ship definition

Copy only the M items into a new section titled "MVP = done when:". Phrase each as a user action, not a feature name:

```
MVP = done when:
1. A freelancer can create an account and log in.
2. A freelancer can create a task with a title and due date.
3. A freelancer can mark a task complete.
4. A freelancer can log time against a task.
5. A freelancer can generate and send an invoice from logged time.
```

This list is your launch gate. When all 5 are working end-to-end, you ship and talk to users — even if the UI is rough.

## Verify

Open your final "MVP = done when:" list and check each of the following:

1. Count the items — must be ≤5.
2. Read the core job statement you wrote in Step 2. For each item, ask "does removing this break the job?" All must answer yes.
3. Scan the CUT LIST — every feature not in the MVP must appear there with a written reason.
4. Multiply your estimated hours per M item and confirm the total is within `total_build_hours × 0.6`.

If all four pass, your MVP scope is valid. If any fail, return to Step 3 and cut further.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Every feature feels like M | Core job statement is too broad ("an app that helps freelancers") | Rewrite the core job as a single, narrow action: "lets a freelancer create and send one invoice" — then re-label |
| M list passes Step 3 but build takes 3× longer than estimated | Hour estimates were optimistic; integration glue was not counted | Re-estimate each M item by breaking it into subtasks (design, backend, frontend, testing) and summing; add 30% for unknown unknowns |
| Stakeholder or co-founder insists a C item is actually M | Feature preference disguised as necessity | Ask: "Can a user complete the core job without this feature on day 1?" If yes, it is not M; document the disagreement in the CUT LIST |
| After cutting to 5, the product feels embarrassingly simple | Good — this is the goal | Write down the feeling; it means you have correctly eliminated scope. Ship it and let users tell you what is actually missing |
| Two features look like M but together exceed time budget | Both are real requirements but the sequence matters | Ship the first M item that unblocks user testing; defer the second to V1.1 |

## Next

- `ugly-first-version` — start building your 5 M items with the ugliest viable implementation before polishing anything.
- `mvp-launch-checklist` — a gate-by-gate checklist to run before calling your MVP live.
- Once your MVP is live and you have 10+ users, revisit the CUT LIST to decide which N items to promote to the next sprint.

## References

- [knowledge/free/dev/code-quality/code-decomposition-principles](../../../knowledge/free/dev/code-quality/code-decomposition-principles) — the single-responsibility constraint applied to source files (one file, one job; split when it grows too large) is the same discipline applied here to product scope: one MVP, one job; cut every feature that does not serve that job directly.
