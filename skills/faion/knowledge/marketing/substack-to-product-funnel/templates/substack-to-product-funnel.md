<!--
purpose: Markdown skeleton for a Substack-to-Product Funnel artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/substack-to-product-funnel.json.
token-budget-impact: ~250 tokens.
-->

# Substack-to-Product Funnel — <artefact_id>

- **operator** (string): <named_publication_owner>
- **publication_url** (string): <substack_url>
- **paid_tier** (object): <{name, monthly_price, annual_price, concrete_benefit}>
- **recommendation_partners** (array): <≥3 publications with URL + agreement_at>
- **cross_post_cadence** (object): <{per_month, partner_rotation}>
- **welcome_sequence** (array): <5 emails; email 4 carries the hard-product CTA>
- **hard_product_url** (string): <url>
- **hard_product_cta_text** (string): <≤140 chars>
- **kpi_set** (object): <{free_subs, paid_subs, hard_product_conversions, recommendation_inflow}>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
