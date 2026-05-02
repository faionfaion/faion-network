---
name: weekly-review-solo
description: Run a 30-minute Friday ritual that syncs roadmap.md, checks 5 key metrics, drafts next-week priorities, archives done items, and surfaces one blocker.
tier: solo
group: product-planning
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a repeatable 30-minute Friday ritual that checks your five core health metrics (signups, MRR, churn, active users, incidents), updates your `roadmap.md` Now column, archives done items, writes a `weekly-plan.md` entry for the coming week, and surfaces one explicit blocker — keeping your product moving without drift.

## Prerequisites

- A `roadmap.md` file in your repo root with Now/Next/Later columns (see [roadmap-for-one-person](../product-planning/roadmap-for-one-person)).
- At least one analytics source you can check in under 5 minutes: Stripe dashboard for MRR/signups/churn, Plausible or PostHog for active users, GitHub Issues or your own error logs for incidents.
- A `weekly-plan.md` file at repo root (or create it in Step 3 below).
- A `weekly-review-template.md` copied into your repo (template provided in Step 2).
- Git repo with write access so you can commit the review result.

## Steps

1. **Copy the review template into your repo.**

   Create `weekly-review-template.md` at your repo root with this content (copy once; re-use every Friday):

   ```markdown
   # Weekly Review — <YYYY-MM-DD>

   ## Metrics snapshot

   | Metric | Last week | This week | Delta |
   |--------|-----------|-----------|-------|
   | Signups (trial starts) | | | |
   | MRR ($) | | | |
   | Churn (cancelled this week) | | | |
   | Active users (7-day) | | | |
   | Incidents (bugs/outages logged) | | | |

   ## Roadmap Now — status check

   <!-- Copy rows from roadmap.md Now column and update Status + Signal -->
   | Outcome | Signal | Status | Action |
   |---------|--------|--------|--------|
   | | | | |

   ## Done this week

   <!-- Items completed — will be archived from roadmap.md -->
   -

   ## Next-week plan (max 3 focus items)

   1.
   2.
   3.

   ## One blocker

   > Blocker: <description>
   > Owner: <you / external / unknown>
   > Next action: <what you will do by end of Monday>
   ```

   Commit the template:

   ```bash
   git add weekly-review-template.md
   git commit -m "docs: add weekly-review-template.md"
   ```

2. **Open your analytics sources (5 minutes).**

   Pull the five numbers before filling anything:

   - **Signups:** Stripe → Customers → filter "created this week" or PostHog → Persons → date range.
   - **MRR:** Stripe → Revenue → Monthly Recurring Revenue tile, or `stripe revenue mrr` in the Stripe CLI:
     ```bash
     stripe customers list --limit 100 | python3 -c "import sys,json; data=json.load(sys.stdin); print(len(data['data']), 'customers')"
     ```
     (For quick MRR, use Stripe Dashboard directly — CLI MRR calculation requires the `billing` API.)
   - **Churn:** Stripe → Subscriptions → filter "canceled" + this week date range.
   - **Active users:** Plausible → `plausible.io/<your-domain>` → Unique Visitors → last 7 days. Or PostHog → Insights → Active users (7-day).
   - **Incidents:** count open GitHub Issues labeled `bug` or `incident` created this week:
     ```bash
     gh issue list --label bug --state open --created ">=<YYYY-MM-DD>" --repo <owner>/<repo>
     ```

3. **Fill the weekly-review-template.md copy for this week.**

   Copy `weekly-review-template.md` to `weekly-plan.md` (or append a new dated section to it):

   ```bash
   cp weekly-review-template.md weekly-plan.md
   # Then edit weekly-plan.md with this week's date and numbers.
   ```

   Fill in the Metrics snapshot table with the numbers from Step 2. Be exact — no estimates.

4. **Update `roadmap.md` Now column.**

   Open `roadmap.md`. For each row in Now:

   - If Signal moved to target → mark `Status: Done`. Add item to "Done this week" in your review file.
   - If Signal moved but target not reached → mark `Status: In progress`. Note the delta.
   - If Signal did not move and you worked on it → check for a blocker. Add to "One blocker" section.
   - If item is no longer top priority → move it back to Next.

   Promote one item from Next into Now for each Done item, keeping Now at ≤3 rows.

5. **Archive done items from `roadmap.md`.**

   Move completed Now rows to `roadmap-archive.md` (create if absent):

   ```bash
   # roadmap-archive.md format:
   ## Archived — <YYYY-MM-DD>
   | Outcome | Signal | Completed |
   |---------|--------|-----------|
   | Increase trial→paid by 5 pp | Stripe: 18% → 23% | 2026-05-02 |
   ```

   Delete done rows from `roadmap.md` Now table.

