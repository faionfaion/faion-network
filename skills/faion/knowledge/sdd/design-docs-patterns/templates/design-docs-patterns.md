<!--
purpose: Markdown skeleton for a Design Docs Patterns artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/design-docs-patterns.json.
token-budget-impact: ~250 tokens.
-->

# Design Docs Patterns — &lt;artefact_id&gt;

- **doc_id** (string): &lt;stable id&gt;
- **title** (string): &lt;doc title&gt;
- **scope** (string): &lt;small | team | cross-org&gt;
- **format** (string): &lt;Google-lite | Amazon-6-pager | Uber-RFC | Stripe-ERD&gt;
- **sections** (object): &lt;required sections populated&gt;
- **non_goals** (array): &lt;≥1 non-goal&gt;
- **alternatives** (array): &lt;≥2 genuine&gt;
- **review_deadline** (date): &lt;ISO date&gt;
- **owner** (string): &lt;named author&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
