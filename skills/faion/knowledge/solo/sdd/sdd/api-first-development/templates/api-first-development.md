<!--
purpose: Markdown skeleton for a API-First Development artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/api-first-development.json.
token-budget-impact: ~250 tokens.
-->

# API-First Development — &lt;artefact_id&gt;

- **openapi_spec_path** (string): &lt;path to openapi.yaml&gt;
- **openapi_version** (string): &lt;must start with 3.1&gt;
- **endpoints** (array): &lt;list of {path, method, op_id}&gt;
- **mock_server_url** (string): &lt;Prism mock URL&gt;
- **contract_test_config** (string): &lt;path to schemathesis.yaml or equivalent&gt;
- **version** (string): &lt;semver of the API itself&gt;
- **owner** (string): &lt;named owner&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
