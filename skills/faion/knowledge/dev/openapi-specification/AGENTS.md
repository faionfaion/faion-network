# OpenAPI Specification

## Summary

**One-sentence:** Authoring + CI gates for an OpenAPI 3.1 spec: one canonical bundle, $ref reuse, operationId everywhere, breaking-change gate via oasdiff, generator-spec drift detection.

**One-paragraph:** OpenAPI documents rot the moment they diverge from server code, generators silently emit unsafe clients when required arrays are missing, and operationIds drift on path renames. This methodology fixes a contract-first authoring loop: one canonical openapi.yaml at repo root + redocly bundle for distribution; every operation carries operationId in kebab/camel; every reusable schema lives under components/* and is referenced via $ref; every response code carries named examples; Spectral + redocly lint on every PR; oasdiff blocks breaking changes; server-generated specs commit a snapshot and CI fails on drift.

**Ефективно для:**

- Перший API контракт - треба зафіксувати форму до імплементації.
- Server-generated spec (FastAPI / drf-spectacular / NestJS) дрейфує - потрібен gate.
- Клієнти ламаються на breaking change - треба oasdiff на PR.
- Кодген видає any замість union - перевірити discriminator.
- Команда забуває required array - типи стають Partial.

## Applies If (ALL must hold)

- Project ships an HTTP API consumed by external or internal clients.
- Spec will be the source of truth for generated clients and mock servers.
- CI infrastructure exists where linters and diff gates can run.
- A repository owner can sign off breaking-change overrides.

## Skip If (ANY kills it)

- Project is a throwaway prototype with no API consumers.
- API surface is GraphQL or gRPC only - use the appropriate schema language.
- Spec drift is intentional during a refactor (use a feature branch).
- Team prefers AsyncAPI for event-driven APIs - use that spec instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| API requirements | markdown user stories or specs | product |
| Auth model | OAuth2 / JWT / API key description | security |
| Error-shape decision | RFC 7807 problem+json yes/no | engineering |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | consumer of the path/verb shape this spec freezes. |
| [[api-error-handling]] | consumer of the error schema this spec references. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: single bundle, operationId everywhere, $ref reuse, required array, oasdiff gate, named examples, server-spec drift check | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step contract-first authoring + CI wiring | ~900 |
| `content/05-examples.xml` | essential | Worked example contract-first vs server-generated | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-operations` | sonnet | Per-endpoint judgement; operationId + request/response shape. |
| `lift-components` | haiku | Mechanical $ref extraction once duplicates are flagged. |
| `configure-linters` | haiku | Boilerplate .redocly.yaml + .spectral.yaml. |
| `review-breaking-diff` | opus | Stakes high; one wrong call breaks every client. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-skeleton.yaml` | OpenAPI 3.1 skeleton with components reuse + security + named examples. |
| `templates/openapi-base.yaml` | Minimal OpenAPI 3.1 base for a brand-new service (info + servers + components shell). |
| `templates/openapi-ci.yml` | GitHub Actions workflow wiring Spectral + oasdiff gates on every PR. |
| `templates/spectral.yaml` | Spectral ruleset enforcing required arrays, named examples, security on operations. |
| `templates/_smoke-test.json` | Minimum viable artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-openapi-specification.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[api-rest-design]]
- [[api-error-handling]]
- [[api-documentation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - source authority (hand vs generated), lint status, breaking-diff presence - onto a rule from `content/01-core-rules.xml`. Use it before touching the spec: it decides apply-vs-skip, picks the source-of-truth path, and routes BREAK diffs to human review.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/openapi-skeleton.yaml`

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
security:
  - bearerAuth: []
paths:
  /users/{id}:
    get:
      operationId: get-user
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              examples:
                UserActive:
                  $ref: '#/components/examples/UserActive'
        '404':
          $ref: '#/components/responses/NotFound'
components:
  schemas:
    User:
      type: object
      required: [id, email, name]
      properties:
        id: { type: string, format: uuid }
        email: { type: string, format: email }
        name: { type: string, minLength: 1, maxLength: 100 }
  parameters:
    UserId:
      name: id
      in: path
      required: true
      schema: { type: string, format: uuid }
  responses:
    NotFound:
      description: Resource not found
      content:
        application/problem+json:
          schema:
            type: object
            required: [type, title, status]
  examples:
    UserActive:
      summary: Active user
      value: { id: '550e8400-e29b-41d4-a716-446655440000', email: 'a@b.co', name: 'Ada' }
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### `templates/openapi-base.yaml`

```yaml
openapi: 3.1.0
info:
  title: Service API
  version: 1.0.0
  description: Replace with service description.

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /users:
    get:
      summary: List users
      operationId: list-users
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
      summary: Create user
      operationId: create-user
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

  /users/{userId}:
    get:
      summary: Get user
      operationId: get-user
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
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
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
        name:
          type: string
          minLength: 1
          maxLength: 100

    UserList:
      type: object
      required: [data, meta]
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      required: [total, limit, offset]
      properties:
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string

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
      description: Authentication required
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

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

tags:
  - name: Users
    description: User management
```

### `templates/openapi-ci.yml`

```yaml
name: openapi

on: [pull_request]

jobs:
  lint-and-diff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install tools
        run: npm i -g @redocly/cli @stoplight/spectral-cli

      - name: Redocly lint
        run: redocly lint openapi.yaml

      - name: Spectral lint
        run: spectral lint openapi.yaml --fail-severity=warn

      - name: Breaking-change diff
        run: |
          git show origin/main:openapi.yaml > /tmp/base.yaml
          docker run --rm \
            -v "$PWD:/specs" \
            -v /tmp:/tmp \
            tufin/oasdiff breaking /tmp/base.yaml /specs/openapi.yaml --fail-on ERR
```

### `templates/spectral.yaml`

```yaml
extends: ['spectral:oas']
rules:
  operation-operationId: error
  operation-description: warn
  oas3-schema-required: error
  no-additionalProperties-true-on-response: error
  named-examples-required: error
  operation-security-defined: error
```

### `templates/_smoke-test.json`

```json
{
  "openapi_version": "3.1.0",
  "canonical_path": "openapi.yaml",
  "lint_config": {
    "redocly": ".redocly.yaml",
    "spectral": ".spectral.yaml"
  },
  "breaking_change_gate": {
    "enabled": true,
    "tool": "oasdiff"
  },
  "operation_id_coverage": {
    "covered": 1,
    "total": 1
  }
}
```
