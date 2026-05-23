# Stakeholder Engagement

## Summary

**One-sentence:** Identify, classify, and engage every stakeholder via a YAML register grounded in observable evidence, with quadrant-based cadence and tracked current-vs-desired engagement levels.

**One-paragraph:** Stakeholder engagement classifies stakeholders into a power × interest quadrant (manage_closely / keep_satisfied / keep_informed / monitor) and assigns a cadence per quadrant. Each entry records desired vs current engagement level (unaware / resistant / neutral / supportive / leading) plus an evidence citation (minutes, ticket, signed sign-off). The methodology produces a versioned YAML register reviewed weekly with overdue stakeholders flagged automatically.

**Ефективно для:**

- Programmes with sponsor + steering + delivery stakeholder triangle.
- Cross-vendor work where stakeholders span ownership boundaries.
- Regulated environments requiring evidence of stakeholder sign-off.
- Distressed projects where misalignment is a leading cause of slip.

## Applies If (ALL must hold)

- Programme has sponsor + steering + delivery stakeholder layers.
- Cross-vendor work needs evidence of engagement per role.
- Regulated context requires audit-trail of stakeholder sign-offs.
- Project shows political misalignment symptoms.

## Skip If (ANY kills it)

- Solo project with no external stakeholder pressure.
- Pure-Scrum team with PO carrying all stakeholder weight.
- One-week spike — engagement ritual cost exceeds value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder list | interview notes / org chart | kickoff |
| Charter | signed PDF / MD | sponsor |
| Communication-plan template | MD | comms |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-register` | Static register populated before engagement scheduling. |
| `stakeholder-engagement-advanced` | Differentiated strategies build on quadrant classification. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — quadrant per stakeholder, evidence per entry, cadence per quadrant, current-vs-desired, overdue flag | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for engagement-register artefact | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: identify → classify → set cadence → engage → review | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping engagement state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-quadrant` | sonnet | Needs judgment on power/interest signals. |
| `draft-cadence-plan` | haiku | Template fill from quadrant rules. |
| `synthesise-misalignment-report` | opus | Cross-stakeholder synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/engagement-register.yaml` | YAML register with quadrant + cadence + evidence. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stakeholder-engagement.py` | Schema-validate engagement register JSON. | Pre-commit + weekly review. |
| `scripts/engagement-due.py` | Flag stakeholders overdue per quadrant cadence. | Weekly cron. |

## Related

- [[stakeholder-register]]
- [[stakeholder-engagement-advanced]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the stakeholder-engagement input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
