<!--
purpose: Minimum-viable filled-in version of the openai-assistants artefact for smoke testing.
consumes: nothing — this is a fixture.
produces: Reference output for `scripts/validate-openai-assistants.py --self-test`.
depends-on: `content/02-output-contract.xml`.
token-budget-impact: zero.
-->

# Smoke-test artefact for openai-assistants

Filled fixture used by `scripts/validate-openai-assistants.py --self-test`. Edit only when the output schema changes.

```json
{
  "slug": "openai-assistants",
  "version": "1.1.0",
  "owner": "ml-eng:alice",
  "produced_at": "2026-05-22T11:30:00Z",
  "produces": "code",
  "scope": {"title": "Smoke-test openai-assistants", "context_link": "https://github.com/org/repo/issues/0"},
  "approver": "tl:bob",
  "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"}
}
```
