<!--
purpose: Markdown skeleton for a Micro MVPs artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/micro-mvps.json.
token-budget-impact: ~250 tokens.
-->

# Micro MVPs — &lt;artefact_id&gt;

- **hypothesis** (string): &lt;single falsifiable claim with numeric prediction&gt;
- **gate_event** (string): &lt;named gate&gt;
- **gate_threshold** (number): &lt;numeric gate&gt;
- **build_window** (object): &lt;ISO start/end ≤7 days&gt;
- **manual_backend_plan** (string): &lt;explicit description of manual back-end&gt;
- **decision_at** (string): &lt;ISO datetime ≤ window_close + 7 days&gt;
- **decision** (string): &lt;go | kill | iterate&gt;
- **owner** (string): &lt;named owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
