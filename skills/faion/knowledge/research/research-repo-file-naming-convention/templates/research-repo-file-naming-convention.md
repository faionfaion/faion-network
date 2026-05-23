<!--
purpose: Markdown skeleton for a Research Repo File-Naming Convention artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/research-repo-file-naming-convention.json.
token-budget-impact: ~250 tokens.
-->

# Research Repo File-Naming Convention — &lt;artefact_id&gt;

- **repo_root** (string): &lt;absolute path to research repo&gt;
- **folder_tree** (array): &lt;lifecycle folders: recruit/, run/, tag/, synthesise/, archive/&gt;
- **filename_grammar** (string): &lt;regex for valid filenames&gt;
- **manifest_schema** (object): &lt;JSON Schema for manifest.json&gt;
- **anonymisation_policy** (string): &lt;Pnnn rule + scrub regex&gt;
- **owner** (string): &lt;named researcher&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
