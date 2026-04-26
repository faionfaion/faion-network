# Backlog Management

## Summary

Methodology for maintaining a prioritized, healthy backlog that connects work items to product goals. Applies the DEEP principle (Detailed-top, Emergent-bottom, Estimated, Prioritized) and INVEST criteria for story quality. Weekly grooming, regular cleanup, and a clear "ready" definition prevent backlogs from becoming unactionable dumping grounds.

## Why

Backlogs treated as storage accumulate hundreds of items with no clear ordering, vague requirements, and stale entries. This silently kills velocity: sprint planning becomes negotiation theater, engineers start without clear acceptance criteria, and important work competes with noise. A healthy backlog — 2-4 sprints of ready items, under 10% stale, over 80% with acceptance criteria — makes planning fast and execution clear.

## When To Use

- Backlog has more than 100 items and "next sprint" is unclear or untrusted.
- Pre-grooming session: classify new items, flag stale ones for archive.
- After SDD spec/design lands: decompose into INVEST stories with acceptance criteria.
- Cross-project rollup: same person owns 5+ backlogs across Linear/Jira/GitHub Projects.
- Migrating between trackers (Trello to Linear, GitHub Issues to Jira).

## When NOT To Use

- Solo founder with fewer than 30 items — a Markdown file beats agent automation.
- Backlog is a wishlist with no commitment system — fix process before adding agents.
- Compliance-bound product (medical, aviation) where every state change needs human signoff and audit trail.

## Content

| File | What's inside |
|------|---------------|
| `content/01-backlog-principles.xml` | DEEP/INVEST principles, backlog structure (Ready/Upcoming/Backlog/Icebox), and item quality criteria. |
| `content/02-grooming-process.xml` | 5-step process: capture, groom, prioritize, refine, cleanup. Includes health targets and agent integration rules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-health-check.md` | Snapshot by status/type with health metrics table and action checklist. |
| `templates/grooming-agenda.md` | Session template: new item triage, top-of-backlog review, refinement, estimates, cleanup. |
| `templates/backlog-item.md` | Story template with user story, Given/When/Then AC, size, priority, dependencies, links. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/backlog-health.sh` | Linear API pull + Claude health report + stale candidate extraction, designed for weekly cron. |
