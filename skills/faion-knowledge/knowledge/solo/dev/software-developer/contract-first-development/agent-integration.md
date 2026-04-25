# Agent Integration — Contract-First Development

## When to use
- New API where multiple consumers (FE, mobile, partners) exist or are planned.
- Cross-team handoff: BE and FE built in parallel, no time to wait for "done" backend.
- Public/partner APIs that need stable, versioned, machine-readable contracts.
- Microservices where service boundaries are evolving and need explicit contracts to prevent drift.
- AI-agent-generated services — the spec becomes the deterministic source the LLM cannot drift from.

## When NOT to use
- One-off internal scripts, cron jobs, single-team tools where contract overhead exceeds value.
- Highly experimental endpoints during prototyping (spec churn dominates).
- Pure GraphQL stacks — schema-first GraphQL achieves the same outcome with different tooling.
- gRPC services — `.proto` is already the contract; this methodology applies but tools differ.
- Server-rendered web apps where the "API" is HTML forms, not JSON.

## Where it fails / limitations
- Generated stubs for OpenAPI 3.1 are uneven across languages — Python FastAPI generator lags spec features.
- Spec-vs-implementation drift if regen isn't enforced in CI; teams hand-edit generated code "just this once".
- `oneOf` / `anyOf` / discriminator support varies between generators — complex polymorphism breaks codegen.
- Auth flows (OAuth2 redirects, MFA) cannot be fully expressed; you still need narrative docs.
- Spec linters can pass while the API is semantically broken (wrong status codes, wrong pagination shape).
- Large monolith specs (>5k lines) become unreviewable — split by tag/domain or use `$ref` across files.
- Generated TypeScript clients use untagged unions for `oneOf`; consumers need additional type guards.

## Agentic workflow
Drive contract-first as: (1) agent drafts OpenAPI from PRD/feature spec, (2) human + spectral lint, (3) approved spec triggers codegen for server stubs + client SDK + contract tests, (4) implementer agent fills only `# TODO`-marked methods, (5) CI re-generates and diffs to detect drift. The spec file lives at the repo root as `openapi.yaml`; treat its commits as breaking-change events — they trigger consumer regen.

### Recommended subagents
- `faion-api-agent` — owns OpenAPI authoring, breaking-change detection, generator config.
- `faion-sdd-executor-agent` — implements business logic against generated stubs under SDD gates.
- `faion-feature-executor` — orchestrates the spec → codegen → impl → test sequence as discrete tasks.

### Prompt pattern
```
Read .product/features/<feature>/spec.md. Produce openapi.yaml fragment
covering only the new endpoints. Use $ref for shared schemas already in
components/schemas. Include 4xx error responses from
components/responses/*. Stop. Do not implement.
```

```
Run `redocly lint openapi.yaml`. Run `openapi-generator generate -i
openapi.yaml -g python-fastapi -o ./generated`. Diff generated/models
against server/models and surface mismatches. Do not edit either side
yet — surface diff for review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `redocly cli` | Lint, bundle, preview, diff specs | npm i -g @redocly/cli |
| `spectral` | Customizable OpenAPI linter | npm i -g @stoplight/spectral-cli |
| `openapi-generator-cli` | Multi-language client/server stubs | npm i -g @openapitools/openapi-generator-cli |
| `oasdiff` | Detect breaking changes between two specs | go install github.com/Tufin/oasdiff |
| `prism` | Mock server from spec, validation proxy | npm i -g @stoplight/prism-cli |
| `schemathesis` | Property-based contract testing from spec | pip install schemathesis |
| `dredd` | Spec-vs-implementation HTTP test runner | npm i -g dredd |
| `swagger-cli` | Validate, bundle, resolve $ref | npm i -g swagger-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight Studio | SaaS+OSS | partial | Visual editor; agents prefer CLI but humans benefit from review UI. |
| SwaggerHub | SaaS | yes (API) | Spec hosting + governance + codegen. Has org-level style guides. |
| Redocly | SaaS+OSS | yes (CLI/CI) | Best-in-class docs renderer + lint. |
| Postman | SaaS | yes (API) | Imports OpenAPI, generates collections + monitors. |
| Bump.sh | SaaS | yes (CLI) | Versioned spec hosting + diff alerts to Slack. |
| Apicurio Registry | OSS | yes | Self-hosted spec registry with semver. |
| Mockoon | OSS | yes | Local mock server from OpenAPI. |
| Zuplo | SaaS | yes | API gateway built directly from OpenAPI. |

## Templates & scripts
See `templates.md` for the OpenAPI scaffold and CI workflow. Inline drift detector:

```bash
#!/usr/bin/env bash
# scripts/check-spec-drift.sh — fail CI if generated code diverges from server/
set -euo pipefail

