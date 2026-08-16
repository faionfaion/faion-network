# API Documentation

## Summary

**One-sentence:** Generates a six-section API reference (Overview, Auth, Quick Start, Endpoints, Error Codes, Changelog) with copy-paste curl examples and machine-readable OpenAPI alongside the prose.

**One-paragraph:** Developers evaluate APIs in under 5 minutes; missing any of six canonical sections causes abandonment. This methodology emits an API reference scaffold with the six required sections, copy-paste curl examples per endpoint, an error-codes table linked to the Problem Details schema (RFC 7807), and a Changelog tied to spec version bumps. Output: docs-bundle ready for static-site rendering + OpenAPI cross-link.

**Ефективно для:**

- Solo dev publishing the first public API docs on docs.example.com.
- Re-doing legacy docs that lost half their consumers due to missing Quick Start.
- Wiring the docs site to OpenAPI so examples stay in sync with the contract.
- Adding a Changelog so partners can plan around deprecations.

## Applies If (ALL must hold)

- API has external consumers (B2B / public).
- OpenAPI spec exists (api-contract-first or api-openapi-spec).
- Docs site is rendered (Docusaurus / Mintlify / Redoc / homegrown).
- Author has access to ship the docs site.

## Skip If (ANY kills it)

- Internal-only RPC documented in code comments.
- Single-team API where Slack channel is the docs.
- Generated SDK README only (no per-endpoint usage docs).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OpenAPI spec | openapi.yaml | api-contract-first output |
| Auth scheme | AUTH-* artefact | api-authentication output |
| Error catalogue | Problem Details JSON | api-error-handling output |
| Docs site stack | Docusaurus / Mintlify / Redoc | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-contract-first]] | Source of the spec the docs cross-link. |
| [[api-error-handling]] | Source of the error-codes table. |

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
| `api_documentation_draft` | sonnet | Bounded synthesis. |
| `api_documentation_validate` | haiku | Mechanical schema check. |
| `api_documentation_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/doc-structure.md.j2` | Markdown skeleton enforcing the six-section structure |
| `templates/doc-structure.md` | Markdown skeleton enforcing the six-section structure Generated from `templates/doc-structure.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/openapi-examples.yaml` | OpenAPI examples block patterns used by the docs site |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-documentation artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-documentation artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-documentation.py` | Validate api-documentation artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-openapi-spec]]
- [[api-rest-design]]
- [[api-contract-first]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/openapi-examples.yaml`

```yaml
openapi: "3.1.0"
info:
  title: Example API
  version: "1.0.0"

paths:
  /users:
    post:
      operationId: createUser
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              basic:
                summary: Minimal user
                value:
                  name: "Jane Doe"
                  email: "jane@example.com"
              with-role:
                summary: Admin user
                value:
                  name: "Admin"
                  email: "admin@example.com"
                  role: "admin"
      responses:
        "201":
          description: User created
          headers:
            Location:
              schema:
                type: string
              description: URL of the created user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        "400":
          $ref: '#/components/responses/ValidationError'
        "409":
          $ref: '#/components/responses/Conflict'

components:
  schemas:
    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
        email:
          type: string
          format: email
        role:
          type: string
          enum: [user, admin]
          default: user

    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string

  responses:
    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'
    Conflict:
      description: Resource already exists
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetail'

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
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-documentation.json",
  "type": "object",
  "required": [
    "docs_id",
    "sections",
    "quick_start_curl_count",
    "endpoints_documented",
    "error_codes_documented",
    "changelog_entries",
    "verdict"
  ],
  "properties": {
    "docs_id": {
      "type": "string",
      "pattern": "^DOCS-[A-Z0-9-]{2,40}$"
    },
    "sections": {
      "type": "array",
      "minItems": 6,
      "items": {
        "type": "string",
        "enum": [
          "overview",
          "authentication",
          "quick-start",
          "endpoints",
          "error-codes",
          "changelog"
        ]
      },
      "uniqueItems": true
    },
    "quick_start_curl_count": {
      "type": "integer",
      "minimum": 1
    },
    "endpoints_documented": {
      "type": "integer",
      "minimum": 0
    },
    "error_codes_documented": {
      "type": "integer",
      "minimum": 0
    },
    "changelog_entries": {
      "type": "integer",
      "minimum": 0
    },
    "examples_source": {
      "type": "string",
      "enum": [
        "openapi",
        "hand"
      ]
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
  "docs_id": "DOCS-PUBLIC-API-V1",
  "sections": [
    "overview",
    "authentication",
    "quick-start",
    "endpoints",
    "error-codes",
    "changelog"
  ],
  "quick_start_curl_count": 3,
  "endpoints_documented": 18,
  "error_codes_documented": 12,
  "changelog_entries": 6,
  "examples_source": "openapi",
  "verdict": "pass"
}
```
