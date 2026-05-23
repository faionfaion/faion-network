<!--
purpose: Markdown skeleton for a Tweet Thread Launch Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/tweet-thread-launch-template.json.
token-budget-impact: ~250 tokens.
-->

# Tweet Thread Launch Template — &lt;artefact_id&gt;

- **launch_id** (string): &lt;kebab-case slug&gt;
- **operator** (string): &lt;named launcher&gt;
- **tweets** (array): &lt;exactly 7 tweets with id + text + media&gt;
- **demo_gif_url** (string): &lt;<30s gif/mp4 URL&gt;
- **hook_variants_tested** (array): &lt;≥3 variants with pre-launch impressions&gt;
- **social_proof_quote** (object): &lt;{quote, handle, consent_logged_at}&gt;
- **scheduled_for** (date-time): &lt;ISO timestamp&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
