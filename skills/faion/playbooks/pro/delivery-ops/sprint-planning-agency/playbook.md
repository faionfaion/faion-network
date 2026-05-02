---
name: sprint-planning-agency
description: Run a 2-week sprint cadence for a 5-person agency team — Monday planning, daily standup, mid-sprint check-in, Friday demo and retro, velocity tracking.
tier: pro
group: delivery-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a repeating 2-week sprint cadence running for your agency team: a 90-minute Monday planning session that locks scope and capacity, a 15-minute daily standup, a 30-minute mid-sprint check-in, and a 1-hour Friday demo and retrospective. You will track team velocity over 3+ sprints and use it to make reliable delivery commitments to clients.

## Prerequisites

- A project management tool with a backlog: Linear, Jira, or Shortcut. Story points enabled (Fibonacci: 1, 2, 3, 5, 8, 13).
- A 5-person agency team: 1 project lead, 3–4 contributors, 1 client-facing owner (may overlap).
- At least 1 sprint of historical data — or start velocity tracking from sprint 1 and commit conservatively.
- Each team member's available days for the sprint (accounts for PTO, client calls, internal ops).
- A recurring calendar series pre-blocked for: Monday 10:00 planning (90 min), daily 09:30 standup (15 min), Wednesday of week 2 check-in (30 min), Friday 16:00 demo+retro (60 min).
- Familiarity with [pro/delivery-ops/capacity-planning](../capacity-planning/playbook.md) — sprint capacity derives from engineer utilization targets.

## Steps

### Monday Planning (90 min)

1. Pull the top items from the backlog into a "Sprint Candidate" column in Linear/Jira. Aim for 20–30% more items than you expect to fit — leave the final cut to capacity math.

2. Run **backlog refinement** (first 30 min of planning): for each candidate, confirm the acceptance criteria is 1–3 concrete, testable statements. Reject any item where the team cannot agree on done in under 2 minutes — push it back to backlog for more definition.

3. Estimate unpointed items using Planning Poker. Use Fibonacci points. Anything estimated at 13 must be split before entering the sprint — 13-point stories hide too much uncertainty for a 2-week window.

4. Calculate **sprint capacity**:

   ```
   capacity_pts = (available_days × velocity_per_day_per_person) × headcount
   ```

   For a 5-person team with 8 working days per sprint (2 days per week absorbed by ceremonies, admin, and client calls) and a velocity of 2 pts/day/person:

   ```
   capacity_pts = 8 × 2 × 5 = 80 pts
   ```

   Use your actual rolling 3-sprint average velocity — not a target — for `velocity_per_day_per_person`.

5. Commit to a sprint scope where total story points ≤ `capacity_pts`. Pull items from the "Sprint Candidate" column top-down (priority order) until capacity is filled.

6. Assign ownership: each story gets one named owner before the meeting ends. Unassigned stories become blockers on day 1.

7. State the **sprint goal** — one sentence describing what the team will have shipped by Friday. Example: "By Friday 2026-05-16, the client onboarding flow is live in staging and approved by Marta from Kovals Ltd."

### Daily Standup (15 min)

8. Run async-first: each person posts to `#standup-2026-q2` Slack channel by 09:30 with exactly three lines:

   ```
   Done: <what I finished since yesterday>
   Doing: <what I am working on today>
   Blocked: <what is blocking me, or 'nothing'>
   ```

9. Hold a 10-minute live sync only when ≥1 person has posted `Blocked:` with a named blocker. The project lead resolves blockers or escalates by 10:00.

10. Track blockers in a `blockers.md` log at the repo root or in a Notion doc — include date opened, person blocked, root cause, and date resolved.

### Mid-Sprint Check-In (30 min, Wednesday of week 2)

11. Pull the sprint board and count: stories in Done vs. stories remaining. A healthy sprint at the mid-point of week 2 has ≥70% of points in Done or In Review.

12. If remaining points > 30% of committed scope at mid-sprint of week 2, identify the two largest remaining stories and make a cut decision: de-scope to next sprint or reassign to available capacity.

13. Send a one-paragraph status update to the client (if the sprint delivers client-facing work):

    ```
    Hi Marta — mid-sprint check-in for Sprint 7 (May 5–16).
    Completed: user login flow, email notifications.
    In progress: onboarding modal (due Fri).
    No blockers. On track for Friday demo.
    ```

### Friday Demo + Retro (60 min)

14. **Demo (20 min):** Each story owner demos the finished work against acceptance criteria. No slides — live product or staging link only. Client can attend; keep demos under 5 min per story.

15. **Retro (40 min):** Use the Start / Stop / Continue format. Each person submits 1–3 items per column in FigJam or a shared Notion board before the meeting. The project lead reads them aloud and the team votes on the top 1–2 actionable items. One owner per action item — it goes straight into the next sprint's backlog.

