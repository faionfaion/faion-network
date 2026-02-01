# API-First Development

API-first development is a strategy where the API contract (specification) is designed before any code is written. The specification becomes the single source of truth, driving code generation, documentation, testing, and client SDK creation.

## Why API-First?

### Traditional Approach (Code-First) Problems

- APIs designed after implementation lead to inconsistent designs
- Breaking changes for consumers
- Documentation that doesn't match reality
- Frontend/mobile teams blocked waiting for backend

### API-First Benefits

| Benefit | Description |
|---------|-------------|
| **Parallel development** | Frontend and backend teams work simultaneously using mocks |
| **Contract as spec** | LLMs generate code directly from structured OpenAPI definitions |
| **Early testing** | QA begins before implementation is complete |
| **Living documentation** | Docs stay accurate with zero maintenance |
| **SDK generation** | Client libraries auto-generated from spec |
| **Reduced hallucinations** | Strongly-typed specs eliminate LLM ambiguity |

## API-First for LLM Code Generation

LLMs require structured, machine-readable contracts to understand API functionality. OpenAPI specifications act as "hand-holding" for LLMs, significantly reducing errors.

### Why OpenAPI Works for LLMs

1. **Structured format** - JSON/YAML is easily parsed by LLMs
2. **Type information** - Schemas provide explicit types, reducing hallucinations
3. **Examples included** - Request/response examples guide generation
4. **Validation rules** - Constraints (min/max, patterns) are explicit
5. **Natural language descriptions** - Human-readable fields improve AI understanding

### LLM + OpenAPI Integration Benefits

| Capability | Description |
|------------|-------------|
| **Code generation** | Generate server stubs, client SDKs in any language |
| **Documentation** | Generate human-readable docs from technical specs |
| **Test generation** | Create test cases from endpoint specifications |
| **API queries** | Natural language questions about API functionality |
| **Validation** | Verify implementation matches contract |

## OpenAPI 3.1 Features

OpenAPI 3.1 (released 2021) introduced significant improvements:

| Feature | Description |
|---------|-------------|
| **JSON Schema alignment** | Full JSON Schema vocabularies support (draft 2020-12) |
| **Webhooks** | Top-level `webhooks` element for event-driven APIs |
| **$ref improvements** | Better reference handling, sibling keywords allowed |
| **Nullable simplification** | Use `type: ['string', 'null']` instead of `nullable: true` |
| **contentMediaType** | Describe encoding of string content |
| **Deprecation** | `deprecated: true` keyword for sunset planning |

### OpenAPI 3.1 vs 3.0

```yaml
# OpenAPI 3.0 nullable
nullable: true
type: string

# OpenAPI 3.1 nullable (JSON Schema aligned)
type: ['string', 'null']
```

## API-First Workflow

```
DESIGN -> VALIDATE -> MOCK -> IMPLEMENT -> TEST -> DEPLOY
   |         |          |         |          |
OpenAPI   Spectral    Prism    codegen    contract
  spec    linting    server   from spec    tests
```

### Phases

1. **Design** - Write OpenAPI specification collaboratively
2. **Validate** - Lint with Spectral for consistency and best practices
3. **Mock** - Deploy mock server (Prism) for frontend development
4. **Implement** - Generate server stubs, implement business logic
5. **Test** - Contract testing ensures backend matches spec
6. **Deploy** - Generate client SDKs, publish documentation

## Versioning Strategies

### Approaches

| Strategy | Format | Pros | Cons |
|----------|--------|------|------|
| **URL Path** | `/v1/users` | Visible, cacheable | URL management |
| **Header** | `Accept: application/vnd.api.v2+json` | RESTful | Harder to test |
| **Query Param** | `/users?version=2` | Flexible | Caching issues |

### Semantic Versioning

Use MAJOR.MINOR.PATCH:
- **MAJOR** - Breaking changes (v1 -> v2)
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes

### OpenAPI Version Management

```yaml
info:
  title: My API
  version: 2.1.0  # Semantic version
```

Best practice: Maintain separate OpenAPI documents per major version.

## Tools Ecosystem

| Category | Tools |
|----------|-------|
| **Editor** | [Swagger Editor](https://editor.swagger.io/), [Stoplight Studio](https://stoplight.io/studio) |
| **Linting** | [Spectral](https://stoplight.io/open-source/spectral), [Redocly](https://redocly.com/) |
| **Mocking** | [Prism](https://stoplight.io/open-source/prism), WireMock |
| **Documentation** | Swagger UI, [Redoc](https://redocly.com/redoc), Stoplight |
| **Code Generation** | [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator), openapi-stack |
| **Contract Testing** | Pact, Dredd |
| **Security** | OWASP ZAP |

## Multi-Agent Systems for API-First

Recent research (2025-2026) shows LLM-based multi-agent systems can automate the full API-first workflow:

1. **Spec Agent** - Generates OpenAPI from natural language requirements
2. **Code Agent** - Generates server implementation from spec
3. **Test Agent** - Creates and runs contract tests
4. **Refine Agent** - Iterates based on test failures

Key insight: Keep specifications small and focused for better LLM generation quality.


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related Files

- [checklist.md](checklist.md) - API-first development checklist
- [examples.md](examples.md) - OpenAPI specification examples
- [templates.md](templates.md) - Reusable OpenAPI templates
- [llm-prompts.md](llm-prompts.md) - LLM prompts for API design

## Sources

- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0) - Official standard
- [OpenAPI Best Practices](https://learn.openapis.org/best-practices.html) - Official guide
- [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) - Code generation
- [Spectral Linting](https://stoplight.io/open-source/spectral) - Validation rules
- [API Versioning Best Practices](https://redocly.com/blog/api-versioning-best-practices) - Versioning guide
- [LLM + OpenAPI Integration](https://stackon.cloud/blog/llm-openapi-integration-for-seamless-api-development) - AI integration
- [Multi-Agent API Development](https://arxiv.org/html/2510.19274v1) - Research paper
