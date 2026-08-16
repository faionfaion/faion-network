<!--
purpose: Markdown skeleton for a Tweet Thread Launch Template artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/tweet-thread-launch-template.json.
token-budget-impact: ~250 tokens.
-->

# Tweet Thread Launch Template — <artefact_id>

- **launch_id** (string): <kebab_case_slug>
- **operator** (string): <named_launcher>
- **tweets** (array): <exactly 7 tweets with id + text + media>
- **demo_gif_url** (string): <<30s gif/mp4 URL>
- **hook_variants_tested** (array): <≥3 variants with pre-launch impressions>
- **social_proof_quote** (object): <{quote, handle, consent_logged_at}>
- **scheduled_for** (date-time): <iso_timestamp>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
