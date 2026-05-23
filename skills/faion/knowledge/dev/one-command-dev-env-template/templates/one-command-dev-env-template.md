<!--
purpose: Markdown skeleton for a One Command Dev Env Template decision-record.
consumes: Inputs from the Prerequisites table in AGENTS.md.
produces: a Markdown decision-record consumable by humans + indexable by tools.
depends-on: content/02-output-contract.xml schema.
token-budget-impact: ~180 tokens.
-->

# Dev Env Reset Decision — &lt;artefact_id&gt;

- **artefact_id**: &lt;kebab-case-slug&gt;
- **owner**: &lt;handle or email — single named human, never "team"&gt;
- **status**: active
- **version**: 1.0.0
- **last_reviewed**: 2026-05-22

## Decision

&lt;The actual choice. One short line. Example: "`make dev-up` runs docker compose up + bootstrap script + seed-fixtures.sh".&gt;

## Rationale

&lt;Two or more sentences. Cite at least one input artefact by name (ticket, runbook, repo path). Example: "Ticket eng-1234 surfaced that new joiners spend 3h on first run. The bootstrap script at scripts/dev-up.sh already handles deps + migrations + seed; wrapping it in make dev-up gives one canonical entry point."&gt;

## Inputs used

- &lt;input_1_name&gt; — &lt;source path or URL&gt;
- &lt;input_2_name&gt; — &lt;source path or URL&gt;

## Notes

&lt;Optional: "ready for owner review" or "wrong-tool note" or "supersedes &lt;old_artefact_id&gt;".&gt;
