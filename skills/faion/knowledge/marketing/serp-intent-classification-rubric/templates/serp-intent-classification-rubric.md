<!--
purpose: Markdown skeleton for a SERP Intent Classification Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/serp-intent-classification-rubric.json.
token-budget-impact: ~250 tokens.
-->

# SERP Intent Classification Rubric — <artefact_id>

- **query** (string): <verbatim_target_query>
- **primary_intent** (enum): <one of I / C / T / N>
- **primary_subtype** (string): <e.g., I:how-to, C:vs, T:buy, N:brand>
- **secondary_intent** (string|null): <null unless ≥30% of top-10 serve a different class>
- **serp_evidence** (array): <≥2 independent signals with type+value>
- **recommendation** (enum): <SINGLE_BRIEF | SPLIT | AMBIGUOUS_BLOCK>
- **classifier** (string): <named_human_agent>
- **classified_at** (date-time): <iso_timestamp>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
