# Agent Integration — OpenAPI Specification

## When to use
- Designing a new HTTP/JSON API and you want a single source of truth for clients, servers, mocks, tests, and docs.
- Generating typed clients (TS, Python, Go, Rust) from one spec instead of hand-writing N SDKs.
- Contract-first work between FE and BE where one is human and the other is agent-built.
- Documenting an existing API (reverse-engineer with `swagger-ui-watcher`/`har-to-openapi`) before refactor.
- Public API surface where Stripe/GitHub-style docs and SDK generation are expected.

## When NOT to use
- Pure internal RPCs between trusted services — use Protobuf / gRPC / tRPC; OpenAPI adds ceremony for no win.
- GraphQL APIs — schema is the contract, OpenAPI is irrelevant.
- Event-driven / pub-sub — use AsyncAPI instead.
- Tiny one-endpoint webhook receivers — overhead > value.
- Server-driven UI / RSC payloads — JSON-RPC over a stream, not REST.

## Where it fails / limitations
- OpenAPI 3.1 ≠ JSON Schema 2020-12 in every tool — generators (Java, Python `openapi-generator`) lag the spec by months.
- `oneOf` / `anyOf` / discriminator unions are inconsistently supported across code generators; Rust + Go generators are weakest.
- File upload (`multipart/form-data`) descriptions are awkward; many generators botch streaming uploads.
- Hand-edited specs drift from implementation in days. Generated specs (FastAPI, NestJS, drf-spectacular) drift less but expose internal types.
- Spec-first workflows fail when the spec is huge (>5k lines): linters become slow, diffs are unreadable, agents lose track of `$ref` graphs.
- Polymorphic responses (e.g., `error` shape varies by endpoint) blow up generated client unions.

## Where it fails / limitations (security)
- Generators emit clients that silently drop unknown fields → forward-compat issues.
- `securitySchemes` only describes auth, doesn't enforce it. Agents often forget `security: []` on public endpoints.

## Agentic workflow
Treat the spec as **the** artifact. A planner subagent drafts paths + schemas from a feature spec. A linter subagent runs Spectral and Redocly to enforce style. A generator subagent regenerates client SDKs and server stubs and commits them as a separate diff. A diff-reviewer subagent compares the new spec to `main` and emits a breaking-change report (paths removed, required fields added, enums shrunk).

### Recommended subagents
- `faion-sdd-executor-agent` — own spec → review → generate → tests loop.
- A user-defined `openapi-linter` (model: haiku) — run Spectral/Redocly, return only violations.
- A user-defined `breaking-change-detector` (model: sonnet) — diff specs, classify changes (additive / breaking / cosmetic).
- `password-scrubber-agent` — sweep generated SDK fixtures for leaked tokens.

### Prompt pattern
- "Read `openapi-specification/README.md` and the feature spec at `<path>`. Emit additions to `openapi.yaml` only — paths, schemas under `components.schemas`, parameters under `components.parameters`. Use `$ref` for every reuse. Add `operationId`, `tags`, examples, and 4xx/5xx via `components.responses`. Output unified diff against current `openapi.yaml`."
- "Compare `openapi.yaml@HEAD` to `openapi.yaml@main`. Classify each change as additive, breaking, or cosmetic. Output a markdown table; flag breaking changes with `BREAK`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@redocly/cli` | Lint, bundle, split, preview | `npm i -g @redocly/cli` — https://redocly.com/docs/cli |
| `@stoplight/spectral-cli` | Style + correctness linter, custom rulesets | `npm i -g @stoplight/spectral-cli` |
| `openapi-generator-cli` | Generate clients/servers in 50+ langs | `npm i -g @openapitools/openapi-generator-cli` |
| `openapi-typescript` | TS types only, no runtime client | `npm i -D openapi-typescript` |
| `openapi-fetch` | Tiny typed `fetch` wrapper paired with `openapi-typescript` | `npm i openapi-fetch` |
| `prism` | Mock server + contract validator from spec | `npm i -g @stoplight/prism-cli` |
| `swagger-cli` | Validate, bundle, dereference | `npm i -g @apidevtools/swagger-cli` |
| `oasdiff` | Detect breaking changes between two specs | https://github.com/Tufin/oasdiff |
| `vacuum` | Fast Go-based linter (alt to Spectral) | https://quobix.com/vacuum/ |
| `schemathesis` | Property-based contract tests from spec | `pip install schemathesis` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight | SaaS | Yes (CLI + API) | Visual editor, governance rulesets. |
| Redocly | SaaS + OSS CLI | Yes | Best dev portal generator; CLI is fully scriptable. |
| Bump.sh | SaaS | Yes | API doc hosting + breaking-change diff. |
| SwaggerHub | SaaS | Partial | Heavier, enterprise. |
| Prism (Stoplight) | OSS | Yes | Mock server agents can test against. |
| ReadMe.com | SaaS | Partial | Good docs hosting; CLI exists but limited. |
| Postman | SaaS | Partial | Imports OpenAPI; team-collab oriented, less scriptable. |

