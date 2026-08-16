<!--
purpose: Markdown skeleton for a API-First Development artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/api-first-development.json.
token-budget-impact: ~250 tokens.
-->

# API-First Development — <artefact_id>

- **openapi_spec_path** (string): <path to openapi.yaml>
- **openapi_version** (string): <must start with 3.1>
- **endpoints** (array): <list of {path, method, op_id}>
- **mock_server_url** (string): <Prism mock URL>
- **contract_test_config** (string): <path to schemathesis.yaml or equivalent>
- **version** (string): <semver of the API itself>
- **owner** (string): <named owner>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
