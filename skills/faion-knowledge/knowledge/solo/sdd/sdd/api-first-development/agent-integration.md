# Agent Integration — API-First Development

## When to use
- Starting a new API — design the OpenAPI spec before writing any implementation code
- Frontend and backend are developed in parallel — the spec enables mock server for frontend while backend is being built
- Generating server stubs, client SDKs, or TypeScript types from a specification rather than writing them by hand
- Onboarding an LLM to implement or test an API — providing the full OpenAPI spec as context eliminates ambiguity and reduces hallucinations
- Validating that an existing implementation matches its documented contract (contract testing)
- Multiple consumers (web, mobile, third-party) will use the API — spec is the shared contract

## When NOT to use
- Internal one-off scripts or single-consumer CLI tools where no formal contract is needed
- Rapidly prototyping — write code first, extract spec after the API stabilizes; API-first adds upfront cost to throw-away spikes
- GraphQL APIs — GraphQL has its own SDL-first approach; OpenAPI does not map cleanly to GraphQL schemas
- Simple CRUD with no external consumers — the overhead of spec maintenance exceeds the benefit

## Where it fails / limitations
- Specs become stale if not auto-validated against the live implementation in CI — a spec that lies is worse than no spec
- OpenAPI 3.1 is not fully supported by all tooling (generators, validators) — some tools still target 3.0; check compatibility before using 3.1-specific features (`type: ['string', 'null']`, webhooks)
- Large, monolithic specs are hard for LLMs to reason about — split into multiple spec files and compose with `$ref` when endpoint count exceeds ~50
- Mock servers (Prism) generate responses from examples; if examples are missing or unrealistic, frontend teams build against misleading data
- Code generation from OpenAPI produces boilerplate that developers then customize — the generated code diverges from the spec over time unless regeneration is automated

## Agentic workflow
A spec-design agent takes natural language requirements and generates a draft OpenAPI 3.1 spec, then runs Spectral to lint it for style and consistency violations. A separate implementation agent reads the spec as its primary context and generates Django/FastAPI route stubs with request/response models derived directly from the spec schemas. A third validation agent runs `dredd` or `schemathesis` against the running server to verify the implementation matches the spec. The spec file is the handoff artifact between all three agents.

### Recommended subagents
- `spec-agent` (Sonnet/Opus) — generates and refines OpenAPI spec from requirements; runs Spectral linting
- `code-gen-agent` (Sonnet) — generates server stubs and client SDKs from spec using OpenAPI Generator
- `contract-test-agent` (Haiku) — runs schemathesis or dredd against live server, reports mismatches

### Prompt pattern
```
You are an API designer. Generate an OpenAPI 3.1 specification for the following API:

<requirements in natural language>

Requirements:
- Use OpenAPI 3.1 (no `version:` field quirks, use `type: ['string', 'null']` for nullable)
- Group endpoints with tags
- Include request/response examples for every endpoint
- Define reusable schemas in `components/schemas`
- Add descriptions to all fields — these descriptions are used for LLM code generation context

Return the full spec as a YAML code block.
```

```
Given this OpenAPI spec:
<spec>

Generate:
1. Django REST Framework viewsets for all endpoints, using the schema types directly
2. Pydantic models for request/response validation matching the spec schemas exactly
3. A list of any ambiguities in the spec that would require a design decision to implement

Mark every generated class/function with a comment: # Generated from OpenAPI spec <operationId>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `spectral` | Lint OpenAPI specs for style, consistency, and custom rules | `npm install -g @stoplight/spectral-cli` / [stoplight.io/spectral](https://stoplight.io/open-source/spectral) |
| `prism` | Run a mock server from an OpenAPI spec | `npm install -g @stoplight/prism-cli` / [stoplight.io/prism](https://stoplight.io/open-source/prism) |
| `openapi-generator-cli` | Generate server stubs and client SDKs in 50+ languages | `npm install -g @openapitools/openapi-generator-cli` / [openapi-generator.tech](https://openapi-generator.tech/) |
| `schemathesis` | Property-based contract testing against a live API | `pip install schemathesis` / [schemathesis.io](https://schemathesis.io/) |
| `redocly` | Lint, bundle, and preview OpenAPI specs | `npm install -g @redocly/cli` / [redocly.com](https://redocly.com/) |
| `dredd` | HTTP API testing tool that validates against OpenAPI/API Blueprint | `npm install -g dredd` / [dredd.readthedocs.io](https://dredd.readthedocs.io/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS | Yes — spec as files | Visual OpenAPI editor; stores specs as files agents can read/write |
| Swagger Editor | OSS | Yes — local/web | In-browser spec editor with live preview |
| Redocly | SaaS/OSS | Yes — CLI | Spec bundling, linting, docs hosting |
| Postman | SaaS | Partial — API | Import OpenAPI spec, generate collection; limited for agent automation |
| Bump.sh | SaaS | Yes — CI integration | Publish spec docs and detect breaking changes in CI |

## Templates & scripts
See `templates.md` for the full OpenAPI 3.1 spec skeleton and the Spectral ruleset config.

Spectral lint + Prism mock server startup (inline, 12 lines):
```bash
#!/bin/bash
# api-dev-start.sh — lint spec, start mock server
set -euo pipefail
SPEC="${1:-openapi.yaml}"

echo "Linting $SPEC with Spectral..."
spectral lint "$SPEC" --ruleset .spectral.yaml

echo "Starting Prism mock server on :4010..."
prism mock "$SPEC" --port 4010 --dynamic &
echo "Mock server PID: $!"
echo "API docs: http://localhost:4010/__docs"
```

## Best practices
- Add Spectral linting to CI as a required check — a spec that passes linting is the quality gate before implementation begins
- Include `example:` values in every schema field — Prism mock responses are generated from examples; missing examples produce useless mocks
- Keep specs in the same repository as the implementation and auto-validate in CI with schemathesis — spec drift is the primary failure mode
- Use `$ref` to define schemas once in `components/schemas` and reference them everywhere — duplication causes inconsistency
- Version the spec file itself with semantic versioning in `info.version`; treat MAJOR bumps as breaking changes requiring a new URL path (`/v2/`)
- When using LLMs to implement from spec, pass the full spec as context and instruct the model to use `operationId` values as function names — this creates a traceable mapping from spec to code

## AI-agent gotchas
- **Spec → code mapping must be maintained.** Agents that generate code from a spec and then modify the spec must regenerate the affected code — generated code diverges silently if not re-synchronized. Add a hash of the spec to generated files as a drift detector
- **Large specs exceed context windows.** For APIs with 100+ endpoints, agents must work on one tag group at a time rather than processing the full spec at once
- **Prism mock responses are only as good as the examples.** Agents that generate specs without realistic examples produce mocks that return empty strings and zero values; always generate plausible example data
- **OpenAPI 3.1 vs 3.0 tooling compatibility.** Agents must check the target generator or validator for 3.1 support before using 3.1-specific syntax; some tools silently accept 3.1 YAML but parse it as 3.0, dropping features
- **Contract tests (schemathesis) find real bugs.** When a contract test fails, the agent must determine whether the spec or the implementation is correct — never auto-fix the spec to match a buggy implementation

## References
- [OpenAPI 3.1 specification](https://spec.openapis.org/oas/v3.1.0)
- [OpenAPI best practices](https://learn.openapis.org/best-practices.html)
- [Spectral linting](https://stoplight.io/open-source/spectral)
- [Prism mock server](https://stoplight.io/open-source/prism)
- [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)
- [schemathesis contract testing](https://schemathesis.io/)
- [Multi-agent API development (arxiv)](https://arxiv.org/html/2510.19274v1)
