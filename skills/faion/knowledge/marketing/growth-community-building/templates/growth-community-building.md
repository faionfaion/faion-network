<!--
purpose: Markdown skeleton for a Growth Community Building artefact.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown artefact rendering the JSON output contract for humans.
depends-on: content/02-output-contract.xml + templates/growth-community-building.json.
token-budget-impact: ~250 tokens.
-->

# Growth Community Building — <artefact_id>

- **community_id** (string): <kebab-case slug>
- **host** (string): <named human accountable for rituals>
- **platform** (enum): <discord|slack|circle|telegram>
- **seed_members** (array): <≥50 entries with name + handle + reason>
- **planted_conversations** (array): <5-10 conversation prompts with author>
- **rituals** (array): <≥3 with cadence + owner + agenda>
- **guidelines** (string): <community guidelines markdown>
- **health_targets** (object): <{dau_mau: 0.25, weekly_active_members_pct: 0.4}>
- **version** (string): <semver>
- **last_reviewed** (date): <ISO date>

## Notes

<Optional: 'ready for owner review' or links to validator output.>
