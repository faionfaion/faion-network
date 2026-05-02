---
name: roadmap-for-one-person
description: Build and maintain a one-page roadmap.md with Now/Next/Later columns that keeps you focused on outcomes, not features.
tier: solo
group: product-planning
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a `roadmap.md` file in your repo root with three columns (Now / Next / Later), no more than three items in Now, every item expressed as a measurable outcome, and a weekly review habit that keeps the file honest.

## Prerequisites

- A running product (any stage — even pre-launch) with at least one paying or active user.
- Git repo where you can commit a Markdown file.
- 30 minutes of uninterrupted thinking time for the first draft.
- Optional but useful: basic analytics (Plausible, Mixpanel, or even Stripe MRR dashboard) so you can state outcomes numerically.

## Steps

1. **Create the file** at the root of your repo.

   ```bash
   touch roadmap.md
   git add roadmap.md
   ```

2. **Write the three-column skeleton** in `roadmap.md`.

   ```markdown
   # Roadmap

   > Outcomes over features. Reviewed every Monday.

   ## Now (max 3)

   | Outcome | Signal | Status |
   |---------|--------|--------|
   | | | |

   ## Next

   | Outcome | Signal | Notes |
   |---------|--------|-------|
   | | | |

   ## Later

   | Outcome | Notes |
   |---------|-------|
   | | |
   ```

3. **Fill Now with your top three outcomes.** An outcome answers "what changes for the user or the business?" — not "what do I build?". Use the table below as a guide.

   | Wrong (feature) | Right (outcome) |
   |-----------------|-----------------|
   | Add billing portal | Increase trial→paid conversion by 5 pp |
   | Rebuild onboarding flow | Cut time-to-first-value from 8 min to 3 min |
   | Add CSV export | Retain 10 accounts that cited missing export as churn reason |

   **Real example — hypothetical SaaS `notionform.io` (form builder for Notion):**

   | Outcome | Signal | Status |
   |---------|--------|--------|
   | Increase trial→paid conversion by 5 pp (target: 18%) | Stripe conversion rate | In progress |
   | Reduce first-form publish time to under 90 s | Amplitude median event gap | Planned |
   | Reach 50 active paying workspaces | Stripe active subscriptions | Planned |

4. **Fill Next (3–6 items)** with outcomes that are real but not urgent. These are candidates for Now in 2–4 review cycles.

   Example for `notionform.io`:

   | Outcome | Signal | Notes |
   |---------|--------|-------|
   | Organic signup via SEO: 10 new trials/week | Google Search Console impressions + GA signups | Requires landing page + 3 SEO articles |
   | Add Zapier integration to unblock 8 waitlisted accounts | # activated Zapier connections | Dependency: Zapier review (2–3 weeks) |

5. **Fill Later** with anything that is genuinely valuable but not in the next 60 days. One sentence each.

   ```markdown
   ## Later

   | Outcome | Notes |
   |---------|-------|
   | Launch a public API for power users | Will revisit when MRR > $2k |
   | Support multi-language forms | Requested by 4 users, not a blocker for growth yet |
   ```

6. **Commit the roadmap.**

   ```bash
   git add roadmap.md CHANGELOG.md
   git commit -m "docs: add one-page roadmap"
   ```

7. **Set a weekly review reminder** (pick one channel you actually check).

   - Google Calendar: recurring event every Monday 09:00 "Roadmap review — is Now still right?"
   - Cron job on your laptop that opens the file:
     ```bash
     # crontab -e
     0 9 * * 1 code ~/projects/notionform.io/roadmap.md
     ```
   - Notion reminder if your project notes live there.

8. **Run the weekly review** (takes under 15 minutes).

   - Check each Now item: did the Signal move? If yes, mark done and promote one item from Next.
   - Ask: "Is anything in Now blocked or no longer the top priority?" If yes, demote it to Next and pull the next most important outcome up.
   - Prune Later: if an item has sat there for 3+ months without moving to Next, delete it or archive it in a `roadmap-archive.md`.
   - Commit the update:
     ```bash
     git add roadmap.md
     git commit -m "docs: weekly roadmap update $(date +%Y-%m-%d)"
     ```

## Verify

Open `roadmap.md` and run this mental checklist:

```
[ ] Now has ≤3 rows
[ ] Every Now row has a Signal column with a measurable value (%, count, or time)
[ ] No row in any column reads like a feature ("Add X", "Build Y") without a stated outcome
[ ] File is committed in git
```

For the automated check, confirm the file exists and git tracks it:

```bash
git log --oneline roadmap.md | head -3
```

Output should show at least one commit. If empty, you forgot to commit in Step 6.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Now has 6 items and nothing ships | All items feel equally urgent | Rank by "if I could only ship one thing this week, which moves the most revenue or retention?" — that is Now item 1. Force-limit to 3. |
| Outcomes are vague ("improve UX", "be faster") | No measurement baseline | Add a Signal column; if you cannot state a number, the outcome is not ready for Now — move it to Next until you have data |
| Roadmap drifts: file not updated in 3 weeks | Review habit not anchored to a trigger | Tie review to an existing habit (morning coffee, Monday standup). If using calendar, make it a recurring task, not an event — tasks survive rescheduling |
| Team member (or future co-founder) confused by the format | Too much implicit context | Add a one-paragraph "How to read this" section at the top of `roadmap.md` |
| Now item stuck for 4+ weeks with no Signal movement | Wrong metric, or outcome not in your control | Replace Signal with a leading indicator you can actually move (e.g., "5 user interviews done" instead of "NPS +10") |

## Next

- [writing-first-spec](../sdd-workflow/writing-first-spec) — once an outcome is in Now, write a spec before coding to avoid scope creep.
- [weekly-review-solo](../product-planning/weekly-review-solo) — deeper cadence: combine roadmap review with backlog hygiene and metric check-in.
- [okr-setting methodology](../../../knowledge/solo/product/product-planning/okr-setting) — if your product grows to 2+ people, formalize outcomes into quarterly OKRs.

## References

- [knowledge/solo/product/product-planning/outcome-based-roadmaps](../../../knowledge/solo/product/product-planning/outcome-based-roadmaps) — provides the outcome-vs-feature framing that backs Steps 3 and 4; the "Signal" column in this playbook's tables directly implements the measurability rule from that methodology.
- [knowledge/solo/product/product-planning/roadmap-design](../../../knowledge/solo/product/product-planning/roadmap-design) — covers Now/Next/Later column semantics and the max-3-in-Now constraint applied in Step 2 and Step 8.
- [knowledge/solo/product/product-planning/release-planning](../../../knowledge/solo/product/product-planning/release-planning) — informs the weekly promotion/demotion logic in Step 8: when a Now item completes, how to pull the right Next item up without disrupting flow.
