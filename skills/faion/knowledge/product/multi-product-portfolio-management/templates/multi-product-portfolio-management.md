<!--
purpose: Markdown skeleton for a Multi Product Portfolio Management artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/multi-product-portfolio-management.json.
token-budget-impact: ~250 tokens.
-->

# Multi Product Portfolio Management — <artefact_id>

- **operator** (string): <named portfolio owner>
- **products** (array): <≥3 product objects (name, mode, mrr, traffic, time_budget_hours, capital_allocation_usd)>
- **cross_product_kill_rule** (string): <explicit rule string>
- **quarterly_review_at** (string): <ISO datetime>
- **total_weekly_time_cap** (number): <hours ≤40>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
