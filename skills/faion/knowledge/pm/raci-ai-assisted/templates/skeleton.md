<!-- purpose: RACIMatrix skeleton mapping WBS leaves to R/A/C/I roles -->
<!-- consumes: WBS spec + roster + charter -->
<!-- produces: scaffold consumed by raci-assign-A -->
<!-- depends-on: content/01-core-rules.xml#r-rows-bind-to-wbs-leaves -->
<!-- token-budget-impact: ~150 tokens -->

# RACI Matrix — <project>

**Owner:** <owner_role> / <owner_full_name>
**Status:** draft | published
**Trigger:** kickoff | roster_delta | quarterly_review
**Last reviewed:** YYYY-MM-DD (within 90 days)
**Version:** <document_version>

## Roster (as of last reviewed)

| Role id | Person |
|---------|--------|
| <pm_lead> | <pm_handle> |

## Open WBS leaves

1.1, 2.1

## Rows (one per open leaf)

| WBS id | Deliverable | Responsible | Accountable (exactly one) | Consulted | Informed | Evidence | Status |
|--------|-------------|-------------|----|-----------|----------|----------|--------|
| 1.1    | Planning Documentation | <pm_handle> | <pm_lead> | <sponsor> | <team>  | charter#planning | anchored |
| 2.1    | Login Endpoint | [be-eng]     | [be-lead]  | <security> | <pm>   | wbs-dict#2.1 | anchored \| proposed \| orphaned |

## Roster delta (only when trigger = roster_delta)

- change: join | leave | role_change; role: ...; person: ...; effective date: YYYY-MM-DD; refresh deadline: last day (leave / role_change) or first week (join)
- rows changed: ...; rows orphaned: ...; rows reassigned (wbs id, column, role, anchor): ...

## Review log

| Reviewed at | Kind | Notification (channel, sent on, recipients with rows) / counts (removed, reassigned, still proposed) |
|-------------|------|--------|
| YYYY-MM-DD  | publish \| quarterly_review | ... |

<!-- Rules:
- Exactly one Accountable per row; a role id from the roster, never "team" / "tbd" / a pair.
- Responsible must not be empty; every role id must be in the roster; one column per role per row.
- Evidence must point to charter#section, wbs-dict#id or stakeholders#row; no anchor = status proposed = not published.
- Trigger must be named (no "when needed"); a roster delta is refreshed by the last day / first week.
- Publish sends every R / A holder their rows and records channel, date and rows in the review log.
-->