SPEC=openapi.yaml
GENERATED_DIR=$(mktemp -d)

redocly lint "$SPEC" || { echo "spec lint failed"; exit 1; }

openapi-generator-cli generate \
  -i "$SPEC" -g python-fastapi -o "$GENERATED_DIR" \
  --additional-properties=packageName=app

# Compare only generated models + interfaces, never business code.
DIFF=$(diff -r --brief \
  "$GENERATED_DIR/app/models" server/app/models 2>&1 || true)

if [[ -n "$DIFF" ]]; then
  echo "Spec ↔ implementation drift detected:"
  echo "$DIFF"
  echo "Run: cp -r $GENERATED_DIR/app/models server/app/models"
  exit 1
fi

# Breaking change check vs main
git fetch origin main:main 2>/dev/null || true
git show main:"$SPEC" > /tmp/spec-main.yaml 2>/dev/null && \
  oasdiff breaking /tmp/spec-main.yaml "$SPEC" --fail-on ERR

echo "spec drift check OK"
```

## Best practices
- Treat the spec as code: PR review, semver, branch protection, codeowners.
- Split spec by domain (`paths/users.yaml`, `paths/billing.yaml`) and bundle in CI — avoids merge hell.
- Run `oasdiff` on every PR; block merge on breaking changes unless `BREAKING-CHANGE:` is in commit body.
- Use `operationId` everywhere — generators rely on it for method names; absence breaks regen.
- Keep `examples` realistic and synced with seed data; `prism` will use them for mocking.
- Generate consumer SDK + publish to npm/PyPI on every release — consumers `npm update`, get type safety.
- Pin codegen version; updates change generated output and cause spurious diffs.
- Add `x-internal: true` extension on routes that should not appear in public docs; redocly filters them.

## AI-agent gotchas
- Agents asked to "add an endpoint" often modify server code first then back-fill spec — invert the flow with a hard rule in the agent prompt: "spec changes only; refuse to touch server/* until spec is committed".
- LLMs hallucinate JSON Schema keywords that don't exist (`format: phone-number`) — pin to OpenAPI 3.1 + JSON Schema 2020-12 vocab and run spectral on every output.
- Generators output code with framework versions baked in — agent regen with newer generator can subtly break (e.g., FastAPI Pydantic v1→v2). Pin generator + framework versions in `pyproject.toml` / `package.json`.
- Agents copy-paste schemas instead of using `$ref`, drifting two definitions of `User`. Add a spectral rule `no-duplicate-schemas`.
- Long specs blow context; agents truncate then "fix" missing fields. Solution: split into multi-file spec, agent only loads the file it modifies, bundles in CI.
- Human-in-loop checkpoint: every spec PR needs a human approve — automated merge of spec changes is a recipe for silent breaking changes downstream.

## References
- OpenAPI 3.1 spec — https://spec.openapis.org/oas/v3.1.0
- Redocly spec governance — https://redocly.com/docs/cli/guides/api-governance/
- Spectral rulesets — https://meta.stoplight.io/docs/spectral
- oasdiff breaking-change rules — https://github.com/Tufin/oasdiff
- "API design first" (Postman) — https://www.postman.com/api-platform/api-design/
- Schemathesis docs — https://schemathesis.readthedocs.io/
