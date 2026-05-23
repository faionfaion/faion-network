<!--
purpose: Markdown skeleton for a Validation Paralysis Breaker artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/validation-paralysis-breaker.json.
token-budget-impact: ~250 tokens.
-->

# Validation Paralysis Breaker — &lt;artefact_id&gt;

- **hypothesis** (string): &lt;one-line statement&gt;
- **falsification_trigger** (string): &lt;observable that would falsify&gt;
- **budget_start** (datetime): &lt;ISO datetime&gt;
- **budget_end** (datetime): &lt;budget_start + 72h&gt;
- **verdict** (string): &lt;ship | park | extend-once&gt;
- **named_risk** (string): &lt;the risk being taken or carried&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
