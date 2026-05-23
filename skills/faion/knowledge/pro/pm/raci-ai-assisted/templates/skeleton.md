<!-- purpose: RACIMatrix skeleton mapping WBS leaves to R/A/C/I roles -->
<!-- consumes: WBS spec + roster + charter -->
<!-- produces: scaffold consumed by raci-assign-A -->
<!-- depends-on: content/01-core-rules.xml#r2-bounded-output -->
<!-- token-budget-impact: ~150 tokens -->

# RACI Matrix — [Project]

**Owner:** [role] / [person]
**Trigger:** kickoff | roster_delta | quarterly_review
**Last reviewed:** YYYY-MM-DD (within 90 days)
**Version:** [semver]

| WBS id | Deliverable | Responsible | Accountable (exactly one) | Consulted | Informed | Evidence |
|--------|-------------|-------------|----|-----------|----------|----------|
| 1.1    | Planning Documentation | [pm-handle] | [pm-lead] | [sponsor] | [team]  | charter#planning |
| 2.1    | Login Endpoint | [be-eng]     | [be-lead]  | [security] | [PM]   | wbs-dict#2.1 |

<!-- Rules:
- Exactly one Accountable per row.
- Responsible must not be empty.
- Evidence must point to charter line, WBS dictionary entry, or stakeholder register row.
- Trigger must be named (no "when needed").
-->
