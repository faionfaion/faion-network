<!--
purpose: Markdown skeleton for a Substack-to-Product Funnel artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/substack-to-product-funnel.json.
token-budget-impact: ~250 tokens.
-->

# Substack-to-Product Funnel — &lt;artefact_id&gt;

- **operator** (string): &lt;named publication owner&gt;
- **publication_url** (string): &lt;Substack URL&gt;
- **paid_tier** (object): &lt;{name, monthly_price, annual_price, concrete_benefit}&gt;
- **recommendation_partners** (array): &lt;≥3 publications with URL + agreement_at&gt;
- **cross_post_cadence** (object): &lt;{per_month, partner_rotation}&gt;
- **welcome_sequence** (array): &lt;5 emails; email 4 carries the hard-product CTA&gt;
- **hard_product_url** (string): &lt;URL&gt;
- **hard_product_cta_text** (string): &lt;≤140 chars&gt;
- **kpi_set** (object): &lt;{free_subs, paid_subs, hard_product_conversions, recommendation_inflow}&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
