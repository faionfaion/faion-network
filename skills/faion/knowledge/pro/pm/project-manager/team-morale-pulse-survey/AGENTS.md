---
slug: team-morale-pulse-survey
tier: pro
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3373b3efc5e9c25f"
summary: A 4-question anonymous pulse survey (eNPS + workload + autonomy + clarity) run mid-sprint to catch morale slides before they turn into attrition or distressed-project signals.
tags: [team-morale, eNPS, pulse-survey, project-rescue, leadership]
---

# Team Morale Pulse Survey

## Summary

**One-sentence:** A 4-question anonymous pulse survey (eNPS + workload + autonomy + clarity) run mid-sprint to catch morale slides before they turn into attrition or distressed-project signals.

**One-paragraph:** Annual engagement surveys (Gallup Q12, Officevibe) are too lagged for distressed-project rescue or multi-team coordination. This methodology packages a 60-second 4-question pulse (1 eNPS, 1 workload score, 1 autonomy score, 1 clarity score) with anonymous submission, weekly cadence, and a deterministic alert rule (eNPS drop &gt; 20 or any axis median &lt; 6 → manager 1:1 within 48h). Output: `MoralePulse` aggregate report + per-team alerts. Designed to be PM-runnable (no HR needed) inside a sprint window.

## Applies If (ALL must hold)

- team size 3-15 (single-team) OR multi-team program with consistent cadence
- PM has authority to schedule 1:1s and act on signals
- team has a private chat channel (Slack/Teams) where the survey link can be posted
- engagement spans ≥ 4 sprints (so trend analysis is meaningful)

## Skip If (ANY kills it)

- team size &lt; 3 — anonymity impossible; do real 1:1s
- HR already runs a competing weekly pulse — duplicate cadence dilutes response rates
- team is in active crunch / launch &lt; 7 days out — survey workload during crunch is hostile
- PM does NOT act on prior signals — running this when nothing happens with results destroys trust

## Prerequisites

- a survey tool (Polly, Officevibe Pulse, Google Forms, Tally) that supports anonymity
- weekly recurring calendar event for posting and review
- a private channel for the PM to share aggregate results
- baseline data: first 2 weeks data is calibration, not signal

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/distressed-project-rescue` | Consumes morale alerts as a rescue input signal |
| `pro/pm/project-manager/multi-team-coordination` | Aggregates pulse across teams for program-level view |
| `pro/comms/hr-recruiter/team-coaching` | Downstream handler when 1:1s reveal coaching needs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-question limit, anonymity, alert thresholds, action SLA, no-retaliation | ~900 |
| `content/02-output-contract.xml` | essential | `MoralePulse` aggregate schema + alert event schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: identifying with N-of-1, scope creep questions, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `survey_template_compose` | haiku | Fixed text fill |
| `response_aggregation` | haiku | Numeric average + median |
| `alert_decision` | sonnet | Threshold + multi-axis check |
| `trend_summary_for_pm` | sonnet | Cross-sprint comparison |

## Templates

| File | Purpose |
|------|---------|
| `templates/pulse-survey.md` | The 4-question form |
| `templates/morale-pulse.json` | Output schema |
| `templates/alert-event.json` | Alert event schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/aggregate-pulse.py` | Aggregates anonymous responses, applies alert rules | Weekly Thursday 16:00 |
| `scripts/trend-report.py` | 4-week rolling trends per team | End of sprint |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `distressed-project-rescue`, `multi-team-coordination`
- external: [Gallup Q12 employee engagement](https://www.gallup.com/q12-employee-engagement-survey/) · [Net Promoter Score / eNPS framework](https://www.netpromoter.com/) · [Officevibe Pulse research 2023](https://officevibe.com/state-of-engagement) · [Patrick Lencioni — Five Dysfunctions of a Team](https://www.tablegroup.com/topics-and-resources/teamwork-five-dysfunctions/)
