<!--
purpose: Markdown skeleton for a Living Documentation artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/living-documentation.json.
token-budget-impact: ~250 tokens.
-->

# Living Documentation — <artefact_id>

- **docs_root** (string): <absolute path to docs/>
- **docs_framework** (string): <Hugo | Docusaurus | MkDocs | other>
- **auto_generated_sections** (array): <list of {file, generator, source}>
- **hand_authored_sections** (array): <list of {file, owner}>
- **ci_checks** (object): <link-validation + spec-diff + build-success flags>
- **changelog_source** (string): <commits | manual (only commits allowed)>
- **owner** (string): <owner_full_name>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
