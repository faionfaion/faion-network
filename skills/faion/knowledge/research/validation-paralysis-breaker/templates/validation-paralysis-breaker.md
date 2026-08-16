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
- **budget_start** (datetime): <iso_datetime>
- **budget_end** (datetime): <budget_start_72h>
- **verdict** (string): <ship | park | extend-once>
- **named_risk** (string): <the risk being taken or carried>
- **owner** (string): <owner_full_name>
- **version** (string): <document_version>
- **last_reviewed** (date): <last_reviewed_date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
