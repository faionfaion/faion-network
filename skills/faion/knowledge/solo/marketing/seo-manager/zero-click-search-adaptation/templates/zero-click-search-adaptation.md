<!--
purpose: Markdown skeleton for a Zero-Click Search Adaptation artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/zero-click-search-adaptation.json.
token-budget-impact: ~250 tokens.
-->

# Zero-Click Search Adaptation — &lt;artefact_id&gt;

- **page_url** (string): &lt;the canonical URL receiving the citation spec&gt;
- **target_query** (string): &lt;the head query the page targets&gt;
- **owner** (string): &lt;single named accountable owner (handle/email)&gt;
- **jsonld_article** (object): &lt;valid schema.org Article JSON-LD&gt;
- **jsonld_faq** (object): &lt;valid schema.org FAQPage JSON-LD (≥4 Q/A pairs)&gt;
- **lede_rewrite** (string): &lt;40-60 word direct answer, first paragraph&gt;
- **original_data_points** (array): &lt;≥3 stats with value+year+source&gt;
- **kpi_set** (object): &lt;impressions, branded_queries, ai_citation_rate, on_serp_actions&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO-8601 date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
