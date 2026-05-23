<!-- purpose: minimum-viable filled-in version of the spec artefact for smoke testing -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: artefact instance that MUST validate via scripts/validate-graceful-offboard-script.py -->
<!-- depends-on: templates/graceful-offboard-script.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~200 tokens -->

# Graceful Offboard Script — Smoke Test Fixture

```json
{
  "artefact_id": "graceful-offboard-script-acme-2026-05-23",
  "owner": "Ruslan Faion <ruslan@faion.net>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "decision": "Approve scope-clause A-07 against discovery interview from 2026-04-15.",
  "rationale": "Maria Lopes (VP Ops) confirmed in the 2026-04-15 interview at 00:12:30 that v1 ships single-currency only; the pricing assumes that constraint per A-07.",
  "inputs_used": [
    {
      "name": "interview-2026-04-15",
      "source": "interviews/2026-04-15-vp-ops.md"
    },
    {
      "name": "pricing-worksheet",
      "source": "pricing/v1.xlsx"
    }
  ]
}
```
