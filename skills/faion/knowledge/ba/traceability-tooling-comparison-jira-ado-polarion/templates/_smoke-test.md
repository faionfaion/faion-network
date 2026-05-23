<!-- purpose: minimum-viable filled-in version of the report artefact for smoke testing -->
<!-- consumes: nothing — this is a hand-filled fixture -->
<!-- produces: artefact instance that MUST validate via scripts/validate-traceability-tooling-comparison-jira-ado-polarion.py -->
<!-- depends-on: templates/traceability-tooling-comparison-jira-ado-polarion.md, content/02-output-contract.xml -->
<!-- token-budget-impact: ~200 tokens -->

# Traceability Tooling Comparison (Jira / ADO / Polarion) — Smoke Test Fixture

```json
{
  "artefact_id": "traceability-tooling-comparison-jira-ado-polarion-2026-05-23",
  "owner": "Ruslan Faion <ruslan@faion.net>",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "summary": "Comparison of Jira / ADO / Polarion against the trace-gate criteria on 2026-04-30.",
  "findings": [
    {
      "id": "f1",
      "statement": "Jira lacks first-class trace-gate; needs custom workflow.",
      "evidence": "audit/jira-config-2026-04-30.md",
      "severity": "medium"
    },
    {
      "id": "f2",
      "statement": "Polarion has built-in audit trail; meets BABOK \u00a710.43.",
      "evidence": "audit/polarion-config-2026-04-30.md",
      "severity": "info"
    }
  ],
  "recommendations": [
    {
      "id": "r1",
      "action": "Adopt Polarion if regulated; else extend Jira with custom gate.",
      "owner": "Tomas Silva <tomas@example.com>"
    }
  ]
}
```
