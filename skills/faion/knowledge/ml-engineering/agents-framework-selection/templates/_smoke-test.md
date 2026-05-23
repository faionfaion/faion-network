<!--
purpose: Minimum-viable filled-in version of the agents-framework-selection artefact for smoke testing.
consumes: nothing — this is a fixture.
produces: Reference output for `scripts/validate-agents-framework-selection.py --self-test`.
depends-on: `content/02-output-contract.xml`.
token-budget-impact: zero.
-->

# Smoke-test artefact for agents-framework-selection

Filled fixture used by `scripts/validate-agents-framework-selection.py --self-test`. Edit only when the output schema changes.

```json
{
  "slug": "agents-framework-selection",
  "version": "1.1.0",
  "owner": "ml-eng:alice",
  "produced_at": "2026-05-22T11:30:00Z",
  "produces": "decision-record",
  "scope": {"title": "Smoke-test agents-framework-selection", "context_link": "https://github.com/org/repo/issues/0"},
  "approver": "tl:bob",
  "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"}
}
```
