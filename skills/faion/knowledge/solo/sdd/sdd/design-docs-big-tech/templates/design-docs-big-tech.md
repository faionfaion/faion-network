<!--
purpose: Markdown skeleton for a Design Docs at Big Tech Companies artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/design-docs-big-tech.json.
token-budget-impact: ~250 tokens.
-->

# Design Docs at Big Tech Companies — &lt;artefact_id&gt;

- **doc_format** (string): &lt;RFC | ERD | 6-Pager | ADR | Custom&gt;
- **scope** (string): &lt;small | team | cross-org&gt;
- **audience** (array): &lt;named roles&gt;
- **page_budget** (integer): &lt;1..10&gt;
- **review_deadline** (date): &lt;ISO date&gt;
- **alternatives** (array): &lt;≥2 including 'do nothing'&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
