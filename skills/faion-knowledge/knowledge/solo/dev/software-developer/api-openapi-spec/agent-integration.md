# Agent Integration — OpenAPI Specification

## When to use
- Designing or evolving any HTTP/JSON API meant for >1 consumer.
- API documentation must stay in sync with implementation (regen docs on every spec PR).
- Generating typed SDK clients for FE / mobile / partners.
- Mocking endpoints for FE devs while BE is in flight (Prism, Mockoon).
- Contract testing with Schemathesis / Dredd against staging.
- Replacing handwritten Postman collections with a single source of truth.

## When NOT to use
- GraphQL APIs — use SDL / GraphQL schema; OpenAPI for GQL is awkward.
- gRPC / protobuf services — `.proto` is the contract.
- Trivial internal endpoints with one consumer (the same service team).
- Server-rendered HTML apps (Django templates, Rails views).
- Streaming APIs (SSE, WebSockets) with rich semantics — AsyncAPI is the right spec.
- Tightly coupled libraries (Python imports), where a function signature is the contract.

## Where it fails / limitations
- Discriminated unions (`oneOf` + `discriminator`) generate inconsistent code per language.
- File uploads (`multipart/form-data`) need careful schema; many generators botch them.
- Auth flows: only declarative parts (Bearer, API key, OAuth2 URLs) — actual flow logic stays in code/docs.
- Spec linters miss semantic mistakes (correct shape, wrong status code, swapped pagination semantics).
- Large specs (>5k lines) are slow to lint and unreviewable as a single PR — split files + bundle.
- OpenAPI 3.1 ↔ JSON Schema 2020-12 alignment is real but tooling lags (some validators only support 3.0).
- Versioning a public API across breaking changes requires multiple specs (`v1.yaml`, `v2.yaml`) + redirect strategy.

## Agentic workflow
Drive spec authoring as: (1) agent reads PRD / feature spec, (2) drafts new paths + schemas referencing existing components, (3) runs `redocly lint` and `oasdiff breaking` automatically, (4) emits diff for human review, (5) on approval, runs codegen for server stubs + client SDK + contract tests. The spec is **authored** (not generated from code) — code generation flows from spec, not the reverse. Pair with `contract-first-development` methodology for full lifecycle.

### Recommended subagents
- `faion-api-agent` — primary author of OpenAPI specs, owns `$ref` reuse and naming.
- `faion-sdd-executor-agent` — implements server stubs + tests once spec is approved.
- `faion-feature-executor` — sequences spec-draft → lint → review → impl tasks.

### Prompt pattern
```
Add new endpoint <method> <path> to openapi.yaml. Use existing
components/schemas where possible (list before adding new). Required:
operationId, tags, request body schema with example, all response codes
including 4xx via $ref to components/responses. After write, run
`redocly lint openapi.yaml` and `npx @stoplight/spectral-cli lint openapi.yaml`.
Stop on lint errors.
```

```
Compare openapi.yaml between HEAD and main. Output: (1) breaking changes
per oasdiff, (2) new operations, (3) deprecated operations. Format as
PR comment markdown.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redocly cli` | Lint, bundle, preview, split, diff | npm i -g @redocly/cli |
| `spectral` | Custom rule linter (governance) | npm i -g @stoplight/spectral-cli |
| `swagger-cli` | Validate, bundle multi-file specs | npm i -g swagger-cli |
| `openapi-generator-cli` | Stubs + SDKs in 50+ languages | npm i -g @openapitools/openapi-generator-cli |
| `openapi-typescript` | Fast TS types from spec | npm i -D openapi-typescript |
| `oasdiff` | Breaking-change detection | go install github.com/Tufin/oasdiff |
| `prism mock` | Mock server from spec | npm i -g @stoplight/prism-cli |
| `prism proxy` | Live spec validation against real backend | bundled |
| `schemathesis` | Property-based contract testing | pip install schemathesis |
| `vacuum` | Fast Go-based linter | https://quobix.com/vacuum/ |
| `swagger-codegen` | Older alternative to openapi-generator | https://github.com/swagger-api/swagger-codegen |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SwaggerHub | SaaS | yes (API) | Hosted spec editor + style guides + codegen. |
| Stoplight | SaaS | yes | Visual spec editor + governance + mocking. |
| Redocly | SaaS+OSS | yes | Best docs renderer; Workflows for CI/CD spec ops. |
| Bump.sh | SaaS | yes (CLI) | Versioned hosting + Slack/PR diff notifications. |
| Postman | SaaS | yes (API) | Imports OpenAPI; generates collections + tests. |
| ReadMe | SaaS | yes (rdme CLI) | Developer hub built from OpenAPI. |
| Mintlify | SaaS | yes | Modern docs from OpenAPI; Anthropic-style. |
| Apicurio | OSS | yes | Self-hosted spec registry with semver. |
| Scalar | OSS | yes | Modern free Redoc alternative. |
| Zuplo | SaaS | yes | API gateway built directly from OpenAPI. |

