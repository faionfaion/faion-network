<!--
purpose: Markdown skeleton for a SERP Intent Classification Rubric artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/serp-intent-classification-rubric.json.
token-budget-impact: ~250 tokens.
-->

# SERP Intent Classification Rubric — &lt;artefact_id&gt;

- **query** (string): &lt;verbatim target query&gt;
- **primary_intent** (enum): &lt;one of I / C / T / N&gt;
- **primary_subtype** (string): &lt;e.g., I:how-to, C:vs, T:buy, N:brand&gt;
- **secondary_intent** (string|null): &lt;null unless ≥30% of top-10 serve a different class&gt;
- **serp_evidence** (array): &lt;≥2 independent signals with type+value&gt;
- **recommendation** (enum): &lt;SINGLE_BRIEF | SPLIT | AMBIGUOUS_BLOCK&gt;
- **classifier** (string): &lt;named human / agent&gt;
- **classified_at** (date-time): &lt;ISO timestamp&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
