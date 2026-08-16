<!-- purpose: Single work-package Dictionary card. -->
<!-- consumes: stakeholder register + sized leaf + scope statement -->
<!-- produces: one dictionary[] entry in the WBS spec -->
<!-- depends-on: content/01-core-rules.xml#dictionary-required -->
<!-- token-budget-impact: ~130 tokens -->

# WBS Dictionary Entry

## WBS [X.X.X] — <work_package_name>

| Field               | Value |
|---------------------|-------|
| Parent              | [Parent WBS ID and Name] |
| Description Included | [What IS in scope] |
| Description Excluded | [What is NOT in scope — explicit] |
| Deliverable         | <tangible_output_produced> |
| Acceptance Criteria | [Observable, testable conditions — not "looks good"] |
| Owner               | [Role or named team — exactly one; UNRESOLVED if not in stakeholder register] |
| Effort Estimate     | [Hours — strictly 8-80] |
| Dependencies        | <predecessor_wbs_ids> |
| Notes               | [Risks, assumptions, constraints] |

<!--
Rules:
- Acceptance criteria are observable and testable.
- Owner from stakeholder register or UNRESOLVED.
- effort_hours strictly in [8,80].
- No dates here; schedule is separate.
-->
