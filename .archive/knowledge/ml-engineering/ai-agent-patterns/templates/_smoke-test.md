<!--
purpose: Minimum-viable filled-in version of the ai-agent-patterns artefact for smoke testing.
consumes: nothing — this is a fixture.
produces: Reference output for `scripts/validate-ai-agent-patterns.py --self-test`.
depends-on: `content/02-output-contract.xml`.
token-budget-impact: zero.
-->

# Smoke-test artefact for ai-agent-patterns

Filled fixture used by `scripts/validate-ai-agent-patterns.py --self-test`. Edit only when the output schema changes.

```json
{
  "slug": "ai-agent-patterns",
  "version": "1.1.0",
  "owner": "ml-eng:alice",
  "produced_at": "2026-05-22T11:30:00Z",
  "produces": "decision-record",
  "scope": {"title": "Smoke-test ai-agent-patterns", "context_link": "https://github.com/org/repo/issues/0"},
  "approver": "tl:bob",
  "review": {"cadence": "quarterly", "next_review_at": "2026-08-22"}
}
```
