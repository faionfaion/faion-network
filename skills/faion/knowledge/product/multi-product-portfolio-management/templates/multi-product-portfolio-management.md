<!--
purpose: Markdown skeleton for a Multi Product Portfolio Management artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/multi-product-portfolio-management.json.
token-budget-impact: ~250 tokens.
-->

# Multi Product Portfolio Management — &lt;artefact_id&gt;

- **operator** (string): &lt;named portfolio owner&gt;
- **products** (array): &lt;≥3 product objects (name, mode, mrr, traffic, time_budget_hours, capital_allocation_usd)&gt;
- **cross_product_kill_rule** (string): &lt;explicit rule string&gt;
- **quarterly_review_at** (string): &lt;ISO datetime&gt;
- **total_weekly_time_cap** (number): &lt;hours ≤40&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
