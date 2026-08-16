# REST API Design

## Summary

**One-sentence:** Designs a Richardson-Maturity-Model-3 REST surface with plural resource paths, idempotent verbs, RFC 9110-aligned status codes, and HATEOAS links for state transitions.

**One-paragraph:** REST APIs that violate HTTP semantics surprise every consumer. This methodology emits a resource-spec: plural-noun resource paths, verbs matching idempotency expectations (GET/PUT/DELETE idempotent; POST/PATCH not), status codes mapped per RFC 9110, idempotency-key support on POST where appropriate, and HATEOAS links on resources that have state transitions. Output: resource-spec + path-style policy + status-code matrix.

**Ефективно для:**

- Solo dev shipping a brand-new REST API where every endpoint started as POST.
- Refactoring a non-idempotent GET that mutates state (auditor finds it).
- Adding Idempotency-Key support to charge endpoints to survive client retries.
- Standardising status codes across 20 endpoints that returned 200-OK for everything.

## Applies If (ALL must hold)

- API is REST (resource-oriented, not RPC).
- Caller is expected to make multi-step state transitions.
- Author can break clients on documented major version bump.

## Skip If (ANY kills it)

- GraphQL (use api-graphql).
- Pure RPC API (gRPC / JSON-RPC) — out of scope.
- Internal RPC where REST conventions cost more than they help.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource inventory | list of resources + operations | PRD |
| OpenAPI spec | openapi.yaml | api-openapi-spec |
| Error catalogue | ERR-* artefact | api-error-handling |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | Source-of-truth spec carrying the design. |
| [[api-versioning]] | Versioning policy governs breaking changes to the design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_rest_design_draft` | sonnet | Bounded synthesis. |
| `api_rest_design_validate` | haiku | Mechanical schema check. |
| `api_rest_design_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-rest-design artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-rest-design artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-rest-design.py` | Validate api-rest-design artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-versioning]]
- [[api-error-handling]]
- [[api-documentation]]
- [[api-openapi-spec]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-rest-design.json",
  "type": "object",
  "required": [
    "spec_id",
    "resources",
    "status_codes_used"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^REST-[A-Z0-9-]{2,40}$"
    },
    "resources": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "path",
          "methods"
        ],
        "properties": {
          "path": {
            "type": "string",
            "pattern": "^/[a-z0-9-]+(/\\{[a-z0-9_]+\\})?(/[a-z0-9-]+)*$"
          },
          "methods": {
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE"
              ]
            }
          },
          "idempotent": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "hateoas_links": {
            "type": "boolean"
          },
          "idempotency_key": {
            "type": "boolean"
          }
        }
      }
    },
    "status_codes_used": {
      "type": "array",
      "items": {
        "type": "integer"
      }
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "spec_id": "REST-ORDERS-V1",
  "resources": [
    {
      "path": "/orders",
      "methods": [
        "GET",
        "POST"
      ],
      "idempotent": [
        "GET"
      ],
      "hateoas_links": true,
      "idempotency_key": true
    },
    {
      "path": "/orders/{id}",
      "methods": [
        "GET",
        "PUT",
        "DELETE"
      ],
      "idempotent": [
        "GET",
        "PUT",
        "DELETE"
      ],
      "hateoas_links": true
    },
    {
      "path": "/orders/{id}/items",
      "methods": [
        "GET",
        "POST"
      ],
      "idempotent": [
        "GET"
      ],
      "idempotency_key": true
    }
  ],
  "status_codes_used": [
    200,
    201,
    204,
    400,
    401,
    404,
    409,
    422,
    429,
    500
  ]
}
```
