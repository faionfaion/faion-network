# PM Tools Comparison

## Summary

A structured framework for evaluating and selecting project management tools through a weighted scoring matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%), a two-week proof-of-concept protocol, total cost of ownership (TCO) analysis, and an ADR template for recording the decision. Covers Jira, Linear, ClickUp, GitHub Projects, GitLab Boards, Azure DevOps, Notion, Trello, and Asana.

## Why

PM tool evaluations fail from anchor bias (the evaluator's preferred tool scores highest) and TCO underestimation (migration + custom reporting routinely doubles the projected cost). A pre-defined weighted matrix with measured PoC data — not vendor marketing — and a forced-rank step prevents score inflation and produces a defensible, auditable decision.

## When To Use

- Selecting an initial PM tool for a new team or product.
- Re-evaluating an existing tool when pain points (speed, cost, integrations) accumulate.
- Building an ADR for a board or leadership review with quantitative scoring.
- Mid-migration sanity check: confirm the chosen tool actually scores higher on what mattered.

## When NOT To Use

- Single-person projects — overhead exceeds gain; use whatever is already available.
- When the org has a mandated tool (e.g., Jira via enterprise contract) and switching is not on the table.
- Hotfix or firefighting periods — tool selection should not be the response to delivery problems.

## Content

| File | What's inside |
|------|---------------|
| `content/01-scoring.xml` | Weighted scoring matrix, category definitions, and reference scores for five major tools. |
| `content/02-process.xml` | PoC protocol, TCO calculator structure, decision matrix, and agent gotchas. |
| `content/03-examples.xml` | Worked ADR (Jira → Linear decision), vendor comparison presentation template. |

## Templates

| File | Purpose |
|------|---------|
| `templates/evaluation-scorecard.md` | Per-tool evaluation scorecard: setup, daily usage, team features, reporting. |
| `templates/tco.yaml` | TCO calculation template: direct, indirect, hidden costs with three-year total. |
| `templates/weighted_score.py` | Script: computes weighted totals from a YAML scorecard file. |
