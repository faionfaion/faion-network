<!-- purpose: minimum-viable filled-in artefact for `validate-seo.py --self-test` parity -->
<!-- consumes: nothing (built-in fixture) -->
<!-- produces: a JSON object that the validator accepts -->
<!-- depends-on: scripts/validate-seo.py -->
<!-- token-budget-impact: ~150 tokens -->

# Smoke-test fixture

The minimum-viable filled artefact for `validate-seo.py` is encoded inline below; the validator's `--self-test` flag bundles the same payload, so this file documents the contract for human readers.

```json
{
  "artefact_id": "seo-smoke-2026-05-23",
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

Run `python scripts/validate-seo.py --self-test` to confirm.
