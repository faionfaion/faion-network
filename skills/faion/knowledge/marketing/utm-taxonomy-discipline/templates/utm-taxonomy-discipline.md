<!--
purpose: Markdown skeleton for a UTM Taxonomy Discipline artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/utm-taxonomy-discipline.json.
token-budget-impact: ~250 tokens.
-->

# UTM Taxonomy Discipline — &lt;artefact_id&gt;

- **operator** (string): &lt;named taxonomy owner&gt;
- **source_vocabulary** (array): &lt;≤12 kebab-case values&gt;
- **medium_vocabulary** (array): &lt;≤6 kebab-case values&gt;
- **campaign_id_pattern** (string): &lt;regex (yyyymmdd-asset-slug shape)&gt;
- **validation_regex** (string): &lt;full URL regex&gt;
- **link_builder_url** (string): &lt;tool URL&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
