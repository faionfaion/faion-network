# Agent Integration — API-First Development

## When to use
- Multiple consumers exist or are planned (frontend, mobile, third-party) before backend code is written
- Frontend and backend teams (or agents) work in parallel — mock server unblocks frontend while backend is implemented
- Public or partner-facing API where contract stability is a hard requirement
- Microservice boundaries: each service contract must be agreed upon before implementation begins
- SDK generation is needed (client libraries from spec)
- API governance is required — linting rules enforce naming conventions, versioning, error format across services

## When NOT to use
- Internal single-consumer service where spec would be written after implementation anyway (YAGNI)
- Rapid prototype or proof-of-concept with fewer than 3 endpoints — design overhead exceeds benefit
- GraphQL-first projects: OpenAPI is REST-specific; AsyncAPI serves event-driven; pick the right contract format
- When the team has no CI pipeline to enforce spec compliance — spec drift will occur within weeks

## Where it fails / limitations
- "Design before code" discipline breaks down under deadline pressure; agents cannot enforce this without process hooks (e.g., CI gate that blocks merge without updated spec)
- OpenAPI spec and implementation diverge silently unless contract tests (Dredd, Pact) run in CI — spec becomes documentation, not truth
- Mock servers (Prism) serve stub data, not real business logic; frontend teams build against mocks and then hit unexpected behaviors when connecting to real backend
- Spectral rules require curation per project — default rulesets flag too many style issues; un-curated, they slow iteration without adding safety
- Code generation (openapi-generator) produces boilerplate that developers modify and then drift from the spec; regeneration overwrites customizations

## Agentic workflow
An agent can draft the initial OpenAPI 3.1 spec from a feature `spec.md` (FR-X → endpoint mapping), run Spectral linting programmatically, and generate a Prism mock server command. The implementation agent then codes against the spec, and a post-implementation Dredd or Pact run validates compliance. The spec file is the single source of truth that flows through draft → linted → mock-verified → contract-tested states.

### Recommended subagents
- `faion-sdd-executor-agent` — executes design-phase tasks including OpenAPI spec creation and linting validation as part of the implementation plan wave

### Prompt pattern
```
From the following functional requirements, generate an OpenAPI 3.1 spec.
Requirements: <paste FR-X list>
Constitution: <auth method, base URL, error format>

Rules:
- One operationId per endpoint, camelCase
- All error responses reference #/components/responses/Error
- Include at least one request example per POST/PUT/PATCH endpoint
- Nullable fields use type: ['string', 'null'] (OAS 3.1 style)

Output: valid YAML only. No prose explanation.
```

```
Lint this OpenAPI spec with Spectral default ruleset.
List violations grouped by: (1) errors that break mock server, (2) warnings
that affect SDK generation, (3) style issues that can be deferred.
Do not fix — report only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Spectral | OpenAPI/AsyncAPI linting with configurable rules | `npm install -g @stoplight/spectral-cli` / https://stoplight.io/open-source/spectral |
| Prism | Mock server and proxy from OpenAPI spec | `npm install -g @stoplight/prism-cli` / https://github.com/stoplightjs/prism |
| Dredd | HTTP contract testing — spec vs. running server | `npm install -g dredd` / https://dredd.readthedocs.io |
| openapi-generator-cli | Client/server code generation from OpenAPI spec | `npm install -g @openapitools/openapi-generator-cli` / https://openapi-generator.tech |
| Redocly CLI | Bundle, lint, preview OpenAPI docs | `npm install -g @redocly/cli` / https://redocly.com/docs/cli |
| swagger-cli | Validate and bundle multi-file OpenAPI specs | `npm install -g @apidevtools/swagger-cli` / https://github.com/APIDevTools/swagger-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS + OSS desktop | Partial | Visual OpenAPI editor; no scripting API |
| Swagger Editor / Hub | SaaS | Partial | Real-time validation; SwaggerHub has REST API for spec storage |
| Postman | SaaS | Yes — REST API | Import spec, generate tests, mock server; Postman API for automation |
| Bump.sh | SaaS | Yes — CLI | API changelog + diff; `bump diff` detects breaking changes in CI |
| Pact | OSS | Yes — CLI | Consumer-driven contract tests; broker available as SaaS (Pactflow) |

## Templates & scripts
See `templates.md` for the full OpenAPI 3.1 spec template. Also see README.md which includes an inline template.

Prism mock server + Spectral lint in one script:
```bash
#!/usr/bin/env bash
# usage: ./api-first-check.sh openapi.yaml
set -euo pipefail
SPEC="$1"
echo "--- Linting spec ---"
spectral lint "$SPEC" --ruleset .spectral.yaml || { echo "Lint failed"; exit 1; }
echo "--- Starting mock server on :4010 ---"
prism mock "$SPEC" --port 4010 &
PRISM_PID=$!
sleep 2
echo "--- Mock server PID: $PRISM_PID ---"
echo "Run: curl http://localhost:4010/your-endpoint"
echo "Press Ctrl+C to stop"
wait $PRISM_PID
```

## Best practices
- Write the spec in YAML, not JSON — YAML supports `$ref` splits across files, comments, and is more readable for large schemas
- Version the spec file in the same commit as the first implementation task — never let the spec live in a separate PR
- Set up Spectral in CI as a pre-merge gate before writing any backend code — breaking lint means a broken contract
- Use `operationId` on every endpoint — SDK generators and mock routers depend on it; blank operationIds produce unusable output
- Define global error schemas (`#/components/schemas/Error`, `#/components/responses/Unauthorized`) once and reference everywhere — prevents inconsistent error formats across endpoints
- Run `bump diff` or equivalent on every PR to surface breaking changes before they hit consumers

## AI-agent gotchas
- Agents generate syntactically valid OpenAPI but miss semantic issues: `$ref` to non-existent component, missing `required` on mandatory fields, wrong `format` for dates — always run Spectral after generation
- Mock server responses are spec-driven stubs; agents writing frontend code against mocks will write code that silently breaks on real backend because mocks don't enforce business rules
- Agents will default to OAS 3.0 patterns (`nullable: true`) in OAS 3.1 specs — the correct 3.1 form is `type: ['string', 'null']`; specify the version explicitly in the prompt
- Contract drift: if the agent modifies the backend implementation without updating the spec, Dredd will fail — configure CI to run Dredd and fail the PR
- Human-in-loop checkpoint: spec changes that break existing consumers require human approval before merging; agents should flag `Breaking change detected` and stop

## References
- https://spec.openapis.org/oas/v3.1.0 (OpenAPI 3.1 official specification)
- https://stoplight.io/open-source/spectral (Spectral linting)
- https://dredd.readthedocs.io (Dredd contract testing)
- https://docs.pact.io (Pact consumer-driven contract testing)
- https://bump.sh/blog/what-is-api-contract-testing (API contract testing overview)
- "API Design Patterns" — JJ Geewax (Manning)
