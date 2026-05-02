---
name: rice-ice-prioritization
description: Score your backlog with ICE or RICE, write explicit assumptions, and pick the top 2 items for your next sprint.
tier: solo
group: product-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a scored, sorted backlog in your `tasks.md` file, a written-down assumption log for every score, and exactly two items committed to your next sprint — chosen by number, not by gut.

## Prerequisites

- A `tasks.md` (or equivalent) with at least 4 backlog items written out.
- Each item must have a one-line description of the user-facing change it delivers.
- Familiarity with your product metrics: which actions drive retention, revenue, or activation (needed to estimate Impact/Reach).
- No special tool required — plain Markdown table is enough.

## Steps

1. **Choose your formula for this sprint.**
   Use **ICE** when all items target roughly the same user segment (reach is constant):
   `ICE = Impact × Confidence × Ease` (each 1–10, score = product, max 1000).
   Use **RICE** when items differ in how many users they affect:
   `RICE = (Reach × Impact × Confidence) / Effort` (Effort = person-weeks, min 0.1).

2. **Add a scoring table to `tasks.md`.**
   Insert this block above your backlog list:

   ```markdown
   ## Backlog Scores (ICE)

   | # | Item | Impact | Confidence | Ease | ICE | Assumptions |
   |---|------|--------|------------|------|-----|-------------|
   ```

3. **Score each item — write assumptions before filling numbers.**
   For every item, before entering a digit, write one sentence per axis:
   - Impact: "If this ships, activation rate rises by ~15% based on the onboarding drop-off data."
   - Confidence: "Medium — no A/B data, only 3 user interviews."
   - Ease: "Low friction — reuses existing API, <1 day of work."

   Then translate each sentence to a 1–10 number. The sentence IS the score; the number is just shorthand.

4. **Fill the worked example below into your own file, replacing items with your actual backlog.**

   Suppose your `tasks.md` has these 6 items for a SaaS indie project (`myapp.io`):

   | # | Item | Impact | Confidence | Ease | ICE | Assumptions |
   |---|------|--------|------------|------|-----|-------------|
   | 1 | Add CSV export to the analytics page | 7 | 6 | 8 | 336 | Impact: power users ask for this weekly (7). Confidence: known segment, no revenue tie (6). Ease: existing data layer, just format it (8). |
   | 2 | Redesign onboarding email sequence (3 → 5 steps) | 8 | 5 | 5 | 200 | Impact: onboarding funnel shows 40% drop at step 2 (8). Confidence: hypothesis only, no copy test done (5). Ease: copywriting + Brevo config, 2 days (5). |
   | 3 | Add Stripe webhook retry on 5xx | 6 | 9 | 9 | 486 | Impact: 3 failed payments last month, recoverable (6). Confidence: deterministic — Stripe docs cover it exactly (9). Ease: 30 lines, existing webhook handler (9). |
   | 4 | Build public API v1 (read-only) | 9 | 3 | 2 | 54 | Impact: opens integrations market (9). Confidence: untested demand, no user validation (3). Ease: months of work, auth + docs + versioning (2). |
   | 5 | Fix timezone bug in report dates | 5 | 10 | 10 | 500 | Impact: cosmetic but causes support tickets (5). Confidence: bug is confirmed and reproducible (10). Ease: one-line fix in date formatter (10). |
   | 6 | Add "remember filters" to dashboard | 6 | 7 | 7 | 294 | Impact: reduces repetitive setup for daily users (6). Confidence: 5 users requested it explicitly (7). Ease: localStorage, no backend change (7). |

5. **Sort by ICE score descending.**

   | Rank | Item | ICE |
   |------|------|-----|
   | 1 | Fix timezone bug in report dates | 500 |
   | 2 | Add Stripe webhook retry on 5xx | 486 |
   | 3 | Add CSV export to the analytics page | 336 |
   | 4 | Add "remember filters" to dashboard | 294 |
   | 5 | Redesign onboarding email sequence | 200 |
   | 6 | Build public API v1 (read-only) | 54 |

6. **Pick the top 2 for next sprint — annotate the table.**
   Mark the top 2 with `→ NEXT`:

   ```markdown
   | 1 | Fix timezone bug in report dates | 500 | → NEXT |
   | 2 | Add Stripe webhook retry on 5xx | 486 | → NEXT |
   ```

   Do not cherry-pick lower-ranked items unless an item above is explicitly blocked (dependency, external API unavailable). If you override the ranking, write the override reason inline.

7. **Archive the scoring table after each sprint.**
   Append the scored table to `tasks-archive.md` with the sprint date, so future scoring sessions can compare calibration over time.

## Verify

Open `tasks.md` and confirm:

```
grep -c "NEXT" tasks.md
```

Returns `2`. If it returns 0, the sprint picks are not annotated. If it returns >2, too many items are marked — trim to 2.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Two items have identical ICE scores | Assumptions were not written; scores were guessed symmetrically | Go back to Step 3: write the assumption sentence first, then derive the number — gut-feel clones resolve |
| High-impact items keep scoring low (Confidence kills them) | Confidence is being used as risk aversion, not as epistemic certainty | Confidence should reflect "how sure am I this estimate is correct", not "how risky is shipping this" — re-read your assumption sentences |
| Sprint always picks the easiest item, never the impactful one | Ease is overweighted because Ease=10 dominates the product | Switch to RICE with explicit Effort denominator; the effort cost acts as a natural brake on trivial easy items |
| Backlog items are too vague to score | Items like "improve UX" have no measurable impact | Rewrite each item as a concrete user-facing outcome before scoring: "reduce checkout steps from 4 to 2" |

## Next

- Apply `backlog-hygiene` first if your backlog has >20 items — score only groomed items.
- After 3 sprints, review calibration: compare estimated vs. actual Impact scores.
- Upgrade to RICE once your product tracks weekly active users or activation cohorts — Reach becomes meaningful data, not guesswork.

## References

- [knowledge/solo/product/product-operations/feature-prioritization-rice](../../../knowledge/solo/product/product-operations/feature-prioritization-rice) — provides the RICE formula definition, axis calibration guidelines, and worked scoring examples that back Steps 1–5 of this playbook.
- [knowledge/solo/product/product-operations/backlog-management](../../../knowledge/solo/product/product-operations/backlog-management) — backlog grooming discipline referenced in Next and Step 7 (archive pattern keeps scoring history clean).
