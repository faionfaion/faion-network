<!--
purpose: Markdown skeleton for a Micro MVPs artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/micro-mvps.json.
token-budget-impact: ~250 tokens.
-->

# Micro MVPs — <artefact_id>

- **hypothesis** (string): <single falsifiable claim with numeric prediction>
- **gate_event** (string): <named gate>
- **gate_threshold** (number): <numeric gate>
- **build_window** (object): <ISO start/end ≤7 days>
- **manual_backend_plan** (string): <explicit description of manual back-end>
- **decision_at** (string): <ISO datetime ≤ window_close + 7 days>
- **decision** (string): <go | kill | iterate>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
