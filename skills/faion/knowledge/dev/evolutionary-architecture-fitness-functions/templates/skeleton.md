<!--
purpose: Canonical skeleton for the `evolutionary-architecture-fitness-functions` suite spec — one block per fitness function plus the suite-level dependency graph, results store and review.
consumes: The characteristics worth guarding, the intended layer graph, one baseline measurement per function, and an owner per function.
produces: A committed suite spec at .product/evolutionary-architecture-fitness-functions/<suite_id>.md, mirrored as JSON for scripts/validate-evolutionary-architecture-fitness-functions.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-evolutionary-architecture-fitness-functions.py.
token-budget-impact: ~900 tokens to fill for a three-function suite.
-->
---
version: 0.1.0
suite_id: <suite_id>
owner: <suite_owner>
last_reviewed: <last_reviewed_date>
---

# Suite

- suite_id: <suite_id>
- system: <system_name>
- owner: <suite_owner>

# Dependency graph

Written here, not only in the tool config (r-ff-structural-dependency-function).

- layers: <layers>
- allowed_edges: <allowed_edges>

# Results store

Every run records its measured value, keyed by function id and commit (r-ff-results-trended).

- location: <results_store_location>
- keyed_by: function_id, commit
- retention_days: <retention_days>

# Review

- cadence: <cadence>
- last_reviewed_at: <last_reviewed_date>
- next_review_at: <next_review_date>

# Functions

Repeat the block below once per function. The first block is the structural function (`kind: structural`); manual functions stay under one fifth of the suite.

## <function_id>

- characteristic: <characteristic>
- metric: <metric_name>
- unit: <unit>
- kind: <kind>
- mode: <mode>
- tool: <tool_name>
- command: `<command>`
- threshold: <threshold_operator> <threshold_value>
- baseline: <baseline_value> measured <baseline_date>
- threshold_mode: <threshold_mode>
- absolute_from: <date or condition; required when threshold_mode is ratchet>
- consequence: <consequence>
- trigger: <trigger>
- scope: <scope>
- owner: <function_owner>
- consecutive_red_reviews: 0
- action: <fix | rebaseline | delete; required once consecutive_red_reviews reaches 2>
