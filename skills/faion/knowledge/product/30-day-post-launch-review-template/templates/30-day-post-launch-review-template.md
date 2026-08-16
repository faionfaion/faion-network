<!--
purpose: Markdown skeleton for a 30 Day Post Launch Review Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/30-day-post-launch-review-template.json.
token-budget-impact: ~250 tokens.
-->

# 30 Day Post Launch Review Template — <artefact_id>

- **launch_id** (string): <named_launch>
- **launch_comms_kit_id** (string): <upstream_artefact_id>
- **review_at** (string): <ISO date (T+30)>
- **funnel_by_channel** (object): <per-channel acquire/activate/retain/revenue counts>
- **hypothesis_verdicts** (array): <≥1 verdict object (hypothesis_id, verdict, evidence)>
- **next_bets** (array): <≥3 ranked bets with budget_usd + budget_hours>
- **owner** (string): <owner_full_name>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
