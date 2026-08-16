<!--
purpose: Markdown skeleton for a UTM Taxonomy Discipline artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/utm-taxonomy-discipline.json.
token-budget-impact: ~250 tokens.
-->

# UTM Taxonomy Discipline — <artefact_id>

- **operator** (string): <named taxonomy owner>
- **source_vocabulary** (array): <≤12 kebab-case values>
- **medium_vocabulary** (array): <≤6 kebab-case values>
- **campaign_id_pattern** (string): <regex (yyyymmdd-asset-slug shape)>
- **validation_regex** (string): <full URL regex>
- **link_builder_url** (string): <tool URL>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