6. **Write next-week plan (3 focus items max).**

   In `weekly-plan.md`, fill "Next-week plan". Each item must be:
   - One concrete deliverable (not a vague intent).
   - Tied to a Now outcome from `roadmap.md`.
   - Actionable by you alone (if it depends on someone else, note that and handle in One Blocker).

   Example for a form-builder SaaS `notionform.io`:
   ```
   1. Ship billing portal (Stripe Customer Portal) — targets trial→paid conversion Now item.
   2. Publish 2 SEO articles drafted last week — targets organic-signup Now item.
   3. Interview 2 churned users from this week's churn — feeds retention data.
   ```

7. **Surface one blocker explicitly.**

   Name exactly one blocker (the highest-risk thing that could derail next week). Assign an owner and a next action due by end of Monday:

   ```markdown
   ## One blocker
   > Blocker: Stripe Customer Portal redirect URL not working in staging.
   > Owner: me
   > Next action: Check Stripe docs on allowed return_url domains, fix by Monday EOD.
   ```

   If there is genuinely no blocker, write:
   ```markdown
   ## One blocker
   > Blocker: None. All three focus items are unblocked.
   ```

8. **Commit the review.**

   ```bash
   git add roadmap.md roadmap-archive.md weekly-plan.md CHANGELOG.md
   git commit -m "docs: weekly review $(date +%Y-%m-%d)"
   ```

9. **Set the recurring reminder** (do this once).

   Pick one method you will actually check:

   - Google Calendar: recurring event every Friday 16:30 "30-min weekly review".
   - Cron job that opens `roadmap.md` and `weekly-plan.md`:
     ```bash
     # crontab -e  (runs Friday at 16:30)
     30 16 * * 5 code ~/projects/notionform.io/roadmap.md ~/projects/notionform.io/weekly-plan.md
     ```
   - Telegram reminder via NERO (if you use NERO): `tg-send "Weekly review time — check roadmap.md and metrics."` wrapped in a cron.

## Verify

After the review, run:

```bash
git log --oneline roadmap.md weekly-plan.md | head -3
```

Confirm the top commit is today's review commit. Then open `roadmap.md` and verify:

```
[ ] Now has ≤3 rows
[ ] Each Now row has an updated Status (not blank)
[ ] weekly-plan.md contains exactly 3 focus items for next week
[ ] "One blocker" section is filled (not blank)
[ ] Done items are absent from roadmap.md Now (they moved to roadmap-archive.md)
```

If `git log` shows no commit from today for these files, the review was not committed — re-run Step 8.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Review takes 90+ minutes, not 30 | Scope creep — trying to refine strategy or fix issues during review | Review is read-only + plan-only. Capture issues as next-week action items; fix nothing during the review slot itself |
| Metrics numbers are not accessible in 5 minutes | No bookmarked dashboard, CLI auth expired | Bookmark Stripe dashboard and Plausible/PostHog directly; keep `gh auth login` token fresh (`gh auth status`). Prep links in a pinned browser tab on Friday morning |
| `roadmap.md` Now has 6 items — unclear what to promote/demote | Items accumulated without weekly pruning | Force-rank the 6 items: "which single item, if shipped, most directly moves MRR or retention?" — that is item 1. Demote items 4-6 to Next immediately |
| "Done this week" is always empty | Work is fragmented across many small tasks with no outcome tracking | Map each task to a Now outcome in `roadmap.md`. If a task does not connect to any Now outcome, it should not have been done — add it to Later or drop it |
| Blocker carries forward unchanged for 3+ weeks | Owner or next action is vague | Rewrite blocker with a specific next action that resolves a sub-problem this week, not the whole blocker. If the owner is external, escalate or find an alternative path |
| `roadmap-archive.md` does not exist | First time running Step 5 | Create it: `touch roadmap-archive.md`, add the header line, then move done rows in |

## Next

- [roadmap-for-one-person](../product-planning/roadmap-for-one-person) — build the `roadmap.md` file this review ritual relies on, if you have not yet.
- [backlog-hygiene](../product-ops/backlog-hygiene) — extend the Friday ritual with a 10-minute backlog pass to keep your issue tracker actionable alongside the roadmap.

## References

- [knowledge/solo/product/product-planning/roadmap-design](../../../knowledge/solo/product/product-planning/roadmap-design) — the Now/Next/Later column semantics and max-3-in-Now constraint are applied directly in Steps 4 and 5; this methodology defines when to promote items from Next.
- [knowledge/solo/product/product-operations/product-analytics](../../../knowledge/solo/product/product-operations/product-analytics) — the five-metric snapshot (signups, MRR, churn, active users, incidents) in Step 2 applies the AARRR coverage model from this methodology, mapping Acquisition → signups, Revenue → MRR/churn, Engagement → active users.
- [knowledge/solo/product/product-operations/backlog-management](../../../knowledge/solo/product/product-operations/backlog-management) — the "archive done items" pattern in Step 5 and the max-3 focus-items constraint in Step 6 implement the DEEP principle's "Prioritized" rule: only ready, outcome-linked items stay in the active view.
