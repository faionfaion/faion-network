<!-- purpose: smoke-test fixture for the methodology validator -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Smoke-test fixture

```json
{
  "slug": "gcp-gke-architecture",
  "title": "Gcp Gke Architecture",
  "scope": "Production deployment for service X across two environments.",
  "components": [
    {
      "name": "frontend"
    },
    {
      "name": "api"
    }
  ],
  "decisions": [
    {
      "id": "d1",
      "topic": "topology",
      "choice": "regional"
    },
    {
      "id": "d2",
      "topic": "pool",
      "choice": "spot"
    },
    {
      "id": "d3",
      "topic": "identity",
      "choice": "WIF"
    }
  ]
}
```
