<!--
purpose: Markdown skeleton for a Launch Tier Decision Frame artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/launch-tier-decision-frame.json.
token-budget-impact: ~250 tokens.
-->

# Launch Tier Decision Frame — <artefact_id>

- **launch_name** (string): <named launch>
- **funnel_goal** (string): <enum (signups | paid | waitlist | press | qualitative)>
- **selected_tier** (integer): <1-4 (soft / friend / ph-day / blitz)>
- **readiness_score** (object): <capacity + support + rollback subscores>
- **retreat_cost** (string): <concrete units>
- **rationale** (string): <≥200 chars>
- **owner** (string): <named human owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
