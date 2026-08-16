<!--
purpose: Markdown skeleton for a Use Case Mapping artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/use-case-mapping.json.
token-budget-impact: ~250 tokens.
-->

# Use Case Mapping — <artefact_id>

- **use_case_id** (string): <stable id (UC-001..)>
- **primary_actor** (string): <named role>
- **goal** (string): <active-verb statement>
- **preconditions** (array): <system + actor state before flow starts>
- **main_flow** (array): <numbered steps>
- **alternative_flows** (array): <≥1 branching scenarios>
- **postcondition** (string): <observable end state>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
