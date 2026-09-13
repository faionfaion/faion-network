<!--
purpose: Canonical skeleton for the `fitness-function-suite-bootstrap` starter suite spec — 5 to 8 functions, one block each, plus the dependency graph, launch date and four weekly reviews.
consumes: One critical endpoint, the CI system, the package layout, the published API definition, and one baseline measurement per function.
produces: A committed suite spec at .product/fitness-function-suite-bootstrap/<suite_id>.md, mirrored as JSON for scripts/validate-fitness-function-suite-bootstrap.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-fitness-function-suite-bootstrap.py.
token-budget-impact: ~1200 tokens to fill for a five-function suite.
-->
---
version: 0.1.0
suite_id: <suite_id>
owner: <suite_owner>
launch_date: <launch_date>
---

# Suite

- suite_id: <suite_id>
- system: <system_name>
- owner: <suite_owner>
- launch_date: <launch_date>
- cadence_after_week_four: <cadence_after_week_four>

# Dependency graph

Written here, not only in the tool config (r-ffsb-dependency-direction-tool).

- layers: <layers>
- allowed_edges: <allowed_edges>

# Weekly reviews

Four entries at seven-day intervals from launch_date (r-ffsb-owner-and-weekly-review). Fill red_functions and actions at each review.

- week 1: <week1_date> reviewed_by <reviewer> red_functions: <ids> actions: <one line per action>
- week 2: <YYYY-MM-DD> reviewed_by <role:handle> red_functions: <ids> actions: <one line per action>
- week 3: <YYYY-MM-DD> reviewed_by <role:handle> red_functions: <ids> actions: <one line per action>
- week 4: <YYYY-MM-DD> reviewed_by <role:handle> red_functions: <ids> actions: <one line per action>

# Functions

5 to 8 blocks, at least one per category: performance, deployability, dependency, complexity, contract. Every block launches as informational or ratchet; `promotion` is filled only when mode becomes blocking (r-ffsb-ratchet-first-then-block).

## <function_id>

- category: <category>
- tool: <tool_name>
- command: `<command>`
- threshold: <threshold_operator> <threshold_value> <unit>
- baseline: <baseline_value> measured <baseline_date>
- mode: <mode>
- runs_on: <runs_on>
- owner: <function_owner>
- consecutive_red_reviews: 0
- action: <fix | rebaseline | remove; required once consecutive_red_reviews reaches 2>
- promotion: <green_runs_on_main (at least 5), approved_by, review_date, promoted_at; required when mode is blocking>
- performance only: endpoint <METHOD /path>, load_profile <versioned path>, runner_kind <dedicated-runner | dedicated-environment>; runs_on must be post_merge or nightly
- deployability only: metric <pipeline_duration | merge_to_production_lead_time>, script_path <committed script>; threshold unit is minutes
- complexity only: per_function_limit <10 by default>, baseline_file <committed list of current violators>
- contract only: method <pact | schema-diff>, consumers <names> or released_schema_ref <URL or path>
