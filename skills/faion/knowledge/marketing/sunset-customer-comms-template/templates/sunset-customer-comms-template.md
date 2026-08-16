<!--
purpose: Markdown skeleton for a Sunset Customer Comms Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/sunset-customer-comms-template.json.
token-budget-impact: ~250 tokens.
-->

# Sunset Customer Comms Template — <artefact_id>

- **artefact_id** (string): <kebab-case slug>
- **owner** (string): <named human>
- **cause_sentence** (string): <one honest line>
- **timeline** (object): <{announce_date, migration_window_days, v1_off_date}>
- **migration_path** (object): <{primary: v2|competitor|refund, terms}>
- **communication_channels** (array): <email + in-app + status-page>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