## Templates & scripts
See `templates.md` for full skeleton spec. Inline minimal validator:

```bash
#!/usr/bin/env bash
# scripts/validate-openapi.sh — pre-commit gate
set -euo pipefail
SPEC="${1:-openapi.yaml}"

[[ -f "$SPEC" ]] || { echo "no spec at $SPEC"; exit 1; }

# 1. structural
npx --yes @stoplight/spectral-cli lint "$SPEC" --ruleset .spectral.yaml \
  || { echo "spectral failed"; exit 1; }

# 2. redocly governance
npx --yes @redocly/cli lint "$SPEC" \
  || { echo "redocly failed"; exit 1; }

# 3. examples match schema
npx --yes openapi-examples-validator "$SPEC" \
  || { echo "examples mismatch"; exit 1; }

# 4. breaking changes vs main
if git rev-parse origin/main >/dev/null 2>&1; then
  git show origin/main:"$SPEC" > /tmp/main-spec.yaml 2>/dev/null \
    && oasdiff breaking /tmp/main-spec.yaml "$SPEC" --fail-on ERR \
    || true
fi

echo "openapi validation OK"
```

Recommended `.spectral.yaml`:

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

## Best practices
- Treat the spec as code: PR review, codeowners, semver, conventional commits.
- Split into multiple files (`paths/users.yaml`, `components/schemas/user.yaml`) and bundle in CI.
- Use `operationId` everywhere; SDKs become method names.
- Include realistic `examples`; Prism mocks use them, devs see them in docs.
- Centralize errors in `components/responses/Errors.yaml`; reuse via `$ref`.
- Pin codegen + linter versions; treat upgrades as PRs.
- Generate types into a separate package (`@org/api-types`) and version it; consumers import.
- Keep request/response schemas separate (`UserCreate` vs `User`) — don't reuse the response shape as input.
- Document pagination, errors, and rate limits at top-level (in `description` and as headers); inheriting from a base ensures consistency.
- Add `x-` extensions for org-specific metadata (`x-rate-limit`, `x-internal`) and document them in `.spectral.yaml`.

## AI-agent gotchas
- LLMs hallucinate JSON Schema keywords (`format: phone-number`, `format: ssn`) — pin to OpenAPI 3.1 + JSON Schema 2020-12 spec; spectral catches.
- Agents add new schemas instead of `$ref`-ing existing ones — drift. Force a "list existing schemas first" step.
- LLMs default to OpenAPI 3.0; check `openapi: 3.1.0` is preserved across edits.
- Generators silently truncate on unknown formats — review generated SDK types, don't trust `redocly lint` alone.
- Long specs blow context; agents drop `$ref` anchors when summarizing. Always edit a slice (single path/schema), not whole file.
- Code-gen drift: agents regenerate stubs and overwrite hand-written impl. Mark stubs read-only via `.openapi-generator-ignore` for service classes.
- Agents asked to "version the API" produce ambiguous results — define versioning policy explicitly (URI path, header, content-negotiation) before asking.
- Human-in-loop checkpoint: any breaking change (`oasdiff` reports ERR) must be human-approved + bumped via semver-major; agents should never auto-merge.
- Examples generated by LLMs can include real-looking PII / API keys — scan with `gitleaks` before commit.

## References
- OpenAPI 3.1 spec — https://spec.openapis.org/oas/v3.1.0
- JSON Schema 2020-12 — https://json-schema.org/draft/2020-12/json-schema-core
- Redocly governance docs — https://redocly.com/docs/cli/guides/api-governance/
- Spectral built-in OAS ruleset — https://meta.stoplight.io/docs/spectral/4dec24461f3af-open-api-rules
- OpenAPI Generator — https://openapi-generator.tech/
- "API styleguide" (Adidas) — https://github.com/adidas/api-guidelines
- "API design notes" (Microsoft REST guide) — https://github.com/microsoft/api-guidelines
