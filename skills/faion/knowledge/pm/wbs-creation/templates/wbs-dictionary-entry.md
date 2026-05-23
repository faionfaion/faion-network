<!-- purpose: Single work-package Dictionary card with all required fields. -->
<!-- consumes: stakeholder register + sized leaf + scope statement -->
<!-- produces: one dictionary[] entry per leaf in the WBS spec -->
<!-- depends-on: content/01-core-rules.xml#dictionary-required -->
<!-- token-budget-impact: ~120 tokens -->

# WBS Dictionary Entry

| Field               | Value              |
|---------------------|--------------------|
| WBS ID              | [X.X.X]            |
| Name                | [Work Package Name — noun phrase] |
| Description / Included | [What is in scope for this leaf] |
| Description / Excluded | [What is explicitly NOT in scope] |
| Deliverable         | [Tangible output produced] |
| Acceptance Criteria | [Observable, testable conditions for done — at least one] |
| Owner               | [Role or named team — exactly one accountable; UNRESOLVED if not in stakeholder register] |
| Effort Estimate     | [Hours — must be in [8, 80]] |
| Dependencies        | [Predecessor WBS IDs] |
| Notes               | [Risks, assumptions, constraints] |

<!--
Rules:
- Owner MUST come from the stakeholder register; UNRESOLVED if missing.
- Acceptance criteria are observable and testable; "looks good" rejected.
- Effort_hours strictly 8-80.
- No dates in this card; schedule is a separate artefact.
-->
