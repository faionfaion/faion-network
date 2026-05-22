<!--
purpose: Minimum-viable filled-in version of the methodology-corpus-licence-bundle artefact for smoke testing.
consumes: nothing — this is a fixture.
produces: Reference output for `scripts/validate-methodology-corpus-licence-bundle.py --self-test`.
depends-on: `content/02-output-contract.xml`.
token-budget-impact: zero.
-->

# Smoke-test artefact for methodology-corpus-licence-bundle

Filled fixture used by `scripts/validate-methodology-corpus-licence-bundle.py --self-test`. Edit only when the output schema changes.

```json
{
  "slug": "methodology-corpus-licence-bundle",
  "version": "1.1.0",
  "owner": "ml-eng:alice",
  "produced_at": "2026-05-22T11:30:00Z",
  "produces": "spec",
  "scope": {"title": "Smoke-test methodology-corpus-licence-bundle", "context_link": "https://github.com/org/repo/issues/0"},
  "approver": "tl:bob",
  "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"}
}
```
