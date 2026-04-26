# Consumer Contract Tests Generated from OpenAPI / Traffic

## Summary

Pact consumer contracts have one classic weakness: the consumer team has to *write* them. When that author is an LLM hand-rolling Pact JSON, the contract drifts from the actual provider spec and `can-i-deploy` becomes noise. The fix is to point an MCP server or skill at the canonical artifact — OpenAPI spec, recorded HTTP traffic, or typed client code — and have it *generate* the consumer Pact file plus matching client test. The generated contract is then committed as the source of truth and never edited by hand. PactFlow reports up to 60% reduction in test creation time and the AI-generated contracts are deterministic enough to gate provider deploys with `can-i-deploy`.

## Why

A Pact contract is a *machine-readable* statement of "consumer X expects provider Y to behave like this". When the consumer is a microservice with an OpenAPI spec, the spec already encodes what the consumer will accept; an LLM that infers the Pact from the spec produces a far more accurate contract than one written from a feature ticket. PactFlow's MCP server (2025) and the Pact AI skill bundle this pipeline. The deterministic part — sample request/response from spec — is solved; the LLM only adds matchers and edge cases. Treating the generated artifact as canonical also stops hand-edited Pacts from masking real provider regressions.

## When To Use

- Microservices with more than two consumers per provider, where mock drift is a recurring incident driver.
- Polyglot stacks where each consumer uses a different mock library and contracts diverge silently.
- Consumer services authored or maintained by a coding agent that has access to the provider's OpenAPI/AsyncAPI spec.
- Third-party API integrations where you control only the consumer side and need a reproducible mock.

## When NOT To Use

- Single-consumer monolith calling a provider it owns — no contract gap to close, just integration tests.
- GraphQL providers with strong codegen — schema-diff plus typed client gives the same guarantee cheaper.
- One-off internal cron-callers or scripts — the Pact broker overhead exceeds the benefit.
- Providers without any spec artifact (no OpenAPI, no recorded traffic) — generate the spec first, then the Pact.

## Content

| File | What's inside |
|------|---------------|
| `content/01-generate-from-spec.xml` | Generate Pact from OpenAPI/traffic, never hand-write; commit generator command. |
| `content/02-canigo-deploy-gate.xml` | Wire `can-i-deploy` into provider CI as the cross-service gate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pactflow-mcp-prompt.txt` | MCP/skill prompt that drives PactFlow generation from an OpenAPI spec. |
| `templates/canigo-deploy.yml` | GitHub Actions step wiring `can-i-deploy` as a required check on the provider repo. |
