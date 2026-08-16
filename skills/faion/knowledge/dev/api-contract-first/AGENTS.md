# API Contract-First Development

## Summary

**One-sentence:** Generates an OpenAPI spec + CI contract-test wiring so both server and clients are generated from the same source — never the other way round.

**One-paragraph:** Code-first APIs drift between server and client; contract-first locks both to one source. This methodology emits an OpenAPI 3.1 spec (or AsyncAPI for events), the CI job that breaks on schema-drift, and the codegen wiring for server stubs + client SDKs. Output: contract-pack with `openapi.yaml`, `contract-ci.yaml`, and a checklist that every PR touching the API also updates the spec.

**Ефективно для:**

- Solo dev shipping a new public API where mobile + web + partners all need a client.
- Migrating a code-first Flask/Express API to contract-first to stop schema drift.
- Adding a CI gate that prevents PRs from landing without an updated spec.
- Generating SDKs in 3 languages instead of hand-writing each.

## Applies If (ALL must hold)

- API has &gt;= 1 consumer that is not the same team as the producer.
- OpenAPI 3.1 tooling is available (or AsyncAPI for event-based).
- Repo CI can run a contract-diff step (openapi-diff / oasdiff).
- Author has authority to enforce the gate on the PR.

## Skip If (ANY kills it)

- Single-team, single-consumer prototype where drift cost is zero.
- GraphQL API (schema serves the contract — use api-graphql).
- Legacy SOAP — out of scope.
- Internal-only RPC where protobuf already enforces contract.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API surface inventory | list of endpoints | code or PM |
| OpenAPI baseline | openapi.yaml or empty stub | templates/openapi-base.yaml |
| CI runner | GitHub Actions / GitLab CI | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-openapi-spec]] | Spec authoring conventions. |
| [[api-versioning]] | Breaking-change rules for the spec. |

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
| `api_contract_first_draft` | sonnet | Bounded synthesis. |
| `api_contract_first_validate` | haiku | Mechanical schema check. |
| `api_contract_first_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/contract-ci.yaml` | GitHub Actions workflow that runs oasdiff against base branch |
| `templates/openapi-base.yaml` | OpenAPI 3.1 skeleton with version-policy stub + additionalProperties=false defaults |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-contract-first artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-contract-first artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-contract-first.py` | Validate api-contract-first artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-openapi-spec]]
- [[api-rest-design]]
- [[api-documentation]]
- [[contract-first-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/contract-ci.yaml`

```yaml
name: API Contract CI

on:
  pull_request:
    paths:
      - 'openapi.yaml'
      - 'server/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        run: npx --yes @stoplight/spectral-cli lint openapi.yaml

      - name: Generate server stubs
        run: |
          docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
            -i /local/openapi.yaml \
            -g python-fastapi \
            -o /local/generated \
            --additional-properties=packageName=api

      - name: Compare generated models with implementation
        run: diff -r ./generated/models ./server/models

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements-test.txt

      - name: Run contract tests
        run: pytest tests/contract/ -v
```

### `templates/openapi-base.yaml`

```yaml
openapi: "3.1.0"
info:
  title: Payment API
  version: "1.0.0"

paths:
  /payments:
    post:
      operationId: createPayment
      summary: Create a new payment
      description: Initiates a payment for the given customer.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
      responses:
        "201":
          description: Payment created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
        "400":
          $ref: '#/components/responses/ValidationError'
        "422":
          $ref: '#/components/responses/BusinessError'

components:
  schemas:
    CreatePaymentRequest:
      type: object
      required: [amount, currency, customer_id]
      properties:
        amount:
          type: integer
          minimum: 1
          description: Amount in cents
        currency:
          type: string
          enum: [USD, EUR, GBP]
        customer_id:
          type: string
          format: uuid

    Payment:
      type: object
      properties:
        id:
          type: string
          format: uuid
        amount:
          type: integer
        currency:
          type: string
        status:
          type: string
          enum: [pending, completed, failed]

    ProblemDetail:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        traceId:
          type: string

  responses:
    ValidationError:
      description: Request body validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
    BusinessError:
      description: Business rule violation
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-contract-first.json",
  "type": "object",
  "required": [
    "pack_id",
    "spec_path",
    "spec_version",
    "ci_diff_job",
    "codegen_targets",
    "verdict"
  ],
  "properties": {
    "pack_id": {
      "type": "string",
      "pattern": "^CPACK-[A-Z0-9-]{2,40}$"
    },
    "spec_path": {
      "type": "string",
      "minLength": 4
    },
    "spec_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"
    },
    "ci_diff_job": {
      "type": "string",
      "minLength": 4
    },
    "codegen_targets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "enum": [
          "python",
          "typescript",
          "go",
          "rust",
          "java",
          "csharp",
          "ruby"
        ]
      }
    },
    "examples_count": {
      "type": "integer",
      "minimum": 0
    },
    "operations_count": {
      "type": "integer",
      "minimum": 0
    },
    "verdict": {
      "type": "string",
      "enum": [
        "pass",
        "fail"
      ]
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "pack_id": "CPACK-PUBLIC-API-V1",
  "spec_path": "openapi/public-api.yaml",
  "spec_version": "1.4.0",
  "ci_diff_job": ".github/workflows/contract-ci.yaml",
  "codegen_targets": [
    "typescript",
    "python"
  ],
  "examples_count": 42,
  "operations_count": 18,
  "verdict": "pass"
}
```
