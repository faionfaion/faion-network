<!-- purpose: minimum-viable filled-in artefact for `validate-newsletter-to-paid-funnel-template.py --self-test` parity -->
<!-- consumes: nothing (built-in fixture) -->
<!-- produces: a JSON object that the validator accepts -->
<!-- depends-on: scripts/validate-newsletter-to-paid-funnel-template.py -->
<!-- token-budget-impact: ~150 tokens -->

# Smoke-test fixture

The minimum-viable filled artefact for `validate-newsletter-to-paid-funnel-template.py` is encoded inline below; the validator's `--self-test` flag bundles the same payload, so this file documents the contract for human readers.

```json
{
  "artefact_id": "newsletter-to-paid-funnel-template-smoke-2026-05-23",
  "owner": "Ruslan Faion <ruslan@faion.net>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    { "name": "smoke-input", "source": "tests/fixtures/smoke.md" }
  ],
  "sections": [
    { "heading": "Context", "body": "smoke" },
    { "heading": "Decision", "body": "smoke" }
  ],
  "decision": "smoke-test pass"
}
```

Run `python scripts/validate-newsletter-to-paid-funnel-template.py --self-test` to confirm.
