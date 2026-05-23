---
slug: pm-tool-selection
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Structured tool-evaluation framework: scope requirements, 5-dimension scorecard (ecosystem, governance, integrations, agent-API, TCO), 3-vendor bake-off, decision record with reversal trigger.
content_id: "4d5e6f7a8b9c0d1e"
complexity: medium
produces: decision-record
est_tokens: 4200
tags: [pm-tools, evaluation, procurement, tco, decision-making]
---
# PM Tool Selection

## Summary

**One-sentence:** Structured tool-evaluation framework: scope requirements, 5-dimension scorecard (ecosystem, governance, integrations, agent-API, TCO), 3-vendor bake-off, decision record with reversal trigger.

**One-paragraph:** Structured tool-evaluation framework: scope requirements, 5-dimension scorecard (ecosystem, governance, integrations, agent-API, TCO), 3-vendor bake-off, decision record with reversal trigger.

**Ефективно для:**

- PMO, що уперше консолідує tool-портфоліо.
- Стартапів, що switched з task-app на full PM platform.
- Agency-ів, що obliquely вибирають tool під клієнта.
- Команд після M&A, де треба merge tool stacks.

## Applies If (ALL must hold)

- Team has ≥10 active PM users.
- Tooling budget ≥3k/yr is committed.
- Switching cost is acceptable (data migration plan exists).
- Decision-maker is named and has authority.

## Skip If (ANY kills it)

- &lt;10 PM users — task-app or shared spreadsheet suffices.
- Vendor contract locked-in beyond decision horizon.
- Existing tool meets &gt;80% of needs — stay and refactor.
- No identified pain — premature optimisation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cross-tool-migration]] | Migration plan triggered if decision is to switch. |
| [[change-control]] | Tool switch is a controlled change. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `requirements-author` | sonnet | Translate pain into scoped requirements. |
| `scorecard-builder` | sonnet | Build 5-dimension scorecard with weights. |
| `bake-off-runner` | opus | Drive 3-vendor evaluation week. |
| `decision-record-author` | sonnet | Author final decision record with reversal trigger. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scorecard.yaml` | 5-dimension scorecard with per-dimension weight. |
| `templates/decision-record.md` | ADR-style decision with context, options, decision, consequences, reversal. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tool-selection.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[azure-devops-boards]]
- [[jira-workflow-management]]
- [[gitlab-boards]]
- [[cross-tool-migration]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (active_users, budget_band, current_tool_satisfaction) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
