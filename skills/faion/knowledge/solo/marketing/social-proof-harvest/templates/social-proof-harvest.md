<!--
purpose: Markdown skeleton for a Social Proof Harvest artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/social-proof-harvest.json.
token-budget-impact: ~250 tokens.
-->

# Social Proof Harvest — &lt;artefact_id&gt;

- **quote_id** (string): &lt;stable record id&gt;
- **source_url** (string): &lt;URL of original public mention&gt;
- **author_handle** (string): &lt;platform handle&gt;
- **author_display_name** (string): &lt;name shown on the wall&gt;
- **verbatim_quote** (string): &lt;exact text — no paraphrase&gt;
- **captured_at** (date-time): &lt;ISO timestamp&gt;
- **channel** (enum): &lt;twitter|linkedin|reddit|hn|discord|product-hunt|other&gt;
- **consent** (object): &lt;{requested_at, granted_at, granted_via}&gt;
- **status** (enum): &lt;captured|requested|approved|published|expired&gt;
- **publish_surfaces** (array): &lt;wall|landing-hero|sales-deck|email-signature&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
