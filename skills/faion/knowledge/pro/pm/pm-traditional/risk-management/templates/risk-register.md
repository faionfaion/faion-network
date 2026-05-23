<!-- purpose: Risk register markdown template (PMBoK-aligned, EMV-ready) -->
<!-- consumes: project charter, WBS, vendor SOWs, historical risk archive -->
<!-- produces: artefact conforming to content/02-output-contract.xml schema -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~600-1500 tokens when fully populated -->

# Risk Register — <project name>

> Owner: <name>  •  Review cadence: weekly  •  Last review: YYYY-MM-DD

| ID    | Description                  | Category | P (VL-VH) | I (VL-VH) | Score | Strategy | Owner    | Trigger condition          | Source artefact         | Status  |
|-------|------------------------------|----------|-----------|-----------|-------|----------|----------|----------------------------|-------------------------|---------|
| R-001 | Key developer leaves         | people   | M         | H         | 0.18  | mitigate | name     | resignation notice filed   | hr-attrition-table.md   | active  |
| R-002 | Vendor API breaking change   | vendor   | L         | H         | 0.06  | transfer | name     | vendor changelog cite      | contract-sow-v2.pdf     | active  |

## Closed risks (audit trail)

| ID    | Outcome                                          | Closed on   |
|-------|--------------------------------------------------|-------------|
| R-000 | passed without triggering                        | YYYY-MM-DD  |
