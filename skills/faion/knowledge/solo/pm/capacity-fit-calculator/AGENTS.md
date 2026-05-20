---
slug: capacity-fit-calculator
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "2534aec450f5d0f3"
summary: Lightweight per-sprint capacity vs commitment calculator for solo PMs — PTO + ceremonies + interrupt buffer subtracted; outputs a fit ratio used at sprint planning.
tags: [capacity-planning, sprint-planning, solo-pm, agile, allocation]
---
# Capacity-Fit Calculator (Solo PM)

## Summary

**One-sentence:** A per-sprint capacity vs commitment calculator that subtracts PTO, ceremonies, and an interrupt buffer from raw availability, then reports a fit ratio the solo PM can use to accept or trim the sprint.

**One-paragraph:** Pro/delivery-ops has a full capacity-planning playbook designed for resource managers across multiple programs. A solo PM running a single team needs less — but they need it weekly and without spreadsheet ceremony. This methodology pins a deterministic formula (effective_capacity = head_count × work_days × focus_hours − ceremonies − pto − interrupt_buffer) and a "fit ratio" (committed_points / effective_capacity). When fit &gt; 0.9, the sprint is unsafe; when 0.7-0.9, acceptable; when &lt; 0.5, the sprint is under-committed and likely to drift. The calculator runs in &lt; 15 minutes and produces a one-line fit statement the team can challenge at sprint planning.

## Applies If (ALL must hold)

- Team uses time-boxed sprints (1-3 weeks) with point or hour estimates.
- PM is solo (or small team) and does not have a dedicated resource manager.
- Historical velocity exists for at least 3 sprints (rolling average available).
- PM has visibility into team PTO calendar.

## Skip If (ANY kills it)

- Flow-based teams (Kanban, no-sprint) — use WIP-limit + cycle-time methodology instead.
- Team commits explicitly to "fixed scope, variable date" — capacity-fit is about the wrong dimension.
- Headcount &gt; 12 — switch to the pro tier delivery-ops capacity-planning methodology.
- First-3-sprints team without velocity baseline — use commitment-floor heuristic, not this formula.

## Prerequisites

- Sprint length defined (working days, e.g., 10 days for 2 weeks).
- Per-person focus-hours-per-day baseline (typical: 6h for senior, 5h for junior, 4h for tech lead with mentoring load).
- Ceremony overhead inventory (planning, refinement, standups, retro, demo) summed per sprint per person.
- Team PTO calendar (each absence in days).
- Rolling velocity from last 3 sprints (points or hours per sprint).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/sprint-planning` | The calculator's output is the input to sprint planning facilitation; that methodology is the wrapper. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: formula, subtraction order, interrupt buffer, fit interpretation bands | ~800 |
| `content/02-output-contract.xml` | essential | Fit statement shape; required inputs; tracking sheet | ~600 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: forgotten ceremonies, optimistic velocity, missing PTO | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-effective-capacity` | haiku | Pure arithmetic over inputs |
| `assess-commitment-vs-capacity` | sonnet | Bounded judgment on selected story shape |
| `recommend-trim-or-stretch` | sonnet | Apply fit bands to commitment list |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-sheet.csv` | One-line per sprint with inputs, computed effective_capacity, fit ratio |
| `templates/sprint-fit-statement.md` | The single-paragraph output for sprint planning |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/capacity-compute.py` | Computes effective_capacity and fit_ratio from CSV row | Before sprint planning |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodology: `sprint-planning`, `velocity-tracking`, `commitment-charter`
- external: [Mike Cohn — Agile Estimating and Planning](https://www.mountaingoatsoftware.com/books/agile-estimating-and-planning)