16. **Close the sprint in Linear/Jira:** move un-finished stories back to backlog with a `carry-over-sprintN` label. Do not silently roll them into the next sprint without re-estimation.

### Velocity Tracking

17. After each sprint, record in `velocity.csv`:

    ```
    sprint,start_date,end_date,committed_pts,completed_pts,team_size,notes
    ```

    Example for a 5-person team over 4 sprints:

    ```
    sprint,start_date,end_date,committed_pts,completed_pts,team_size,notes
    7,2026-04-07,2026-04-18,80,72,5,Marta PTO 2d
    8,2026-04-21,2026-05-02,75,76,5,
    9,2026-05-05,2026-05-16,78,74,5,new hire onboarding 1d
    10,2026-05-19,2026-05-30,80,80,5,
    ```

18. Calculate the 3-sprint rolling average of `completed_pts` after every sprint. Use this number — not `committed_pts` — as your planning ceiling for the next sprint.

    ```
    avg_velocity_3sp = mean(completed_pts for last 3 sprints) = mean(76, 74, 80) = 76.7 → round to 76
    ```

19. Use velocity trend for client commitments: if `avg_velocity_3sp` is stable (±10%), you can quote delivery dates with moderate confidence. If variance is >15%, quote ranges ("2–3 sprints") rather than exact dates.

## Verify

After sprint 1, run this check to confirm your `velocity.csv` is consistent:

```bash
python3 - <<'EOF'
import csv, sys
with open("velocity.csv") as f:
    rows = list(csv.DictReader(f))
if not rows:
    print("ERROR: velocity.csv is empty"); sys.exit(1)
latest = rows[-1]
ratio = float(latest["completed_pts"]) / float(latest["committed_pts"])
print(f"Sprint {latest['sprint']}: completed/committed = {ratio:.2f}")
if ratio < 0.5:
    print("WARNING: <50% completion — re-check capacity calculation or blocker resolution")
else:
    print("velocity.csv OK")
EOF
```

After Friday retro: confirm `#standup-2026-q2` Slack channel shows ≥4 daily posts per person per sprint week (not counting Monday planning day). Gaps indicate standup discipline is slipping.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Committed 80 pts, delivered 45 pts every sprint | Velocity baseline is estimated, not measured | Run 2 sprints at 60% of estimated capacity, measure actual completion, use that as the new baseline |
| Planning takes 3+ hours | Stories not refined before planning; estimation debates during planning | Hold a separate 30-min refinement session on Friday (before retro or after) — planning picks from already-refined stories only |
| Retro produces the same action items every sprint | Actions are assigned but never tracked | Move retro actions into the sprint backlog as explicit 1-pt tasks; mark them Done or carry them forward visibly |
| Mid-sprint check-in reveals 60% of work not started | Stories have hidden dependencies on a single engineer | Require dependency mapping in step 2 refinement; redistribute during planning if one person holds >40% of sprint points |
| Velocity drops 20%+ after adding a new hire | Onboarding overhead not accounted for in capacity | Subtract 8 pts from capacity for each new hire's first sprint; restore gradually over 3 sprints as ramp completes |
| Client attends demo and disputes acceptance criteria | AC was not shared with client before sprint start | Share sprint goal + AC summary with client on Monday after planning; get async approval before Wednesday |

## Next

- [pro/delivery-ops/capacity-planning](../capacity-planning/playbook.md) — connect sprint velocity data to monthly capacity.csv to detect engineer over-utilization signals before they appear in quality metrics.
- Review `knowledge/pro/pm/pm-agile/scrum-ceremonies` for ceremony facilitation depth — particularly estimation anti-patterns that inflate velocity numbers and hide technical debt.
- Once velocity is stable over 6+ sprints, explore `knowledge/pro/pm/pm-agile/agile-hybrid-approaches` to adapt the cadence for fixed-scope client contracts without abandoning sprint hygiene.

## References

- [knowledge/pro/pm/pm-agile/scrum-ceremonies](../../../../../knowledge/pro/pm/pm-agile/scrum-ceremonies) — ceremony structure and facilitation guidelines backing the 90-min planning, 15-min standup, and 1-hour demo/retro time-boxes defined in Steps 1–16.
- [knowledge/pro/pm/pm-agile/team-development](../../../../../knowledge/pro/pm/pm-agile/team-development) — team maturity stages that explain why velocity is unstable in sprints 1–3 and why new-hire capacity reduction (Step 19 troubleshooting) is necessary during Forming/Storming phases.
- [knowledge/pro/pm/pm-agile/agile-hybrid-approaches](../../../../../knowledge/pro/pm/pm-agile/agile-hybrid-approaches) — hybrid delivery models for fixed-price agency contracts; informs the velocity-to-commitment translation in Step 19 when quoting client delivery dates.
