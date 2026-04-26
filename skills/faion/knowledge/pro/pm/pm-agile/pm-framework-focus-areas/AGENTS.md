# PMBOK 8 Focus Areas

## Summary

PMBOK 8 replaces Process Groups with five method-agnostic Focus Areas — Initiating, Planning, Executing, Monitoring & Controlling, Closing — distributed across 40 non-prescriptive processes. Focus areas answer "when in the project lifecycle" (orthogonal to the seven performance domains which answer "what area of work"). Teams tailor which focus areas need full treatment vs. light coverage based on project type, size, and regulatory regime.

## Why

Process groups from PMBOK 6 implied a sequential, waterfall flow that felt alien to agile and iterative teams. Focus areas preserve the lifecycle anchors (start, middle, close) without prescribing execution order — allowing Scrum sprints to map into Executing while planning happens iteratively inside each sprint rather than once upfront.

## When To Use

- Replacing PMBOK 6 process groups in PMO documentation; focus areas are method-agnostic.
- Mapping agile ceremonies to a process-group equivalent for stakeholders trained on PMBOK 6.
- Building a project audit rubric — each focus area becomes one section.
- Onboarding new PMs from PMP-aligned curricula since 2023.
- Tailoring conversations: "what's required at each focus area for this project size?"

## When NOT To Use

- Pure agile teams that already operate with Scrum/Kanban events — overlaying focus areas adds bureaucracy.
- Highly regulated environments still mandating PMBOK 6 process groups verbatim.
- Day-to-day execution detail — focus areas are framework-level, not task-level.
- Single-person solo work — overhead exceeds value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-focus-areas.xml` | All five focus areas with purpose, agile-to-focus-area mapping, and common failure modes. |
| `content/02-tailoring.xml` | Tailoring rules by project type/size, interaction with seven performance domains, anti-patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scaffold_focus_areas.sh` | Shell script: creates a docs/ tree with one folder and default artifacts per focus area. |
