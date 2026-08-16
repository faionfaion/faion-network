<!--
purpose: Markdown skeleton for a Design Docs Patterns artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/design-docs-patterns.json.
token-budget-impact: ~250 tokens.
-->

# Design Docs Patterns — <artefact_id>

- **doc_id** (string): <stable id>
- **title** (string): <doc title>
- **scope** (string): <small | team | cross-org>
- **format** (string): <Google-lite | Amazon-6-pager | Uber-RFC | Stripe-ERD>
- **sections** (object): <required sections populated>
- **non_goals** (array): <≥1 non-goal>
- **alternatives** (array): <≥2 genuine>
- **review_deadline** (date): <ISO date>
- **owner** (string): <named author>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
