# 30-Day Onboarding Phase

## Summary

Structured first-30-day onboarding framework covering orientation (Week 1), foundation
building (Week 2), and deep-dive with first deliverable (Weeks 3-4). The testable rule:
every 30-day plan must define exactly one meaningful milestone (first PR, first sales
call, first resolved ticket) — "completed all training" is not a valid milestone because
it measures activity, not contribution.

## Why

20% of voluntary turnover happens within the first 45 days. BambooHR research links
structured onboarding to 82% higher retention and 70% faster productivity ramp. The
single-milestone rule forces managers and new hires to agree on what "good" looks like
at Day 30, preventing the "set and forget" pattern where the plan becomes a shelf
document with no measurable outcome.

## When To Use

- Generating role-specific 30-day plans (engineer, sales, support) from a universal
  template plus team runbook.
- Producing pre-boarding and Day 1 packets: welcome email, equipment checklist, week 1
  calendar invites, required doc links.
- Tracking onboarding completion across new hires via HRIS/LMS APIs and surfacing
  "behind plan" cases to managers.
- Drafting personalized check-in agendas (Day 7, 14, 30) based on hire progress.
- Synthesizing 30-day survey responses across cohorts to identify systemic issues.

## When NOT To Use

- Companies under 20 employees where each onboarding is bespoke — structured templates
  become overhead rather than support.
- Senior executives (VP/CXO) — their onboarding is high-touch stakeholder-mapping work
  that template structures cannot capture.
- Contract or contingent workers with engagements shorter than 30 days.
- Active reorg or RIF — build the plan after stabilization, not during.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Day 1-30 phase structure, weekly objectives, success criteria, check-in schedule. |
| `content/02-role-examples.xml` | Role-specific 30-day plans for software engineer and sales representative with concrete milestones. |
| `content/03-rules-and-gotchas.xml` | Single-milestone rule, calendar conflict risks, privacy constraints, localization issues. |

## Templates

| File | Purpose |
|------|---------|
| `templates/30-day-plan.md` | Universal 30-day plan template: week-by-week tasks, success criteria, check-in schedule. |
| `templates/bootstrap-newhire.sh` | Agent entry point: generate plan from role/manager inputs, create GitHub issue. |
