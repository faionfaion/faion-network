# Continuous Discovery

## Summary

Teresa Torres' framework for embedding product discovery into the weekly delivery rhythm: daily signal collection (analytics, tickets), weekly customer interviews (2-3), weekly competitor monitoring, weekly assumption testing, bi-weekly OST synthesis, monthly research review. Implemented as a cron-driven multi-agent pipeline that writes to `.aidocs/product_docs/discovery/`.

## Why

Discovery treated as a one-time project-start activity produces stale insights within weeks. Markets with 6-month half-life on user-need validity (AI tools, fintech, dev tooling) require an always-on opportunity backlog. The agent cadence keeps cheap models (Haiku) on daily mechanical tasks and Opus only on bi-weekly+ pattern recognition, preventing token-cost blowout.

## When To Use

- Live products with active users where signal volume exceeds what a human PM can review unaided.
- Product Trio (PM + designer + engineer) workflows needing a weekly cadence of customer touchpoints.
- Markets with 6-month half-life on user-need validity.
- Solopreneur stacks where one operator must simulate trio coverage via subagents.
- After a launch when growth slows and the "solution that worked 6 months ago no longer works" pattern must be detected.

## When NOT To Use

- Pre-PMF zero-to-one with no users yet — start with `customer-development` or `jobs-to-be-done`.
- Compliance-bound enterprise sales where contract cycles are 6-18 months.
- Hardware/regulated medical where each iteration ships in months.
- Crisis mode (active outage, churn cliff) — switch to root-cause work first.
- When stakeholders demand "validated" answers from a single interview — Torres explicitly rejects validation theater.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cadence-and-agents.xml` | Weekly cadence table, 8-subagent pipeline (model/cadence/inputs/outputs), scheduling via cron/systemd. |
| `content/02-prompt-pattern.xml` | XML prompt pattern for all cadence agents, key rules (N>=5, opportunity vs solution, curse-of-knowledge). |
| `content/03-gotchas-and-tools.xml` | Failure modes, CLI tools, services/apps table, best practices. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost-schema.json` | OST node schema: id/type/parent/evidence/status fields for git-tracked tree. |
| `templates/analytics-watcher.py` | Agent SDK daily watcher: fetches PostHog + tickets, appends to insight-log.md. |
| `templates/crontab.txt` | Cron schedule for four discovery cadences (daily/weekly/bi-weekly/monthly). |

## Scripts

none
