<!--
purpose: Markdown skeleton for a Shutdown Customer Email Pack artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/shutdown-customer-email-pack.json.
token-budget-impact: ~250 tokens.
-->

# Shutdown Customer Email Pack — &lt;artefact_id&gt;

- **artefact_id** (string): &lt;kebab-case slug for the shutdown sequence&gt;
- **owner** (string): &lt;named human signing the emails&gt;
- **service_off_date** (date): &lt;ISO date the product stops&gt;
- **announce_email** (object): &lt;subject + body + send_date (T-30)&gt;
- **refund_email** (object): &lt;subject + body + send_date (T-14) + refund_terms&gt;
- **final_thanks_email** (object): &lt;subject + body + send_date (T+1)&gt;
- **real_reason_sentence** (string): &lt;one honest sentence on cause&gt;
- **refund_or_migration** (object): &lt;{type: refund|migrate, terms: string}&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
