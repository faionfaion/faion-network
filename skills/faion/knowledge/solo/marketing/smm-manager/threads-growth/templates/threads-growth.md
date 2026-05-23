<!--
purpose: Markdown skeleton for a Threads Growth artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/threads-growth.json.
token-budget-impact: ~250 tokens.
-->

# Threads Growth — &lt;artefact_id&gt;

- **operator** (string): &lt;named account owner&gt;
- **daily_post_target** (integer): &lt;≥5&gt;
- **daily_reply_target** (integer): &lt;≥10 to larger accounts&gt;
- **adaptation_log** (array): &lt;X/IG source → Threads adapted text&gt;
- **voice_register** (enum): &lt;casual|playful (formal rejected)&gt;
- **kpi_set** (object): &lt;{impressions, replies_from_strangers, profile_visits, qualified_follows}&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
