---
slug: launch-day-warroom-template
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Coordinated war-room template for launch day — channels, roles, escalation paths, hourly checkpoints, and rollback playbook.
content_id: "54c71c5118d891a2"
tags: [launch,war-room,coordination,product-hunt,rollback,escalation]
---
# Launch-Day Warroom Template

## Summary

**One-sentence:** Coordinated war-room template for launch day — channels, roles, escalation paths, hourly checkpoints, and rollback playbook.

**One-paragraph:** Launch days fail on coordination, not creative. The plan is written and the assets are ready, but on launch morning no one knows who decides when to push the Product Hunt link, who pings the affiliate cohort, or what to do when the API rate-limits. This methodology defines the war-room template: a named role list (launch director, content captain, ops lead, support triage, exec stand-in), a Slack/Discord channel topology (#launch-control, #launch-content, #launch-support, #launch-exec), a 12-hour hourly-checkpoint schedule with explicit decisions per hour, an escalation tree, and a rollback playbook for partial / full launch retraction. Mechanism: pre-launch dress rehearsal, named back-up per role, decision-rights matrix. Primary output: a launch-day runbook every role member acknowledges 48 hours before launch.

## Applies If (ALL must hold)

- launch involves ≥ 2 channels (Product Hunt, X/Twitter, email, podcast, YouTube)
- launch has ≥ 5 contributors (eng, design, marketing, support, comms)
- launch has a fixed launch hour (Product Hunt window, scheduled press)
- prior launch experienced coordination breakdown OR this is the team's first launch
- team uses Slack / Discord / Teams for real-time coordination

## Skip If (ANY kills it)

- solo launch (one person doing everything) — war room would be self-talking
- soft launch / rolling release with no fixed hour
- internal-only launch (no external audience pressure)
- launch already running — use incident playbook, not war-room setup
- ≥ 3 launches per quarter on autopilot — operational maturity, war-room overhead unnecessary

## Prerequisites (must be true before starting)

- launch date + hour set ≥ 14 days out
- contributor list with availability confirmed for launch ± 12h
- assets ready: tweets, emails, blog post, PH listing, screenshots
- support contact rotation finalized
- monitoring + dashboards configured (signups, errors, API latency)
- exec stand-in named in case decision-rights escalation triggers

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/growth-experiment-design` | Optional: launch-as-experiment framing |
| `pro/marketing/gtm-strategist/launch-playbook` | Strategic context the war room executes |
| `pro/dev/software-developer/api-monitoring-alerting` | Alerts during traffic surge |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named roles, dress rehearsal, hourly checkpoints, decision-rights matrix, rollback playbook | ~1000 |
| `content/02-output-contract.xml` | essential | Runbook schema, role assignments, checkpoint table, escalation tree | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (silent role, decision deadlock, channel chaos, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `runbook_outline_draft` | sonnet | Generate war-room runbook skeleton from template |
| `role_assignment_synth` | sonnet | Map team roster to roles + backups |
| `checkpoint_schedule_synth` | sonnet | Generate hour-by-hour schedule with decisions |
| `escalation_tree_writer` | sonnet | Draft escalation paths |

## Templates

| File | Purpose |
|------|---------|
| `templates/warroom-runbook.md` | Master runbook template |
| `templates/role-assignment-matrix.md` | Decision-rights × role matrix |
| `templates/checkpoint-schedule.md` | 12-hour hourly schedule |
| `templates/rollback-playbook.md` | Retraction procedures |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/dress-rehearsal-checklist.py` | Verify pre-launch readiness | T-48h |
| `scripts/launch-status-rollup.py` | Aggregate channel metrics into one update | Hourly during launch |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `launch-retro-template`, `growth-experiment-design`
- external: [Product Hunt launch guide](https://www.producthunt.com/launch) · [Lenny's launch playbook](https://www.lennysnewsletter.com/p/product-launch-playbook)
