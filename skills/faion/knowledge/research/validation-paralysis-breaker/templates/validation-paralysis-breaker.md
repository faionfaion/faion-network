<!--
purpose: Markdown skeleton for a Validation Paralysis Breaker artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/validation-paralysis-breaker.json.
token-budget-impact: ~250 tokens.
-->

# Validation Paralysis Breaker — <artefact_id>

- **hypothesis** (string): <one-line statement>
- **falsification_trigger** (string): <observable that would falsify>
- **budget_start** (datetime): <ISO datetime>
- **budget_end** (datetime): <budget_start + 72h>
- **verdict** (string): <ship | park | extend-once>
- **named_risk** (string): <the risk being taken or carried>
- **owner** (string): <named owner>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
