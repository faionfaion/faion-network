<!--
purpose: Markdown skeleton for a 30 Day Post Launch Review Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/30-day-post-launch-review-template.json.
token-budget-impact: ~250 tokens.
-->

# 30 Day Post Launch Review Template — &lt;artefact_id&gt;

- **launch_id** (string): &lt;named launch&gt;
- **launch_comms_kit_id** (string): &lt;upstream artefact id&gt;
- **review_at** (string): &lt;ISO date (T+30)&gt;
- **funnel_by_channel** (object): &lt;per-channel acquire/activate/retain/revenue counts&gt;
- **hypothesis_verdicts** (array): &lt;≥1 verdict object (hypothesis_id, verdict, evidence)&gt;
- **next_bets** (array): &lt;≥3 ranked bets with budget_usd + budget_hours&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