## Templates & scripts
See `templates.md`. Minimal pre-commit lint + breaking-change check the agent should add to CI:

```yaml
# .github/workflows/openapi.yml
name: openapi
on: [pull_request]
jobs:
  lint-and-diff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm i -g @redocly/cli @stoplight/spectral-cli
      - run: redocly lint openapi.yaml
      - run: spectral lint openapi.yaml --fail-severity=warn
      - name: Breaking-change diff
        run: |
          git show origin/main:openapi.yaml > /tmp/base.yaml
          docker run --rm -v "$PWD:/specs" -v /tmp:/tmp tufin/oasdiff \
            breaking /tmp/base.yaml /specs/openapi.yaml --fail-on ERR
```

## Best practices
- Keep one canonical `openapi.yaml` at repo root; bundle with `redocly bundle` for distribution.
- Always set `operationId` (kebab- or camelCase, unique) — generators key client method names off it.
- Put **every** error response under `components.responses`; reuse via `$ref`. Pick a single `Error` schema and stick to it.
- Use `examples` (plural) per response code with named scenarios; agents can lift these into integration tests.
- Pin `info.version` to semver and bump on every breaking change; gate `oasdiff breaking` in CI.
- Split large specs by tag using `redocly split` once `paths` exceeds ~30 endpoints.
- For server-generated specs (FastAPI, drf-spectacular, NestJS), commit a snapshot to git and CI-fail if it drifts.
- Add Spectral rules: require `description`, ban `additionalProperties: true` on response schemas, require `2xx` + at least one `4xx` per operation.
- Use `nullable: true` (3.0) or `type: ['string', 'null']` (3.1) consistently — generator output diverges otherwise.

## AI-agent gotchas
- LLMs duplicate schemas instead of `$ref`-ing existing ones — leads to subtle drift. Run a post-pass that detects structurally-equal schemas (`redocly stats` + custom check).
- Agents emit `type: object` without `required` array → generated TS becomes `Partial<T>` everywhere. Always require an explicit `required` list.
- LLMs love `oneOf` for union types but forget `discriminator.propertyName`; some generators silently produce `any`. Verify generated client output, not just the spec.
- Agents may invent custom `x-` extensions; they don't reach the generated client. Only use `x-*` if the generator documents support.
- When updating an existing spec, agents often re-indent the whole YAML, producing a giant diff. Pin to `prettier --parser yaml` or `yq` formatting before committing.
- Agents tend to lose `security` blocks on `POST /login` (which should be `[]`) vs other endpoints (which need `bearerAuth`). Add a Spectral rule that fails if `security` is missing.
- Human-in-loop checkpoint: a human must sign off any change that bumps the major version or removes a path; never let an agent merge a `BREAK` diff unattended.
- For FastAPI/drf-spectacular: instruct the agent to regenerate `openapi.yaml` (`fastapi run --export-openapi …` or `drf-spectacular --file …`) **after** code change, then commit both in the same PR.

## References
- OpenAPI 3.1 spec — https://spec.openapis.org/oas/v3.1.0
- Redocly CLI — https://redocly.com/docs/cli
- Spectral — https://stoplight.io/open-source/spectral
- openapi-generator — https://openapi-generator.tech
- oasdiff — https://github.com/Tufin/oasdiff
- openapi-typescript — https://openapi-ts.dev
- Schemathesis — https://schemathesis.readthedocs.io
- API style guide examples — https://github.com/zalando/restful-api-guidelines
