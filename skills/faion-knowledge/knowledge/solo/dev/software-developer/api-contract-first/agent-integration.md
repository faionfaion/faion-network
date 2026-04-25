# Agent Integration — Contract-First API Development

## When to use
- New service with multiple consumers (mobile, web, partners) where stub generation lets clients start in parallel with the server.
- Cross-team or cross-repo APIs where the spec is the negotiated contract and code is downstream.
- Public APIs where backward-compatibility guarantees demand a single source of truth and breaking-change detection.
- Polyglot stacks where a single OpenAPI / AsyncAPI / Protobuf definition feeds 3+ language SDKs.
- LLM-driven implementation: agents are most reliable when given a closed schema; contract-first reduces hallucination surface.

## When NOT to use
- Solo prototypes / MVP exploration where the schema flips weekly — generation overhead exceeds value.
- Internal RPC inside one repo with one team — code-first frameworks (FastAPI, NestJS w/ decorators) keep velocity higher.
- APIs with heavy dynamic shapes (admin / metaprogramming endpoints) where schema can't capture the surface.
- Specs that would be larger than the implementation — usually a sign you're over-engineering for a future you don't have.

## Where it fails / limitations
- Spec drift: developers patch the controller and forget the spec; without CI enforcement the spec rots quickly.
- Generated code ergonomics: openapi-generator output is often verbose, idiomatic-poor, and locked to template choices.
- Generator bugs: certain Python / TypeScript generators emit broken code for `oneOf`, recursive schemas, or `additionalProperties` — silently.
- Breaking-change detection is brittle: same JSON schema can be expressed two ways and `oasdiff` reports false breaks.
- Conditional / polymorphic responses (`oneOf`, `anyOf`, discriminator) are hard for generators and harder for SDK consumers.
- AsyncAPI tooling lags OpenAPI by 2–3 years; stub generation is shaky for event-driven contracts.
- Spec authoring tools (Stoplight Studio, Swagger Editor) make easy contracts easy and hard contracts harder; agents often produce spec that is technically valid but semantically poor.
- Mock servers diverge from real backend semantics (auth, idempotency, rate limits) — clients pass mock tests and break in staging.

## Agentic workflow
A four-stage pipeline. (1) **Design**: a domain-modeling agent produces an OpenAPI 3.1 spec from PRD + REST style guide; a critic agent runs Spectral and the `api-rest-design` rules. (2) **Approve**: human-in-the-loop merge gate; `oasdiff breaking` blocks regressions. (3) **Generate**: CI pipeline emits server stubs (FastAPI / NestJS / go-chi), client SDKs (TS, Py, Go), and contract test scaffolds via `openapi-generator` or `orval`/`oazapfts`. (4) **Implement**: an SDD-driven coding agent fills business logic in the generated stub, never editing the generated models — contract tests enforce the spec. Repeat: any spec change re-runs (3) and any new endpoint re-runs (1)–(4).

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — gates: spec compiles, Spectral clean, `oasdiff` non-breaking (or major-bumped), generated code committed in same PR.
- A **spec-critic** subagent (worth creating): runs Spectral + custom rules from `api-rest-design` and `api-versioning`; outputs PASS/FAIL with rule IDs.
- `faion-feature-executor` (skill) — sequences the four stages as ordered tasks; pauses at the human-approve gate.
- A **stub-impl** subagent: instructed to fill `NotImplementedError` in the generated server with business logic, forbidden from touching the model files.
- `password-scrubber-agent` — scrub examples in spec before publishing.

### Prompt pattern
Spec drafting:
```
You are an API designer. Produce an OpenAPI 3.1 YAML for the use cases
in <prd>. Follow Zalando RESTful guidelines and the rules in
api-rest-design/README.md. Use Problem+JSON for errors. Tag every
operation. Include 2 examples per request and per 2xx response. Output
only the YAML; no commentary.
```

Stub-fill (post-generation):
```
You are filling generated server stubs. Files under server/models/**
are GENERATED — DO NOT EDIT. Implement only methods raising
NotImplementedError in server/apis/**. Use the repository in
server/repositories/<resource>.py. After each method, run pytest -k
contract_<operationId>; the test must pass.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openapi-generator` | Generate stubs/clients in 50+ targets | https://openapi-generator.tech/ |
| `oapi-codegen` | Go server + client from OpenAPI | `go install github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@latest` |
| `orval` | TS clients (axios, fetch, react-query, zod) from OpenAPI | `npm i -D orval` ; https://orval.dev |
| `oazapfts` | Minimal TS fetch client | `npm i -D oazapfts` |
| `datamodel-code-generator` | OpenAPI → Pydantic / dataclasses | `pip install datamodel-code-generator` |
| `spectral` | Spec linter (custom rulesets) | `npm i -g @stoplight/spectral-cli` |
| `oasdiff` | Breaking change detector | https://github.com/Tufin/oasdiff |
| `prism` | Mock server + contract validation proxy | `npm i -g @stoplight/prism-cli` |
| `dredd` | Spec-vs-implementation contract test runner | `npm i -g dredd` |
| `schemathesis` | Property-based testing from OpenAPI | `pip install schemathesis` |
| `buf` | Protobuf-equivalent of the above for gRPC | https://buf.build |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight | SaaS + desktop | Yes — Spectral CLI | Visual designer + governance. |
| SwaggerHub | SaaS | Yes — REST API | Hosted spec governance + style guides. |
| Bump.sh | SaaS | Yes — CLI | Versioned hosting + breaking-change diff. |
| Apicurio Registry | OSS | Yes | Self-hosted spec/schema registry. |
| Postman | SaaS | Yes — API + Newman CLI | Spec import + contract tests in CI. |
| Speakeasy | SaaS | Yes — CLI | Polished SDK generation across languages. |
| Fern | SaaS + OSS CLI | Yes | Spec-first SDK + docs generator. |
| Buf Schema Registry | SaaS | Yes — `buf` CLI | gRPC-equivalent of SwaggerHub. |
| Konnect (Kong) | SaaS | Yes — API | Spec-first deploy to gateway. |

