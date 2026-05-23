<!--
purpose: Markdown skeleton for a Launch Tier Decision Frame artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/launch-tier-decision-frame.json.
token-budget-impact: ~250 tokens.
-->

# Launch Tier Decision Frame — &lt;artefact_id&gt;

- **launch_name** (string): &lt;named launch&gt;
- **funnel_goal** (string): &lt;enum (signups | paid | waitlist | press | qualitative)&gt;
- **selected_tier** (integer): &lt;1-4 (soft / friend / ph-day / blitz)&gt;
- **readiness_score** (object): &lt;capacity + support + rollback subscores&gt;
- **retreat_cost** (string): &lt;concrete units&gt;
- **rationale** (string): &lt;≥200 chars&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
