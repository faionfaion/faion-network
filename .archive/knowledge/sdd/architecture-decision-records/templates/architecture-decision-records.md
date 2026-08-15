<!--
purpose: Markdown skeleton for a Architecture Decision Records artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/architecture-decision-records.json.
token-budget-impact: ~250 tokens.
-->

# Architecture Decision Records — &lt;artefact_id&gt;

- **adr_id** (string): &lt;stable id (ADR-001..)&gt;
- **title** (string): &lt;decision title&gt;
- **status** (string): &lt;Proposed | Accepted | Deprecated | Superseded&gt;
- **context** (string): &lt;background paragraph&gt;
- **decision** (string): &lt;what was decided&gt;
- **alternatives** (array): &lt;≥2 with rationale&gt;
- **consequences** (object): &lt;{positive: [...], negative: [...]}&gt;
- **supersedes** (string): &lt;ADR id this replaces (or null)&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
