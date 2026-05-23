<!--
purpose: Markdown skeleton for a Solo Niche Disqualifier Checklist artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/solo-niche-disqualifier-checklist.json.
token-budget-impact: ~250 tokens.
-->

# Solo Niche Disqualifier Checklist — &lt;artefact_id&gt;

- **operator** (string): &lt;named freelancer&gt;
- **specialisation_statement** (string): &lt;1-line&gt;
- **floor_rate** (object): &lt;{value, unit}&gt;
- **hard_no_list** (array): &lt;≥5 named industries/project shapes&gt;
- **disqualifier_signals** (array): &lt;exactly 5 signal definitions&gt;
- **rejection_reply_template** (string): &lt;≤60 words&gt;
- **max_eval_minutes** (integer): &lt;≤5&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
