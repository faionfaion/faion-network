# Agile and Hybrid Approaches

## Summary

A decision framework for selecting and tailoring a delivery mode — predictive (waterfall), agile (Scrum/Kanban), or a named hybrid pattern — based on six scored dimensions: requirement clarity, stakeholder engagement, risk tolerance, team agility, contract flexibility, and regulatory burden. "Hybrid" is never a hand-wave; the selected pattern must be named (Water-Scrum-Fall, agile-discovery-then-predictive, predictive-governance-over-agile-execution). LLMs default to "agile" for almost any prompt — force balanced scoring.

## Why

No single approach fits every project. Pure waterfall is too rigid for uncertainty; pure agile fails on fixed-price compliance work. The mismatch creates rework, missed gates, and client disputes. The six-dimension scoring model makes the approach selection auditable — the decision is traceable to project inputs, not PM preference.

## When To Use

- Choosing a delivery mode at project kickoff given a known project context
- Re-evaluating mid-project when symptoms appear (waterfall slipping repeatedly, Scrum failing on fixed-price compliance)
- Designing a tailored hybrid for fixed-price clients
- Authoring the Development Approach section of a PMBoK 8 plan
- Coaching a team transitioning between approaches with explicit ceremony and artefact mappings

## When NOT To Use

- Tiny projects under 4 weeks with a single well-scoped team — any methodology overhead beats the work itself; use a checklist
- Mandated-by-contract approaches (DoD waterfall, FDA validated software) — no degrees of freedom
- Pure operations / BAU work with no defined start/end — use Kanban + SLAs, not project methodology
- Research-heavy pre-PMF startups — approach selection is premature

## Content

| File | What's inside |
|------|---------------|
| `content/01-approach-spectrum.xml` | Predictive vs agile spectrum; six selection dimensions; named hybrid patterns; common failure modes |
| `content/02-scrum-kanban.xml` | Scrum events/roles, Kanban principles/WIP limits, approach-fit metrics |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-planning.md` | Sprint planning document with capacity table, backlog, dependencies, risks |
| `templates/kanban-board.md` | Kanban board state template with WIP limits |
| `templates/approach-score.py` | Python: score six dimensions, recommend predictive/agile/hybrid |
