<!--
purpose: Markdown skeleton for a Research Repo File-Naming Convention artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/research-repo-file-naming-convention.json.
token-budget-impact: ~250 tokens.
-->

# Research Repo File-Naming Convention — <artefact_id>

- **repo_root** (string): <absolute path to research repo>
- **folder_tree** (array): <lifecycle folders: recruit/, run/, tag/, synthesise/, archive/>
- **filename_grammar** (string): <regex for valid filenames>
- **manifest_schema** (object): <JSON Schema for manifest.json>
- **anonymisation_policy** (string): <Pnnn rule + scrub regex>
- **owner** (string): <named researcher>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
