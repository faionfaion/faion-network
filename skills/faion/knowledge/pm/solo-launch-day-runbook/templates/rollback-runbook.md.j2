<!--
purpose: Step-by-step rollback procedure (≤10 minutes)
consumes: See content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~200-500 tokens when loaded as context
-->
# Rollback Runbook

Triggered by: 5xx > 10%, payment success < 50%, security incident, founder discretion.

## Steps (target: 10 minutes)

1. (1 min) Switch nginx to `maintenance.html` fallback. Status page → "Investigating".
2. (2 min) Roll the application container back to the previous tag (`docker compose up -d --pull always` against the pinned previous tag).
3. (1 min) Roll the database migration back IF the migration is reversible. Otherwise restore from the pre-launch snapshot.
4. (2 min) Verify health check passes. Run the abbreviated smoke test (signup + payment).
5. (1 min) Re-enable traffic. Status page → "Operational".
6. (3 min) Post incident note to support inbox auto-reply + Twitter status (use prepared template).

## Outcome

- triggered_at:
- reverted_at:
- steps_taken:
- outcome: (rolled-back / partial / failed)
- followup-actions:
