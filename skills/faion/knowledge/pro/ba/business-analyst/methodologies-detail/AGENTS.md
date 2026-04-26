# BA Methodologies Detail

## Summary

A catalog of 12 enterprise BA frameworks used in BABOK Knowledge Areas 1-6: governance, communication planning, elicitation preparation, requirements maintenance, change impact analysis, current state analysis, future state definition, risk analysis, change strategy planning, requirements architecture, solution options analysis, and solution limitation assessment. Also includes the BABOK 50-technique reference table. Use this as a routing index — classify the user request into one or more of the 12 frameworks, then load content and apply the appropriate template.

## Why

Enterprise BA engagements require explicit decision-making processes (governance), communication strategies, structured state analysis, and scored option comparisons. Without a catalog, agents pick the familiar framework (usually requirements modeling from KA-5) and skip governance, communication, and strategy frameworks that have equal importance but lower LLM visibility. The 50-technique table provides a controlled vocabulary for technique selection.

## When To Use

- Project kickoff: selecting which of the 12 BA frameworks to run for this initiative.
- Mid-project routing: mapping a stakeholder question to the right BABOK technique before drafting a deliverable.
- Audit or handover: producing a BA artifact inventory showing which frameworks were applied and which are missing.
- Training a new analyst or agent on the catalog of techniques and their fit.

## When NOT To Use

- A single well-scoped deliverable with a known framework — go directly to the dedicated methodology folder.
- Lightweight startup or single-feature work — the 12-framework set assumes enterprise or multi-stakeholder context.
- Pure agile teams with story mapping and backlog grooming — governance, change control, and requirements architecture frameworks often duplicate Scrum ceremonies.

## Content

| File | What's inside |
|------|---------------|
| `content/01-frameworks.xml` | Twelve BA frameworks: purpose, four-step process, and template structure for each. Governance through solution limitation assessment. |
| `content/02-techniques.xml` | BABOK 50-technique reference table mapping technique to primary use cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/governance-framework.md` | Decision authority matrix and change control process template. |
| `templates/communication-plan.md` | Audience matrix and key messages template. |
| `templates/change-impact.md` | Change impact analysis template: scope, effort, risks, recommendation. |
| `templates/current-state.md` | Current state assessment: business context, capability assessment, SWOT. |
| `templates/future-state.md` | Future state vision: goals, capability roadmap, constraints, assumptions. |
| `templates/risk-register.md` | Risk register with probability, impact, score, response, and owner. |
| `templates/change-strategy.md` | Gap analysis, solution options comparison, and transition roadmap template. |
| `templates/requirements-architecture.md` | Viewpoints, requirement hierarchy, and dependency table template. |
| `templates/solution-options.md` | Weighted scoring matrix and recommendation template. |
| `templates/solution-limitations.md` | Limitation identification, root cause, impact, and remediation template. |
| `templates/ba-route.sh` | Classifier script routing a user request to frameworks and BABOK technique numbers. |
