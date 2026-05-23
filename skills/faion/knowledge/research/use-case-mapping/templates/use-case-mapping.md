<!--
purpose: Markdown skeleton for a Use Case Mapping artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/use-case-mapping.json.
token-budget-impact: ~250 tokens.
-->

# Use Case Mapping — &lt;artefact_id&gt;

- **use_case_id** (string): &lt;stable id (UC-001..)&gt;
- **primary_actor** (string): &lt;named role&gt;
- **goal** (string): &lt;active-verb statement&gt;
- **preconditions** (array): &lt;system + actor state before flow starts&gt;
- **main_flow** (array): &lt;numbered steps&gt;
- **alternative_flows** (array): &lt;≥1 branching scenarios&gt;
- **postcondition** (string): &lt;observable end state&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
