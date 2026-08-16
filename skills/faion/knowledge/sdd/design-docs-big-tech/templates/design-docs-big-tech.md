<!--
purpose: Markdown skeleton for a Design Docs at Big Tech Companies artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/design-docs-big-tech.json.
token-budget-impact: ~250 tokens.
-->

# Design Docs at Big Tech Companies — <artefact_id>

- **doc_format** (string): <RFC | ERD | 6-Pager | ADR | Custom>
- **scope** (string): <small | team | cross-org>
- **audience** (array): <named_roles>
- **page_budget** (integer): <1..10>
- **review_deadline** (date): <iso_date>
- **alternatives** (array): <≥2 including 'do nothing'>
- **owner** (string): <named_author>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
