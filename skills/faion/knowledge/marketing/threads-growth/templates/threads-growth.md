<!--
purpose: Markdown skeleton for a Threads Growth artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/threads-growth.json.
token-budget-impact: ~250 tokens.
-->

# Threads Growth — <artefact_id>

- **operator** (string): <named account owner>
- **daily_post_target** (integer): <≥5>
- **daily_reply_target** (integer): <≥10 to larger accounts>
- **adaptation_log** (array): <X/IG source → Threads adapted text>
- **voice_register** (enum): <casual|playful (formal rejected)>
- **kpi_set** (object): <{impressions, replies_from_strangers, profile_visits, qualified_follows}>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
