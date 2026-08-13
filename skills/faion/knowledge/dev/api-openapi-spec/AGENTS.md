# OpenAPI Spec Authoring

## Summary

**One-sentence:** Produces a Spectral-clean OpenAPI 3.1 spec with strict schemas, examples per operation, x-versioning policy, and security scheme block linked to the auth methodology.

**One-paragraph:** OpenAPI specs that lint clean still ship surprises. This methodology emits a Spectral-validated OpenAPI 3.1 spec with strict response schemas (additionalProperties=false), one example per request/response, an x-versioning policy declared in info, a security scheme block aligned with the AUTH-* artefact, and components.schemas reused (never inlined twice). Output: openapi.yaml + spectral.yaml + a validate-openapi.sh runner.

**Ефективно для:**

- Solo dev authoring the canonical spec for a new public API.
- Adding Spectral CI to an existing spec that nobody lints.
- Cleaning up an API where 30 endpoints inline the same User schema.
- Wiring x-versioning so downstream tools (codegen, docs) honor deprecations.

## Applies If (ALL must hold)

- Spec lives in OpenAPI 3.1 (or 3.0 in transition).
- Spectral CLI is available for linting.
- Author has authority to refactor schemas into components.

## Skip If (ANY kills it)

- GraphQL schema (use api-graphql).
- AsyncAPI / event-driven spec (out of scope).
- Legacy code-first API where spec is read-only output.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing spec | openapi.yaml | repo or empty stub |
| Auth artefact | AUTH-* spec_id | api-authentication |
| Spectral CLI | binary | @stoplight/spectral-cli |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-contract-first]] | Codegen + CI assumes a clean spec from this methodology. |
| [[api-versioning]] | x-versioning policy is declared here, enforced in versioning. |

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
| `api_openapi_spec_draft` | sonnet | Bounded synthesis. |
| `api_openapi_spec_validate` | haiku | Mechanical schema check. |
| `api_openapi_spec_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-user-api.yaml` | Reference user-api OpenAPI 3.1 spec with strict schemas + x-versioning |
| `templates/spectral.yaml` | Spectral ruleset enforcing the rules in 01-core-rules.xml |
| `templates/validate-openapi.sh` | Shell runner that lints spec with Spectral and counts duplicate schemas |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-openapi-spec artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-openapi-spec artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-openapi-spec.py` | Validate api-openapi-spec artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-contract-first]]
- [[api-documentation]]
- [[api-rest-design]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/openapi-user-api.yaml`

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageOffset'
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a new user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'

  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, name, status]
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: "Jane Doe"
        status:
          type: string
          enum: [active, inactive]
          default: active

    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: "Jane Doe"

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      properties:
        total: { type: integer, example: 100 }
        limit: { type: integer, example: 20 }
        offset: { type: integer, example: 0 }

    Error:
      type: object
      required: [error, code]
      properties:
        error: { type: string }
        code: { type: string }

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    PageLimit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    PageOffset:
      name: offset
      in: query
      schema:
        type: integer
        minimum: 0
        default: 0

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Conflict:
      description: Conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []

tags:
  - name: Users
    description: User management operations
```

### `templates/spectral.yaml`

```yaml
extends: ["spectral:oas"]
rules:
  operation-operationId: error
  operation-description: warn
  operation-tag-defined: error
  no-$ref-siblings: error
  oas3-server-trailing-slash: warn
  contact-properties: warn
  info-contact: warn
```

### `templates/validate-openapi.sh`

```bash
# validate-openapi.sh — pre-commit gate for OpenAPI specs.
# Usage: bash validate-openapi.sh [openapi.yaml]
set -euo pipefail
SPEC="${1:-openapi.yaml}"

[[ -f "$SPEC" ]] || { echo "no spec at $SPEC"; exit 1; }

# 1. Spectral structural + governance
npx --yes @stoplight/spectral-cli lint "$SPEC" --ruleset .spectral.yaml \
  || { echo "spectral failed"; exit 1; }

# 2. Redocly lint
npx --yes @redocly/cli lint "$SPEC" \
  || { echo "redocly failed"; exit 1; }

# 3. Example validation
npx --yes openapi-examples-validator "$SPEC" \
  || { echo "examples mismatch"; exit 1; }

# 4. Breaking change detection vs main
if git rev-parse origin/main >/dev/null 2>&1; then
  if git show origin/main:"$SPEC" > /tmp/main-spec.yaml 2>/dev/null; then
    oasdiff breaking /tmp/main-spec.yaml "$SPEC" --fail-on ERR || true
  fi
fi

echo "OpenAPI validation OK"
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-openapi-spec.json",
  "type": "object",
  "required": [
    "spec_id",
    "openapi_version",
    "info_x_versioning",
    "spectral_errors",
    "duplicate_schemas",
    "verdict"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^OAS-[A-Z0-9-]{2,40}$"
    },
    "openapi_version": {
      "type": "string",
      "enum": [
        "3.0",
        "3.0.1",
        "3.0.2",
        "3.0.3",
        "3.1.0"
      ]
    },
    "info_x_versioning": {
      "type": "object",
      "required": [
        "scheme",
        "deprecation_window_days"
      ]
    },
    "spectral_errors": {
      "type": "integer",
      "minimum": 0
    },
    "spectral_warnings": {
      "type": "integer",
      "minimum": 0
    },
    "duplicate_schemas": {
      "type": "integer",
      "minimum": 0
    },
    "security_aligned_with_auth_id": {
      "type": "string"
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
  "spec_id": "OAS-PUBLIC-API-V1",
  "openapi_version": "3.1.0",
  "info_x_versioning": {
    "scheme": "url-path",
    "deprecation_window_days": 180,
    "breaking_change_policy": "major-bump-required"
  },
  "spectral_errors": 0,
  "spectral_warnings": 3,
  "duplicate_schemas": 0,
  "security_aligned_with_auth_id": "AUTH-PARTNER-API",
  "verdict": "pass"
}
```
