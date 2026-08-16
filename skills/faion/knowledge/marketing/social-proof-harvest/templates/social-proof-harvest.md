<!--
purpose: Markdown skeleton for a Social Proof Harvest artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/social-proof-harvest.json.
token-budget-impact: ~250 tokens.
-->

# Social Proof Harvest — <artefact_id>

- **quote_id** (string): <stable record id>
- **source_url** (string): <URL of original public mention>
- **author_handle** (string): <platform handle>
- **author_display_name** (string): <name shown on the wall>
- **verbatim_quote** (string): <exact text — no paraphrase>
- **captured_at** (date-time): <ISO timestamp>
- **channel** (enum): <twitter|linkedin|reddit|hn|discord|product-hunt|other>
- **consent** (object): <{requested_at, granted_at, granted_via}>
- **status** (enum): <captured|requested|approved|published|expired>
- **publish_surfaces** (array): <wall|landing-hero|sales-deck|email-signature>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
