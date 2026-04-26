# Roadmap Design

## Summary

A five-step process for building a product roadmap as a strategic communication tool,
not a delivery schedule. Covers four roadmap formats (timeline, Now-Next-Later,
outcome-based, kanban) with a selection matrix, theme-based organisation, confidence
levels, and audience-specific rendering (internal vs external). The core rule: every
initiative links to one objective ID; orphaned initiatives are strategy leakage.
Solo founders: if the roadmap doesn't fit one screen, it's a backlog.

## Why

Roadmaps that list features with dates always slip and erode trust. The format mismatch
is the root cause: a timeline roadmap implies commitment; a Now-Next-Later roadmap
signals intent. Choosing the wrong format for the audience turns every missed date into
a broken promise. The theme-plus-objective structure prevents the roadmap from
degenerating into a backlog; confidence levels prevent "Later" from becoming a graveyard.

## When To Use

- Communicating a 1-4 quarter plan to internal team, investors, or customers.
- Multiple stakeholders need a single source of truth linking strategy → themes → initiatives.
- Choosing between roadmap formats — use the selection matrix.
- Onboarding a new contractor or PM who needs a one-page direction document.

## When NOT To Use

- Less than 4 weeks of work — roadmap overhead exceeds value; use a sprint plan or release notes.
- Pure exploration phase before PMF — explicit roadmaps create anchors that bias discovery.
- Highly volatile environments (hackathon, week-by-week pivots) — keep a backlog.
- Feature commitment to a single customer — that is a contract, not a roadmap.

## Content

| File | What's inside |
|------|---------------|
| `content/01-formats.xml` | Four roadmap types with selection matrix (uncertainty, external-sharing, commitment level, team maturity). |
| `content/02-process.xml` | Five-step design process: strategy input, format selection, theme definition, horizon population with confidence levels, stakeholder context. |
| `content/03-rules.xml` | Concrete rules: initiative-to-objective linking, confidence distribution targets, "not doing" as required field, two-artefact publishing, update cadence. Agent gotchas from agent-integration.md. |
| `content/04-examples.xml` | B2B SaaS and solo product Now-Next-Later examples. Antipatterns with fixes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/now-next-later.md` | Now-Next-Later roadmap with vision, themed initiative slots, confidence levels, dependencies, success metrics. |
| `templates/quarterly-outcome.md` | Quarterly outcome roadmap with objectives, initiatives by theme, explicit not-doing, risks, review schedule. |
| `templates/external-roadmap.md` | Customer-facing roadmap: benefits language, no confidence levels or owners, subject-to-change disclaimer. |
| `templates/lint-roadmap.py` | Python validator: checks required keys, Now initiative count, not_doing presence, confidence and objective_id per initiative. |
