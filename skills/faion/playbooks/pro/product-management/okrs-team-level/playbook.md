---
name: okrs-team-level
description: Set one team Objective + 3 measurable Key Results for a quarter, run weekly check-ins, and score at quarter-end.
tier: pro
group: product-management
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook your team will have one clear quarterly Objective, three scored Key Results tied to it, a repeatable weekly check-in ritual at the 0.0/0.3/0.7/1.0 scoring cadence, and a quarter-end review doc that feeds the next planning cycle.

## Prerequisites

- A team of 2–12 people with a shared product or growth scope.
- A shared doc space (Notion, Confluence, or a Google Doc folder) where the OKR lives and is visible to all team members.
- Calendar access to block a weekly 15-minute check-in slot for the full quarter.
- Clarity on the team's primary success metric going into the quarter (e.g., paid user count, DAU/MAU, NPS score).
- Prior playbook (recommended): `prd-template` — confirms the problem space and user goals before setting Objectives.

## Steps

1. **Draft the Objective.** Write one sentence that describes the qualitative outcome the team wants to own by the end of the quarter. Good test: a senior leader outside the team should read it and immediately understand why it matters.
   - Anti-pattern: "Improve the product" — not directional, not inspirational.
   - Good pattern: "Become the default tool for solo founders managing their first product launch."

2. **Sanity-check the Objective against three filters.** Before writing KRs, verify the Objective is:
   - Aspirational — stretches the team slightly beyond comfortable.
   - Bounded — achievable within 12 weeks with the current headcount.
   - Customer-visible — an outsider (user, investor, partner) would care if achieved.
   If it fails any filter, rewrite it before step 3.

3. **Write exactly 3 Key Results.** Each KR must be:
   - A number or ratio, not a task. "100 paid users" is a KR. "Launch pricing page" is a task — move it to the backlog.
   - Owned by the team, not another team.
   - Falsifiable by end of quarter — you can score it 0.0–1.0 with no ambiguity.

   **Example — Growth team Q3:**
   - O: "Become the default tool for solo founders."
   - KR1: 100 paid users (baseline: 23 today).
   - KR2: DAU/MAU ≥ 0.4 (baseline: 0.18 today).
   - KR3: NPS ≥ 30 from first-month cohort survey (baseline: 12 today).

4. **Set the 1.0 target, then the 0.7 target.** For each KR:
   - 1.0 = full achievement. You would be genuinely surprised to hit this.
   - 0.7 = satisfactory stretch. You expect to land here on a good quarter.
   - Commit to KR1 baseline + current in the OKR doc alongside each target.

5. **Publish the OKR doc** in the team shared space within 48 hours of quarter start. Format:

   ```
   Team: Growth
   Quarter: Q3 2026
   Objective: Become the default tool for solo founders.

   KR1: 100 paid users         [current: 23] [0.7 target: 80]
   KR2: DAU/MAU ≥ 0.4          [current: 0.18] [0.7 target: 0.35]
   KR3: NPS ≥ 30               [current: 12] [0.7 target: 25]
   ```

6. **Block weekly check-in.** Every Monday (or your team's equivalent start-of-week), 15 minutes:
   - Each KR owner updates the current number.
   - Score each KR on 0.0 / 0.3 / 0.7 / 1.0 scale:
     - 0.0 — no progress or regression.
     - 0.3 — early signal; well below target pace.
     - 0.7 — on track; reached stretch minimum or better.
     - 1.0 — achieved or exceeded target.
   - If any KR is stuck at 0.0 for two consecutive weeks, flag it as at-risk in the doc and identify one unblock action.

7. **Run the mid-quarter review (week 6).** With the team:
   - Review current scores. If the team is consistently at 1.0 on a KR by week 6, the target was too easy — document it as a calibration lesson for next quarter.
   - Adjust initiatives (tasks, experiments) that feed the KRs. Do NOT adjust the KR targets mid-quarter unless a material external change makes the original target meaningless.

8. **Score the quarter at week 12.** Final scores:
   - Lock scores before the retrospective.
   - Average the three KR scores: (KR1 + KR2 + KR3) / 3.
   - A team average of 0.6–0.7 is healthy. Consistently hitting 1.0 means targets are too conservative.

9. **Write a one-page quarter retrospective.** Include:
   - Final KR scores and the average.
   - One sentence per KR explaining the gap or overshoot.
   - Top 1–2 learnings that inform the next Objective.
   - Draft Objective for next quarter (to be refined in the next planning session).

## Verify

Open the OKR doc and confirm all four items are present:
1. Exactly one Objective sentence.
2. Exactly three KRs, each with a baseline number, a 0.7 target, and a 1.0 target.
3. A weekly check-in entry for the current week with numeric scores.
4. A named owner for each KR visible in the doc header or table.

If any item is missing, the OKR is not operational — return to the relevant step.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Team proposes 7 KRs for one Objective | Scope of Objective is too broad, or team conflating tasks with KRs | Narrow the Objective to a single user outcome; move tasks to project tracker |
| KR score has not moved after 3 weeks | No team initiative is directly driving the KR metric | Map each KR to ≥1 concrete experiment or feature; block 2h to identify the lever |
| Score stays at 1.0 from week 2 onward | Target was set too conservatively (team knows exactly how to hit it) | Document as calibration error; raise 1.0 target for next quarter; use current quarter to explore a bolder KR |
| Team argues over whether a KR is 0.7 or 1.0 | KR definition is ambiguous — "high NPS" instead of "NPS ≥ 30" | Rewrite KR as a hard number or ratio before next quarter; for current quarter, use the midpoint as 0.7 |
| Second team creates a KR that depends on the first team delivering a feature | Cross-team dependency not resolved at planning | OKRs must be owned end-to-end by the setting team; replace with a KR the team can drive autonomously, and track the dependency separately in a RACI |

## Next

- `prd-template` — write a PRD that defines the features and experiments that will drive KR progress.
- Review `knowledge/pro/product/product-manager/product-analytics` for tracking DAU/MAU and NPS instrumentation that feeds KR scoring.
- Consider `knowledge/pro/pm/pm-agile/scrum-ceremonies` to integrate OKR check-ins into an existing sprint cadence without adding extra meetings.

## References

- [knowledge/pro/product/product-manager/product-analytics](../../../knowledge/pro/product/product-manager/product-analytics) — defines the DAU/MAU and retention metrics used as KR targets in Step 3's Growth team example; backs the scoring baseline approach in Steps 4 and 6.
- [knowledge/pro/pm/pm-agile/scrum-ceremonies](../../../knowledge/pro/pm/pm-agile/scrum-ceremonies) — weekly check-in rhythm in Step 6 maps directly to the sprint review cadence; the 0.0/0.3/0.7/1.0 scoring aligns with the done/in-progress/blocked vocabulary used in scrum ceremony facilitation.
