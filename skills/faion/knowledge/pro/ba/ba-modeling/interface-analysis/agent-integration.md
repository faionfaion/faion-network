# Agent Integration — Interface Analysis

## When to use
- A new feature in the SDD `design.md` introduces system-to-system data flow (REST/GraphQL/file/queue) and the spec lacks payload schemas, error codes, auth, or SLA fields.
- Onboarding a third-party SaaS (Stripe, SendGrid, Twilio) and the agent must produce an interface catalog before writing client code.
- Migrating between providers (e.g., REST → gRPC, S3 → R2) where direction, format, and protocol diff must be documented.
- Decomposing a monolith into services: each split point becomes an interface that needs a contract before the team commits to the cut.
- Drafting acceptance criteria for `test-plan.md` tasks that test integration boundaries (contract tests, mocks, error scenarios).

## When NOT to use
- Pure-internal refactor where caller and callee live in the same process and module boundary; ADR is enough, no IF-XXX catalog.
- Throwaway scripts and one-off data migrations — write the script, log fields, move on.
- Greenfield prototype before product-market fit — defer formal interface specs until the contract starts changing under multiple consumers.
- UI-only changes that do not alter the data envelope (CSS, copy, layout). Use `ux-ui-designer` knowledge instead.

## Where it fails / limitations
- Static spec drift: hand-written Markdown specs decay the moment code ships unless generated from OpenAPI/Protobuf source of truth.
- Volume/SLA fields are guessed pre-launch; real numbers only arrive post-load test, so the doc lies for months.
- Async/event flows (Kafka, NATS, webhooks) do not map cleanly to the request/response template — direction is "fan-out", retries are consumer-side, and ordering is a property of the topic, not the message.
- Cross-team interfaces fail at the human boundary: spec is correct, but the other team owns auth rotation and breaks it on Friday.
- LLM-generated specs hallucinate plausible-looking error codes (e.g., 422 where the API returns 400) — every code must be verified against live response.

## Agentic workflow
Drive interface analysis as a three-pass loop with subagents. Pass 1: a research subagent crawls the upstream system's docs (OpenAPI, vendor PDF, sample responses) and emits the raw interface catalog. Pass 2: an SDD/BA subagent fills the spec template, links each field to a requirement ID, and produces contract-test scaffolding. Pass 3: a reviewer subagent diffs the spec against actual HTTP captures (curl/httpie/Postman export) and flags drift. The orchestrator commits the catalog into `.product/<feature>/interfaces/` and references it from `design.md`.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the BA/spec authoring task with quality gates; ensures `interface-spec.md` exists before `design.md` is marked done.
- `faion-brainstorm` (diverge/converge) — for "what could go wrong on this interface" failure-mode generation when no live system exists yet.
- `faion-improver` — periodic audit pass: re-fetch live OpenAPI, diff against committed catalog, open SDD task on drift.
- A custom `interface-analyst` Task agent (spawn ad-hoc with `Task` tool) — reads vendor docs + sample payloads, returns filled spec template only.

### Prompt pattern
```
You are an interface analyst. Source: <OpenAPI URL or pasted spec>.
For each operation produce one block matching the IF-XXX template at
skills/faion/knowledge/pro/ba/ba-modeling/interface-analysis/templates.md
Verify every error code against the source — do not invent codes.
Output: Markdown only, no prose around it.
```

```
You are reviewing interface IF-042. Compare the committed spec against
this live curl capture: <paste>. Return a unified diff of fields,
required flags, and error codes that disagree. If they agree, return "OK".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openapi-cli` (Redocly) | Lint / bundle / diff OpenAPI 3.x | `npm i -g @redocly/cli` |
| `oasdiff` | Breaking-change detector for OpenAPI | `go install github.com/oasdiff/oasdiff@latest` |
| `schemathesis` | Property-based contract testing from OpenAPI | `pip install schemathesis` |
| `httpie` / `curl` | Capture live responses to validate spec fields | distro pkg |
| `mitmproxy` | Record real traffic, export to HAR for spec backfill | `pip install mitmproxy` |
| `grpcurl` | Probe gRPC services without writing client | `brew install grpcurl` |
| `jq` / `gron` | Flatten JSON to grep field names for spec rows | distro pkg |
| `prism` (Stoplight) | Mock server from OpenAPI for downstream dev | `npm i -g @stoplight/prism-cli` |
| `pact-broker` CLI | Publish/verify consumer-driven contracts | `gem install pact_broker-client` |
| `buf` | Protobuf lint, breaking-change check, generate | `brew install bufbuild/buf/buf` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stoplight | SaaS | Yes (REST + Git) | Hosts OpenAPI, generates docs/mocks; agent edits via Git. |
| Postman / Bruno | SaaS / OSS | Partial (Postman API) | Bruno is plain-text Git-friendly, agent-preferred. |
| Pact (pactflow.io) | SaaS+OSS | Yes (CLI + REST) | Consumer-driven contracts, breaks build on drift. |
| Apicurio Registry | OSS | Yes (REST) | Schema registry for Avro/Protobuf/JSON-Schema, versioned. |
| AsyncAPI Studio | OSS | Yes (file-based) | Spec format for Kafka/AMQP/MQTT — async equivalent of OpenAPI. |
| Speakeasy | SaaS | Yes (CLI) | Generates idiomatic SDKs from OpenAPI; agent runs in CI. |
| Mockoon | OSS desktop+CLI | Yes (CLI) | Local mocks from OpenAPI; agent boots before integration test. |
| Hoppscotch | OSS | Partial | REST/GraphQL/WS workbench; collections exportable to JSON. |
| Insomnia | SaaS+OSS | Partial | Same niche as Postman; less Git-friendly than Bruno. |
| Confluent Schema Registry | SaaS+OSS | Yes (REST) | For Kafka topics; enforces compatibility on publish. |

