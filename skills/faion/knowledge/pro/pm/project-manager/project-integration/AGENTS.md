# Project Integration Management

## Summary

The PM acts as integrator across all knowledge areas (scope, schedule, cost, quality, risk, resources, communications, procurement) through a single version-controlled integrated plan. Every change request triggers cross-area impact analysis before approval; status colour is derived from numeric thresholds, not PM narrative; and closure is treated as integration's last mile — formal acceptance plus lessons learned plus archive.

## Why

Projects fail from silo management: scope changes approved without schedule updates, cost baselines drifting from schedule, risks without owners. Without integration, each area optimizes locally and the whole degrades. A machine-readable integrated plan with locked source-of-truth and automated threshold alerts catches cross-area drift before it compounds.

## When To Use

- Programs with 2+ workstreams whose decisions interact (scope vs. schedule vs. cost vs. vendor)
- Initiation phase: drafting the project charter to authorize work and bind sponsor commitment
- Change-heavy environments where every CR has cross-area impact simultaneously
- Multi-team or multi-vendor delivery where local optimization harms whole-system performance
- Project closure: final integration, lessons learned, formal acceptance, contract closeout

## When NOT To Use

- Single-team, single-stream work with a stable backlog — Scrum or Kanban already integrates within the team
- Short tactical engagements under 4 weeks with no inter-area trade-offs — overhead exceeds value
- Pure research or discovery phases with no committed scope — wait until charter signal is real
- Solo-developer projects — keep artifacts lightweight (one-page charter, weekly check); the integrator is one person

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Integration activities, charter elements, change control process, component plan index |
| `content/02-workflow.xml` | Agentic integrated-plan pipeline, subagent roles, change-impact prompt pattern |
| `content/03-tools-and-references.xml` | CLI tools, SaaS platforms, best practices, AI-agent gotchas, references |

## Templates

| File | Purpose |
|------|---------|
| `templates/charter.md` | Project charter template with SMART objectives, success criteria, constraints, approval block |
| `templates/status-report.md` | Weekly status report template with GREEN/YELLOW/RED per knowledge area |
| `templates/integration-status.py` | Script: compute status colours from numeric YAML inputs via threshold ladders |
