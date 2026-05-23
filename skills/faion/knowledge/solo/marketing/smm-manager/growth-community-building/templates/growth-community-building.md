<!--
purpose: Markdown skeleton for a Growth Community Building artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/growth-community-building.json.
token-budget-impact: ~250 tokens.
-->

# Growth Community Building — &lt;artefact_id&gt;

- **community_id** (string): &lt;kebab-case slug&gt;
- **host** (string): &lt;named human accountable for rituals&gt;
- **platform** (enum): &lt;discord|slack|circle|telegram&gt;
- **seed_members** (array): &lt;≥50 entries with name + handle + reason&gt;
- **planted_conversations** (array): &lt;5-10 conversation prompts with author&gt;
- **rituals** (array): &lt;≥3 with cadence + owner + agenda&gt;
- **guidelines** (string): &lt;community guidelines markdown&gt;
- **health_targets** (object): &lt;{dau_mau: 0.25, weekly_active_members_pct: 0.4}&gt;
- **version** (string): &lt;semver&gt;
- **last_reviewed** (date): &lt;ISO date&gt;

## Notes

&lt;Optional: 'ready for owner review' or links to validator output.&gt;
