# PMBoK 8 Five Focus Areas

## Summary

PMBoK 8 replaces the rigid five Process Groups with five Focus Areas (Initiating, Planning, Executing, Monitoring and Controlling, Closing) distributed across seven Performance Domains. The 40 non-prescriptive processes are a tailorable menu, not a checklist. The same five focus areas apply to both predictive and agile delivery; only the artefacts change (charter vs vision; WBS vs backlog; work packages vs sprints; EVM vs velocity; final report vs retrospective).

## Why

Process Groups from PMBoK 6 implied a strict sequential lifecycle that does not fit agile or hybrid delivery. About 80% of practitioners requested their reintroduction as foundational concepts, but as flexible focus areas rather than mandatory phases. The 5 x 7 matrix (focus areas x performance domains) makes tailoring explicit: fill only the cells the project needs, drop the rest.

## When To Use

- Structuring a project plan in PMBoK 8 vocabulary when sponsors expect process-group-style reporting
- Mapping 40 non-prescriptive processes onto a project (select the applicable subset)
- Cross-walking a PMBoK 6 plan into PMBoK 8 vocabulary without losing artefacts
- Building per-focus-area stage-gate checklists for steering-committee reviews
- Tailoring per delivery approach with the same temporal structure

## When NOT To Use

- Pure-Scrum teams whose entire framework is the Scrum Guide — focus areas add a meta-layer with no benefit
- Single-team continuous delivery where Initiating and Closing collapse into a release note
- Agile-coaching contexts where "process" language alienates the team
- PMBoK 7 purist environments not yet adopting PMBoK 8 — vocabulary drift creates confusion

## Content

| File | What's inside |
|------|---------------|
| `content/01-focus-areas.xml` | Five focus areas with predictive vs agile artefact mapping; 40 non-prescriptive processes overview |
| `content/02-rules.xml` | Rules for tailoring, artefact mapping, and avoiding common agent errors (phase confusion, Closing skip, process overload) |

## Templates

| File | Purpose |
|------|---------|
| `templates/lifecycle-matrix.md` | 5 x 7 focus-area x domain matrix template for tailoring |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/matrix-to-checklist.py` | Convert filled lifecycle-matrix YAML into per-focus-area stage-gate checklists |
