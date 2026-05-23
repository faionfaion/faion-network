<!--
purpose: Markdown skeleton for a Living Documentation artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/living-documentation.json.
token-budget-impact: ~250 tokens.
-->

# Living Documentation — &lt;artefact_id&gt;

- **docs_root** (string): &lt;absolute path to docs/&gt;
- **docs_framework** (string): &lt;Hugo | Docusaurus | MkDocs | other&gt;
- **auto_generated_sections** (array): &lt;list of {file, generator, source}&gt;
- **hand_authored_sections** (array): &lt;list of {file, owner}&gt;
- **ci_checks** (object): &lt;link-validation + spec-diff + build-success flags&gt;
- **changelog_source** (string): &lt;commits | manual (only commits allowed)&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
