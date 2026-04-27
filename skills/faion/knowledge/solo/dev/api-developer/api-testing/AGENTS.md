# API Testing

## Summary

Structured methodology for verifying HTTP/gRPC/GraphQL API correctness using a layered pyramid: unit tests (many), integration tests (some), contract tests (consumer-driven, for cross-team interfaces), and E2E tests (few). Every endpoint must have at least one negative test (missing auth, wrong role, malformed body, rate limit).

## Why

APIs break across teams when consumer and provider deploy independently. Contract tests catch schema drift before production. Spec-conformance validation (openapi-core, Schemathesis) closes the gap between what the spec says and what the code does. Without negative cases, auth bypasses and validation gaps ship undetected.

## When To Use

- Any HTTP/gRPC/GraphQL service heading toward production
- Cross-team interfaces where consumer and provider deploy independently (contract tests with Pact)
- API published with an OpenAPI/GraphQL/Protobuf spec — automatic spec-conformance tests close the spec/code gap
- Refactor or version bump — regression suite is the safety net
- Public SaaS API with SLA covering correctness, rate limits, idempotency, and error shape

## When NOT To Use

- Throwaway prototype — smoke test with curl and ship
- When test maintenance cost exceeds the bug risk (low-traffic admin endpoints with no consumers)
- Replacing static type checks — let TypeScript/mypy/Pydantic catch what they can
- 100%-coverage cargo cult — coverage is a leading indicator, not a goal

## Content

| File | What's inside |
|------|---------------|
| `content/01-pyramid-and-rules.xml` | Test pyramid, negative case requirements, spec-conformance rules |
| `content/02-examples.xml` | Pact contract test, FastAPI integration test, OpenAPI validation example |
| `content/03-tools-and-gotchas.xml` | CLI tools, services, AI-agent gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/pytest-integration.py` | pytest fixtures for auth, db, and factory-based test data |
| `templates/schemathesis-gate.sh` | Schemathesis fuzz CI gate against a running OpenAPI app |
| `templates/pact-consumer.js` | Pact consumer-side interaction definition |
| `templates/prompt-generate-tests.txt` | Agent prompt: generate per-endpoint test cases from OpenAPI spec |
