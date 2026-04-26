# Kanban and Scaled Agile Ceremonies

## Summary

Alternative agile cadences for continuous-flow teams (Kanban) and multi-team programs (SAFe). Kanban replaces fixed sprints with five cadences: daily standup (walk-the-board right-to-left), weekly replenishment, weekly service-delivery review, bi-weekly retrospective, and monthly strategy review. SAFe adds PI Planning (2-day, every 8-12 weeks), Scrum-of-Scrums (daily), PO Sync (weekly), and Inspect-and-Adapt (end of PI). The rule: throughput plus 85th-percentile cycle time beats velocity for forecasting; use Monte Carlo on these for date predictions.

## Why

Sprint boundaries break down for ops, platform, and support teams with high mid-sprint volatility. Kanban cadences decouple commitment from timebox, making WIP limits the primary flow-control mechanism. At scale (3+ Scrum teams), PI Planning provides the cross-team dependency surface that individual standups cannot — it is the SAFe ceremony that delivers the most value per hour spent.

## When To Use

- Continuous-flow teams (support, ops, data engineering) with no natural sprint boundary.
- Multi-team programs needing PI Planning and Scrum-of-Scrums coordination.
- Teams with high mid-sprint volatility (incident-heavy ops, content production).
- Platform teams serving many internal customers where replenishment fits better than sprint commitment.
- Hybrid ScrumBan setups: sprint planning kept for steering, WIP limits enforced for flow.

## When NOT To Use

- A single team of fewer than 8 people with stable feature work — Scrum's ceremonies suffice.
- Pure project work with fixed end date and known scope — predictive cadences fit better.
- Organizations drowning in ceremonies; adding SAFe events without removing others causes revolt.
- Discovery-heavy product work where dual-track agile maps better than SAFe.
- Solopreneur or 2-person teams — overhead exceeds value; a personal Kanban board is enough.

## Content

| File | What's inside |
|------|---------------|
| `content/01-kanban-cadences.xml` | Five Kanban cadences: format, participants, metrics reviewed, outputs. WIP limit rules. |
| `content/02-scaled-agile.xml` | SAFe events: PI Planning agenda, Scrum-of-Scrums format, PO Sync, Inspect-and-Adapt. ScrumBan hybrid. |
| `content/03-agent-usage.xml` | Agentic workflows: kanban-flow-analyst, replenishment-prepper, pi-planning-facilitator. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kanban-metrics.md` | Weekly service-delivery review dashboard: throughput, cycle time, WIP vs limits, blockers, aging items. |
| `templates/cycle-stats.py` | Compute throughput and cycle-time percentiles from a JSONL of issues with state timestamps. |
