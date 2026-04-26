# BA Governance

## Summary

Establishes decision rights, change control, and communication planning for requirements work. Three-component methodology: governance framework (decision-authority matrix, change-control flow, prioritization rules), communication planning (audience matrix, channel selection, feedback mechanisms), and elicitation preparation (technique selection by information type). BABOK KA-1 Planning operational layer.

## Why

Requirements processes without explicit governance produce stuck change requests, scope drift, and sign-off ambiguity. A decision-authority matrix with explicit escalation paths prevents the most common failure mode: every change escalating to steering committee because impact thresholds are undefined. Communication plans without feedback mechanisms become write-only channels within weeks.

## When To Use

- Setting up decision rights, change control, and approval workflow for a new product or squad before requirements work starts.
- Projects crossing three or more stakeholder groups (sponsor, dev, ops, legal/compliance) that need a communication plan.
- Preparing elicitation logistics and technique selection before interviews or workshops begin.
- Auditing an existing requirements process where rework, scope drift, or sign-off ambiguity has been observed.
- Regulated builds (SOX, HIPAA, GDPR) where a decision audit trail is mandatory.

## When NOT To Use

- Solo founder / single-team early MVP — formal governance burns time you do not have; use lightweight requirements-prioritization instead.
- Pure engineering refactors with no external stakeholders — governance overhead is waste; rely on PR review.
- Research spikes and discovery sprints where the goal is learning, not committing scope.
- Crisis incidents — use incident command, not governance workflow.

## Content

| File | What's inside |
|------|---------------|
| `content/01-governance-framework.xml` | Decision rights definition, change control process, prioritization rules, approval documentation requirements. |
| `content/02-communication-and-elicitation.xml` | Audience analysis, channel selection, feedback mechanisms, technique selection guide by information type. |

## Templates

| File | Purpose |
|------|---------|
| `templates/governance.md` | Governance artifact skeleton with decision-authority matrix, change-control steps, and communication audience matrix. |
| `templates/scaffold-governance.sh` | Bash script that generates a governance.md skeleton under .aidocs/in-progress/. |