## Templates & scripts
See `templates.md` and `examples.md` for spec + generator config. Inline CI gate (≤50 lines):

```bash
#!/usr/bin/env bash
# contract-gate.sh — block PR if spec/code drift or breaking change.
set -euo pipefail
spec="${1:-openapi.yaml}"
base_spec="$(git show origin/main:$spec 2>/dev/null || true)"

# 1. Lint.
npx --yes @stoplight/spectral-cli lint "$spec" --fail-severity=warn

# 2. Breaking-change check vs main.
if [[ -n "$base_spec" ]]; then
  echo "$base_spec" > /tmp/base.yaml
  oasdiff breaking /tmp/base.yaml "$spec" -f text | tee /tmp/break.txt
  if [[ -s /tmp/break.txt ]]; then
    grep -q "MAJOR" "$spec" || { echo "Breaking changes without MAJOR bump"; exit 1; }
  fi
fi

# 3. Re-generate models, fail if diff.
mkdir -p /tmp/gen
openapi-generator generate -i "$spec" -g python-pydantic-v1 -o /tmp/gen --skip-validate-spec
diff -ru server/models /tmp/gen/openapi_client/models || {
  echo "Generated models out of sync — run make generate"
  exit 1
}

# 4. Run contract tests against the live server (started elsewhere).
schemathesis run "$spec" --base-url "${BASE_URL:?}" --hypothesis-deadline=2000
```

Wire this into GitHub Actions on every PR touching the spec or `server/`.

## Best practices
- The spec is the source of truth. Hand-edits to generated files fail CI.
- Lint with a strict Spectral ruleset (operation IDs, descriptions, examples, tags) — agents will skip these otherwise.
- Run `oasdiff breaking` on every PR; require a MAJOR bump on any breaking change.
- Keep the spec under `api/openapi.yaml` (or split with `$ref`) and version-control it next to the code; PRs that change behavior must change the spec.
- Generate at build time, not at commit time — committed generated code is fine, but it must match the spec exactly (CI re-generates and diffs).
- Provide examples (≥1 per operation, both request and response) — they double as fixture data and improve LLM SDK output.
- Run `schemathesis` or `dredd` in CI: property-based tests catch generators bugs and implementation drift.
- For events / async, use AsyncAPI 3.0 with `@asyncapi/cli`; treat the same way as OpenAPI.
- For gRPC, use `buf` and the same workflow: spec → generate → impl → contract test.

## AI-agent gotchas
- Agents edit generated files when "fixing tests". Mark generated dirs with `// CODEGEN — DO NOT EDIT` headers and add a pre-commit hook that fails on changes inside them.
- LLMs invent OpenAPI fields that don't exist (`x-magic-flag`) or use deprecated 2.0 syntax. Pin the prompt to OAS 3.1 and validate with the official JSON Schema.
- Polymorphic schemas (`oneOf` / `discriminator`) trip both generators and agents — keep schemas flat where possible and document the discriminator value.
- Agents skip examples to save tokens. Force `examples` blocks on every request and 2xx response via Spectral `oas3-valid-media-example` plus a custom "min-1-example" rule.
- Agents conflate "spec" and "docs" — they'll add narrative prose into `description` fields. Keep `description` short; reference external docs via `externalDocs`.
- Breaking-change blindness: agents widen response shapes (add a `null` to a non-nullable field) without bumping major. `oasdiff` catches this; the agent prompt must be told to read its output.
- Mock-server overconfidence: agents wire frontend to Prism mock and declare "done"; mock semantics differ from real (auth, rate limits). Require contract tests against the real server before completing an SDD task.
- Human-in-loop checkpoints: any spec PR labeled `breaking` must be human-approved; any new resource must pass design review before code generation runs.
- Generator pinning: agents may bump generator versions silently; pin the version in `package.json` / `Makefile` and treat upgrades as their own PR.

## References
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/latest.html
- AsyncAPI 3.0 — https://www.asyncapi.com/docs/reference/specification/v3.0.0
- "Designing Web APIs" — Brenda Jin et al. (O'Reilly).
- API Stylebook — http://apistylebook.com/design/guidelines/
- Spectral rulesets — https://meta.stoplight.io/docs/spectral
- oasdiff (breaking change detection) — https://github.com/Tufin/oasdiff
- Schemathesis — https://schemathesis.readthedocs.io
- Buf (gRPC equivalent) — https://buf.build
- Sibling methodologies in this repo: `api-rest-design/`, `api-openapi-spec/`, `api-versioning/`, `api-documentation/`, `contract-first-development/`.
