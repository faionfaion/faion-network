<!--
purpose: Canonical skeleton for the `rfc-template-product-dev-team` RFC — measured problem, options with rejection reasons, enumerated blast radius, tested rollback, dated milestones inside six weeks, named reviewers, status, and the outcome review.
consumes: The metric dashboard, the service map, the staging rollback run, the calendar, and reviewer comments.
produces: A committed RFC at .product/rfc-template-product-dev-team/<rfc_id>.md, mirrored as JSON for scripts/validate-rfc-template-product-dev-team.py.
depends-on: templates/header.yaml, content/02-output-contract.xml, scripts/validate-rfc-template-product-dev-team.py.
token-budget-impact: ~1100 tokens to fill end-to-end.
-->
---
version: 0.1.0
rfc: <rfc_id>
owner: <owner>
status: <status>
shared_on: <shared_on>
---

# RFC

- id: <rfc_id>
- title: <title>
- author: <owner>
- shared_on: <shared_on>

# Problem

State the measured current value, the target and the date. Name no solution here.

- metric: <metric_name>
- current_value: <metric_baseline>
- target_value: <metric_target>
- by_date: <by_date>
- statement: <problem_statement>

# Options

At least two; exactly one chosen; every other carries a rejection reason tied to the metric, cost or risk.

- <chosen_option> (chosen)
- <rejected_option> (rejected: <rejection_reason>)
- do nothing / keep current behaviour (rejected: <reason>)

# Blast radius

One line per service, data store, API, scheduled job and user segment; counts for APIs and segments; an owner each (every owner becomes a reviewer).

- <kind> <name> owner <role:handle> count <n percent of traffic | n tenants | n consumers>
- schema_change: <true | false>
- public_api_change: <true | false>
- data_backfill: <true | false>
- third_party_change: <true | false>

# Rollback

- mechanism: <rollback_mechanism>
- execute_minutes: <rollback_minutes>
- executor: <rollback_executor>
- staging_run: exercised <true | false>, url <run URL> or reason <why not>
- points_of_no_return: <irreversible step> -> pre_check <the check that runs immediately before it>

# Milestones

At least two dated increments inside 42 days; the last is the ship date.

- <milestone_1_date>: <milestone_1_increment>
- <ship_date>: <ship_increment> (ship)

# Reviewers

Named people from the blast radius; `role:handle`; deadline at least 3 working days after shared_on.

- <role:handle> commented <true | false>
- comment_deadline: <comment_deadline>

# Decision

- status: <status>
- decided_on: <YYYY-MM-DD>
- decision: <decision_statement>
- supersession: superseded_by <URL or null>, supersedes <URL or null>

# Evidence

- <metric_url>
- <staging rollback run URL>
- <successor or predecessor RFC when superseded>

# Review

- next_review_at: <next_review_date> (no later than 42 days after ship)
- outcome: remeasured_value <n>, same_method true, result <met | partially-met | not-met>, url <dashboard or query>, reviewed_on <YYYY-MM-DD>
