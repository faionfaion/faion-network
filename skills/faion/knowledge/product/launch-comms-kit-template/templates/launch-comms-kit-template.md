<!--
purpose: Markdown skeleton for a Launch Comms Kit Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/launch-comms-kit-template.json.
token-budget-impact: ~250 tokens.
-->

# Launch Comms Kit Template — <artefact_id>

- **launch_name** (string): <named_launch>
- **positioning_sentence** (string): <≤140 chars canonical sentence>
- **launch_window** (object): <iso_start_end>
- **channels** (object): <per-channel draft objects (PH/HN/X/mail/changelog)>
- **publish_timeline** (array): <per-channel publish_at ISO datetimes>
- **retro_at** (string): <ISO datetime for T+7 retro>
- **owner** (string): <named_human_owner>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
