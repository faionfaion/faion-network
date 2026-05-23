<!-- purpose: smoke-test fixture for the methodology validator -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Smoke-test fixture

```json
{
  "slug": "iac-pr-review-checklist",
  "summary": "Validated iac-pr-review-checklist checklist applied to a single review.",
  "items": [
    {
      "id": "i1",
      "rule": "First rule verified in scope",
      "must_or_should": "MUST",
      "evidence": "PR comment ID 42"
    },
    {
      "id": "i2",
      "rule": "Second rule verified in scope",
      "must_or_should": "MUST",
      "evidence": "plan output line 7"
    },
    {
      "id": "i3",
      "rule": "Third rule verified in scope",
      "must_or_should": "SHOULD",
      "evidence": "monitoring dashboard"
    },
    {
      "id": "i4",
      "rule": "Fourth rule verified in scope",
      "must_or_should": "MUST",
      "evidence": "policy report"
    },
    {
      "id": "i5",
      "rule": "Fifth rule verified in scope",
      "must_or_should": "SHOULD",
      "evidence": "design doc section 3"
    }
  ]
}
```
