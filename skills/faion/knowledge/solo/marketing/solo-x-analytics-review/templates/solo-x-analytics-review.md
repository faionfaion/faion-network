<!--
purpose: Markdown skeleton for a Solo X Analytics Review artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/solo-x-analytics-review.json.
token-budget-impact: ~250 tokens.
-->

# Solo X Analytics Review — &lt;artefact_id&gt;

- **operator** (string): &lt;named X account owner&gt;
- **week_iso** (string): &lt;ISO week tag&gt;
- **metrics** (object): &lt;{impressions, profile_visits, net_followers, replies_from_strangers, link_clicks}&gt;
- **trailing_4w_median** (object): &lt;median per metric&gt;
- **outliers** (array): &lt;posts where impressions ≥3x median&gt;
- **top_post** (object): &lt;{url, hook, variable_observed}&gt;
- **bottom_post** (object): &lt;{url, hook}&gt;
- **qualified_follower_pct** (number): &lt;0..1&gt;
- **next_week_experiment** (object): &lt;{hypothesis, variable, success_metric}&gt;
- **time_spent_min** (integer): &lt;≤20&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
