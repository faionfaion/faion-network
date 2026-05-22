<!--
purpose: one-page picker checklist for AI UX patterns
consumes: feature classification (ui_surface, refusal_possible, irreversible)
produces: mandatory + optional pattern set per feature
depends-on: content/06-decision-tree.xml
token-budget-impact: ~300 tokens when rendered
-->
# AI UX Pattern Picker — {{feature_name}}

| Axis | Value |
|---|---|
| ui_surface | {{ui_surface}} |
| refusal_possible | {{refusal_possible}} |
| irreversible | {{irreversible}} |

## Pattern set

| # | Pattern | Mandatory? | Surface | Component |
|---|---|---|---|---|
| 1 | confidence_indicator | {{p1_mand}} | {{p1_surface}} | {{p1_component}} |
| 2 | refusal_surface | {{p2_mand}} | {{p2_surface}} | {{p2_component}} |
| 3 | edit_handoff | {{p3_mand}} | {{p3_surface}} | {{p3_component}} |
| 4 | why_trail | {{p4_mand}} | {{p4_surface}} | {{p4_component}} |
| 5 | undo_gate | {{p5_mand}} | {{p5_surface}} | {{p5_component}} |
| 6 | progressive_disclosure | optional | {{p6_surface}} | {{p6_component}} |
| 7 | batch_operations | optional | {{p7_surface}} | {{p7_component}} |

Designer: `{{design_owner}}`
Reviewed: `{{review_date}}`
