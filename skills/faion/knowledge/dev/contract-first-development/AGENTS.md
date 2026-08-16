# Contract-First Development

## Summary

**One-sentence:** Design OpenAPI contracts before writing implementation code so stubs, SDKs, and mocks all derive from the spec.

**One-paragraph:** Code-first APIs drift between consumers and providers; contract-first inverts the flow. Authors commit an OpenAPI 3.1 spec, lint it with spectral, regression-check it with oasdiff, and only then generate server stubs, client SDKs, and mock servers from it. The spec is treated like source — PR review, semver, breaking-change gates in CI. Hand-edits to generated stubs are forbidden; changes flow through the spec.

**Ефективно для:**

- New APIs with multiple consumers building in parallel (FE, mobile, partners).
- Public or partner APIs where stable versioning is contractual.
- AI-agent-generated services that need a deterministic contract to anchor regeneration.
- Microservice boundaries where service contracts are the integration surface.

## Applies If (ALL must hold)

- New API with multiple consumers (frontend, mobile, partners) planned or existing.
- Cross-team handoff where BE and FE build in parallel.
- Public or partner APIs needing stable, versioned, machine-readable contracts.
- AI-agent-generated services where spec prevents drift between iterations.
- Microservices where service boundaries are evolving and need explicit contracts.

## Skip If (ANY kills it)

- One-off internal scripts or single-team tools where overhead exceeds value.
- Highly experimental endpoints during prototyping (spec churn dominates).
- Pure GraphQL stacks — schema-first GraphQL achieves the same with different tooling.
- gRPC — `.proto` is already the contract; different tools apply.
- Server-rendered web apps where the API is HTML forms, not JSON.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource model + lifecycle states | bullet list or ERD | product / domain |
| Consumer list with platform + auth model | table | tech-lead |
| Auth scheme + error contract decisions | ADR or note | architect |
| OpenAPI tooling versions (spectral, oasdiff, codegen) | pinned versions | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[rest-api-design]] | Defines the REST conventions the spec encodes. |
| [[api-versioning]] | The breaking-change policy oasdiff enforces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (spec-first, $ref reuse, spectral, oasdiff, codegen-not-handedit, semver) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: scope → draft → lint → review → generate → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: paginated resource API | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `spec_drafting` | opus | Schema design + auth + error contract requires deep synthesis. |
| `spectral_rule_authoring` | sonnet | Mechanical: encode lint rules from style guide. |
| `oasdiff_gate_setup` | sonnet | Pipeline plumbing. |
| `codegen_pipeline` | sonnet | Wire generators (openapi-generator / orval) into build. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-scaffold.yaml` | OpenAPI 3.1 skeleton with resource, list, create, errors, security |
| `templates/spectral.yaml` | Spectral ruleset extending `spectral:oas` |
| `templates/check-spec-drift.sh` | CI script that runs spectral + oasdiff between PR and main |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contract-first-development.py` | Validate the spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rest-api-design]]
- [[api-versioning]]
- [[openapi-specification]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (consumer count, spec stability, auth complexity) to a rule from `01-core-rules.xml`, telling the agent whether to invoke full contract-first, light SDL-only design, or skip the methodology because preconditions fail. Walk it on every fresh invocation.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/openapi-scaffold.yaml`

```yaml
openapi: 3.1.0
info:
  title: Example API
  version: 1.0.0
  description: Replace with feature-specific description.
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      tags: [Resources]
      parameters:
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageOffset'
      responses:
        '200':
          description: List of resources
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create resource
      operationId: createResource
      tags: [Resources]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceRequest'
      responses:
        '201':
          description: Resource created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    Resource:
      type: object
      required: [id, name]
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        name:
          type: string
          minLength: 1
          maxLength: 200

    CreateResourceRequest:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200

    ResourceList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      properties:
        total: { type: integer }
        limit: { type: integer }
        offset: { type: integer }

    Error:
      type: object
      required: [error, code]
      properties:
        error: { type: string }
        code: { type: string }

  parameters:
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

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []

tags:
  - name: Resources
    description: Resource management operations
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

### `templates/check-spec-drift.sh`

```bash
# check-spec-drift.sh — fail CI if generated code diverges from server/ or spec has breaking changes.
# Usage: bash check-spec-drift.sh [openapi.yaml]
set -euo pipefail

SPEC="${1:-openapi.yaml}"
GENERATED_DIR=$(mktemp -d)

# 1. Lint spec
redocly lint "$SPEC" || { echo "redocly lint failed"; exit 1; }
npx --yes @stoplight/spectral-cli lint "$SPEC" --ruleset .spectral.yaml \
  || { echo "spectral lint failed"; exit 1; }

# 2. Generate stubs and diff against committed server models
openapi-generator-cli generate \
  -i "$SPEC" -g python-fastapi -o "$GENERATED_DIR" \
  --additional-properties=packageName=app

DIFF=$(diff -r --brief "$GENERATED_DIR/app/models" server/app/models 2>&1 || true)
if [[ -n "$DIFF" ]]; then
  echo "Spec vs implementation drift detected:"
  echo "$DIFF"
  echo "Run: cp -r $GENERATED_DIR/app/models server/app/models"
  exit 1
fi

# 3. Breaking change check vs main branch
git fetch origin main:main 2>/dev/null || true
if git show main:"$SPEC" > /tmp/spec-main.yaml 2>/dev/null; then
  oasdiff breaking /tmp/spec-main.yaml "$SPEC" --fail-on ERR
fi

echo "Spec drift check OK"
```