## Templates & scripts

`templates.md` already covers the per-interface spec and the catalog. Below: a small drift-detector script the agent runs in CI to keep committed specs in sync with a live OpenAPI URL.

```bash
#!/usr/bin/env bash
# interface-drift-check.sh — flag breaking changes between committed spec and live API.
# Usage: ./interface-drift-check.sh <committed-openapi.yaml> <live-openapi-url>
set -euo pipefail
COMMITTED="${1:?committed spec path required}"
LIVE_URL="${2:?live OpenAPI URL required}"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT

curl -fsSL "$LIVE_URL" -o "$WORK/live.yaml"

# Lint both sides
npx --yes @redocly/cli lint "$COMMITTED" >/dev/null
npx --yes @redocly/cli lint "$WORK/live.yaml" >/dev/null

# Breaking-change diff (exits non-zero on breaking change)
oasdiff breaking "$COMMITTED" "$WORK/live.yaml" --fail-on ERR > "$WORK/diff.txt" || {
  echo "BREAKING CHANGE detected:"; cat "$WORK/diff.txt"; exit 2;
}

# Non-breaking changelog (informational)
oasdiff changelog "$COMMITTED" "$WORK/live.yaml" > "$WORK/changes.md" || true
echo "Spec in sync. Non-breaking changes:"; cat "$WORK/changes.md"
```

Wire into pre-commit or a nightly GitHub Action. Agent reads the diff output and opens an SDD task under `todo/` when drift appears.

## Best practices
- Treat OpenAPI/AsyncAPI/Protobuf as the source of truth; the IF-XXX Markdown is generated or synced, not hand-typed.
- Assign every interface a stable ID (`IF-001`) and reference it from `requirements.md`, `design.md`, and `test-plan.md` — traceability matrix collapses without it.
- Capture at least one real payload per direction with `mitmproxy` or `curl -v` and paste it into the spec; example beats prose for downstream consumers.
- For each error code, document what the consumer must do (retry, surface to user, alert) — codes without behaviour are decoration.
- Version the interface, not the system: `/v1/customers` survives independently of the service's semver.
- Define idempotency keys and dedup window for any non-GET; specify whether retries are safe.
- Capture timeout + retry budget on both sides; mismatched budgets are a top-3 production failure pattern.
- For async interfaces, write down ordering guarantees (per-key, none, total) and consumer-group semantics.
- Keep payload examples literal — no `<placeholder>` tokens. Tools and agents copy-paste them into tests.

## AI-agent gotchas
- Agents hallucinate field types when the source is ambiguous; force a "field types must come from sample payload or OpenAPI, otherwise mark as `unknown`" rule in the prompt.
- Error code tables get auto-completed with the standard HTTP set even when the API only returns three of them. Validate against captured traffic.
- Direction labels flip easily ("we provide" vs "we consume"). Anchor the prompt to a fixed perspective (always our system as subject).
- Async semantics confuse single-shot prompts — split event-driven interfaces into a separate AsyncAPI pass, do not reuse the REST template.
- Auth fields (OAuth scopes, API key locations) are routinely wrong; require the agent to cite the line in vendor docs that defines them.
- Volume/SLA numbers must be marked `tbd` until load test data exists; agents will otherwise emit confident fictions.
- Human-in-the-loop checkpoints: (1) sign-off of new IF-XXX before client code starts, (2) review of any breaking-change diff before deploy, (3) manual confirmation of auth/secret rotation steps.
- When generating contract tests from a spec, run them against both the live system and the mock; a green mock + red live = spec drift, not test bug.

## References
- BABOK v3 §10.21 Interface Analysis (IIBA).
- OpenAPI Specification 3.1 — https://spec.openapis.org/oas/latest.html
- AsyncAPI 3.0 — https://www.asyncapi.com/docs/reference/specification/v3.0.0
- Pact consumer-driven contracts — https://docs.pact.io/
- oasdiff breaking-change rules — https://github.com/oasdiff/oasdiff
- "Building Microservices" 2nd ed., Sam Newman — Ch. 4 (Contracts), Ch. 5 (Integration).
- Postel's law and its discontents — https://datatracker.ietf.org/doc/html/rfc760#section-3
