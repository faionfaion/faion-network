# Agile and Hybrid Approaches

## Summary

A decision framework for selecting among Predictive (waterfall), Agile (Scrum/Kanban), and Hybrid delivery models based on five project factors: requirements clarity, stakeholder availability, risk tolerance, team experience, and contract type. Hybrid approaches combine elements — e.g., Water-Scrum-Fall, agile execution under predictive governance — when no pure model fits.

## Why

Most delivery failures stem from applying the wrong approach: waterfall on high-uncertainty work causes late feedback loops; pure agile on fixed-price contracts masks scope creep. A five-question selection framework with scored thresholds produces a defensible, context-grounded recommendation rather than defaulting to the PM's preferred methodology.

## When To Use

- Project kickoff where the right delivery model is genuinely unclear (mixed-experience team, semi-defined scope).
- Fixed-price contracts that need agile execution under predictive governance (Water-Scrum-Fall).
- Regulated environments where parts must be predictive (compliance, validation) and parts agile (UI, integrations).
- Coaching engagements moving from waterfall to agile, where pure-agile from day one would fail change management.
- Solopreneur or small-team work where lightweight Kanban + monthly review is right-sized.

## When NOT To Use

- A team already running stable Scrum or Kanban — switching to hybrid loses cadence without recovering certainty.
- Pure exploration or research where any delivery framework is overhead.
- Teams whose dysfunction is cultural, not methodological — a hybrid won't fix accountability gaps.
- Crisis or incident response — use incident-response runbooks, not a delivery framework selection.

## Content

| File | What's inside |
|------|---------------|
| `content/01-selection.xml` | The five-factor decision framework, approach spectrum, and when-to-use table. |
| `content/02-hybrid-patterns.xml` | Three hybrid patterns, Scrum events/roles, Kanban principles, common mistakes. |
| `content/03-examples.xml` | Worked examples: fixed-price hybrid contract, solopreneur Kanban, first-hire integration plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-plan.md` | Sprint planning template: goal, capacity table, backlog, dependencies, risks. |
| `templates/kanban-board.md` | Kanban board template with WIP limits. |
| `templates/pick_approach.py` | Script: reads a YAML decision file and outputs Predictive/Agile/Hybrid recommendation. |
