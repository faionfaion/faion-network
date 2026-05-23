<!--
purpose: Markdown skeleton for a Maintain Mode SOPs Solo artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/maintain-mode-sops-solo.json.
token-budget-impact: ~250 tokens.
-->

# Maintain Mode SOPs Solo — &lt;artefact_id&gt;

- **product_name** (string): &lt;named product&gt;
- **weekly_check** (object): &lt;tasks + duration&gt;
- **monthly_reconcile** (object): &lt;tasks + duration&gt;
- **quarterly_upgrade** (object): &lt;tasks + duration&gt;
- **on_call_rule** (object): &lt;trigger + max_response_window_hours&gt;
- **sunset_trigger** (string): &lt;MRR / churn condition&gt;
- **owner** (string): &lt;named human owner&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
