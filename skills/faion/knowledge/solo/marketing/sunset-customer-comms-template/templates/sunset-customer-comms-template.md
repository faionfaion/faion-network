<!--
purpose: Markdown skeleton for a Sunset Customer Comms Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/sunset-customer-comms-template.json.
token-budget-impact: ~250 tokens.
-->

# Sunset Customer Comms Template — &lt;artefact_id&gt;

- **artefact_id** (string): &lt;kebab-case slug&gt;
- **owner** (string): &lt;named human&gt;
- **cause_sentence** (string): &lt;one honest line&gt;
- **timeline** (object): &lt;{announce_date, migration_window_days, v1_off_date}&gt;
- **migration_path** (object): &lt;{primary: v2|competitor|refund, terms}&gt;
- **communication_channels** (array): &lt;email + in-app + status-page&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
