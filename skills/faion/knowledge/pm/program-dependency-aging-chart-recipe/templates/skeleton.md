<!--
purpose: Checkpoint page for the weekly dependency aging chart: header with query and extraction time, adopted bands, the sorted action table with owner and due date per escalated edge, re-baseline decisions, and the SLE line.
consumes: the validated JSON artefact matching content/02-output-contract.xml and the script-generated chart image
produces: the page shown at the weekly checkpoint; one per chart_date
depends-on: content/02-output-contract.xml for field names; content/04-procedure.xml step 8
token-budget-impact: ~400 tokens per week with five to ten edges; ~200 to validate the JSON behind it
-->

---
program: <project_name>
owner: <owner_role>:<owner_handle>   # the program PM; a person, never a team
chart_date: <artefact_date>              # the checkpoint weekday
checkpoint_weekday: <Monday..Sunday>
tracker_query: <tracker_query>
extracted_at: <extracted_at>             # within the checkpoint week
age_bands: 0-7 | 8-14 | 15-28 | over 28     # fixed at bands_adopted_on; never re-cut
bands_adopted_on: <YYYY-MM-DD>
---

# Dependency aging chart

![blocked tasks vs days since opened](<chart_image>)

SLE (p85 of resolved ages, trailing 12 weeks): <N days | insufficient data (fewer than 10 resolved)>

# Action table

Sorted: non-positive slack first (red), then band descending, then blocked tasks descending.

| Link | Producer -> consumer | Type | Opened | Age (days) | Band | Blocked tasks | Needed by | Slack (days) | Action (owner, due date) |
|---|---|---|---|---|---|---|---|---|---|
| <LINK-1> | <team> -> <team> | <api-contract / shared-component / data-feed / infrastructure / review-approval / environment> | <YYYY-MM-DD> | <n> | <band> | <n> | <YYYY-MM-DD or no-deadline> | <n or -> | <verb phrase>, <role:handle>, <YYYY-MM-DD> |

# Re-baseline decisions (top band)

- <LINK> — <move-milestone / cut-scope / swap-producer> — decided by <program PM> on <YYYY-MM-DD> — <note>

# Re-ticketed edges

- <NEW-LINK> superseded_from <OLD-LINK>, opened_at inherited <YYYY-MM-DD>

# Resolved this week

- <LINK> — opened <YYYY-MM-DD>, resolved <YYYY-MM-DD>, <n> days, <delivered / not-needed>
