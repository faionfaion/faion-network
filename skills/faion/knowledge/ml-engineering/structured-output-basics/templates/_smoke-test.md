<!--
purpose: Minimum-viable filled-in version of the structured-output-basics artefact for smoke testing.
consumes: nothing — this is a fixture.
produces: Reference output for `scripts/validate-structured-output-basics.py --self-test`.
depends-on: `content/02-output-contract.xml`.
token-budget-impact: zero.
-->

# Smoke-test artefact for structured-output-basics

Filled fixture used by `scripts/validate-structured-output-basics.py --self-test`. Edit only when the output schema changes.

```json
{
  "slug": "structured-output-basics",
  "version": "1.1.0",
  "owner": "ml-eng:alice",
  "produced_at": "2026-05-22T11:30:00Z",
  "produces": "code",
  "scope": {"title": "Smoke-test structured-output-basics", "context_link": "https://github.com/org/repo/issues/0"},
  "approver": "tl:bob",
  "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"}
}
```
