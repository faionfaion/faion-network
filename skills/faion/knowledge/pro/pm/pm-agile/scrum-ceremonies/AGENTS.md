# Scrum Ceremonies

## Summary

The five Scrum events — Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, and Backlog Refinement — with time-boxes, facilitation patterns (including async/remote variants), tool configurations, and quality gates. Sprint goal must be falsifiable in one sentence; retro actions must have an owner and a linked issue or they do not exist; async standup blockers must escalate within 1 working day.

## Why

Ceremony theatre — running events without the underlying DoR/DoD discipline and action follow-through — is the most common Scrum failure mode. The five events exist to create inspect-and-adapt loops at different cadences, not to generate reports for management. Each event has a specific output and a quality gate; agents can automate prep and capture, but cannot replace facilitation.

## When To Use

- Bootstrapping Scrum for a new team and wiring ceremonies into a PM tool (Jira, Linear, GitHub Projects).
- Replacing free-form standups with structured cadence after onboarding or merging teams.
- Optimizing a remote/distributed Scrum team — async standups, retro tools, recorded reviews.
- Reducing ceremony time-tax (pre-refine with an agent the day before planning).
- Evidence collection for transformations (sprint goal achievement, retro action follow-through, velocity stability).

## When NOT To Use

- Solo developer or pair — Scrum overhead exceeds value; use Kanban with lightweight reviews.
- Pure research or discovery teams with no incremental delivery — use Lean Startup or Discovery Kanban.
- Crisis or incident periods — break glass, run incident process, restart Scrum after.
- Hardware-heavy programs where 2-week sprints do not match material lead times.
- Teams with working ceremonies and good outcomes — do not redesign for novelty.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ceremonies-guide.xml` | All five events: time-boxes per sprint length, sprint planning parts (what/how), daily standup formats (classic/walk-board/async), review setup, retrospective formats (SSC/4Ls/Sailboat/MSG), backlog refinement agenda and DoR. |
| `content/02-estimation-antipatterns.xml` | Planning poker process, T-shirt sizing scale, and antipatterns: ceremony theatre, standup as reporting, retros without action follow-through, estimation anchoring from LLMs, async blocker rot. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-planning.md` | Sprint planning notes: sprint info, goal, team capacity, committed backlog, stretch goals, risks/dependencies, action items. |
| `templates/retrospective.md` | Retrospective template: sprint metrics, what went well, what to improve, action items with owner/due, previous action review, team health check. |
| `templates/standup-bot.yaml` | Geekbot async standup configuration with questions and schedule settings. |
| `templates/sprint-review-readiness.py` | Gate script: checks completion ratio, demoable items, demo environment, invited stakeholders, escaped bug count. |
