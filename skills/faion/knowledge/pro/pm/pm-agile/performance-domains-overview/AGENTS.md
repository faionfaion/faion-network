# Performance Domains Overview (PMBOK 7)

## Summary

PMBOK 7 organizes project management into eight concurrent, interconnected performance domains — Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty — each focused on outcomes rather than process steps. The domains are always active simultaneously; neglecting any one degrades the others through well-documented interaction chains.

## Why

Traditional process-based PM produces compliance metrics while missing value delivery. Domains shift the question from "did we follow the process?" to "are we achieving results in each area?". An eight-axis health check run on real project artifacts (retros, risk registers, sprint logs) produces an actionable RAG snapshot that tells the PM which domain to address first to unblock the most other domains.

## When To Use

- Initial project health scan: rapidly identify which of the eight domains is weakest.
- Onboarding a PM or agent into an existing project with a structured eight-axis mental model.
- Quarterly project audit or steering committee preparation.
- Choosing which methodology to load next (each domain points at concrete sub-methodologies).

## When NOT To Use

- Single-sprint feature work — too high-level; use Scrum ceremonies directly.
- Pure waterfall regulated projects with prescribed templates — use PMBOK 6 process groups.
- Personal or solo projects without stakeholders or external delivery commitments.

## Content

| File | What's inside |
|------|---------------|
| `content/01-domains.xml` | All eight domains: purpose, outcomes, key activities, related methodologies. |
| `content/02-interactions.xml` | Domain interaction table, assessment procedure, common mistakes, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pd-assessment.sh` | Shell script: emits a fresh eight-row assessment skeleton with weakest-domain prompt. |
