<!--
purpose: Markdown skeleton for a Backlog Grooming and Roadmapping artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/backlog-grooming-roadmapping.json.
token-budget-impact: ~250 tokens.
-->

# Backlog Grooming and Roadmapping — &lt;artefact_id&gt;

- **backlog_items** (array): &lt;≥10 with score + rationale + status&gt;
- **p0_items** (array): &lt;≤3&gt;
- **scoring_framework** (string): &lt;RICE | MoSCoW&gt;
- **now_items** (array): &lt;currently in flight&gt;
- **next_items** (array): &lt;next horizon&gt;
- **later_items** (array): &lt;later horizon&gt;
- **last_groomed_at** (datetime): &lt;ISO datetime&gt;
- **owner** (string): &lt;named PM&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
