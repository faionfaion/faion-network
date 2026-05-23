<!--
purpose: Markdown skeleton for a Launch Comms Kit Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/launch-comms-kit-template.json.
token-budget-impact: ~250 tokens.
-->

# Launch Comms Kit Template — &lt;artefact_id&gt;

- **launch_name** (string): &lt;named launch&gt;
- **positioning_sentence** (string): &lt;≤140 chars canonical sentence&gt;
- **launch_window** (object): &lt;ISO start/end&gt;
- **channels** (object): &lt;per-channel draft objects (PH/HN/X/mail/changelog)&gt;
- **publish_timeline** (array): &lt;per-channel publish_at ISO datetimes&gt;
- **retro_at** (string): &lt;ISO datetime for T+7 retro&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
