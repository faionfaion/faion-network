# API-First Development

## Summary

Design the OpenAPI 3.1 contract before writing any implementation code. The spec is the
single source of truth: generate server stubs, client SDKs, mock servers, and contract
tests from it. Every endpoint, schema, and error format is decided in YAML before a line
of backend code exists.

## Why

APIs designed after implementation are inconsistent across services, break consumers on
change, and block frontend teams until the backend ships. Writing the spec first forces
the team to agree on the contract, enables parallel frontend development via mock servers
(Prism), and lets Spectral linting catch naming/versioning violations before any code
drifts from the design.

## When To Use

- Multiple consumers planned (frontend, mobile, third-party) before backend is written
- Frontend and backend agents/teams work in parallel — mock server unblocks frontend
- Public or partner-facing API where contract stability is a hard requirement
- Microservice boundaries require agreed contracts before implementation begins
- SDK generation is needed (client libraries from spec)
- API governance required — linting rules enforce naming, versioning, error format

## When NOT To Use

- Internal single-consumer service where spec would be written after implementation anyway (YAGNI)
- Rapid prototype with fewer than 3 endpoints — design overhead exceeds benefit
- GraphQL-first projects: OpenAPI is REST-specific; use AsyncAPI for event-driven
- No CI pipeline to enforce spec compliance — spec drift will occur within weeks

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | API-first workflow, core principles, OpenAPI 3.1 key features, toolchain |
| `content/02-checklist.xml` | Phase-by-phase checklist: spec design → validation → mock → code gen → contract tests |
| `content/03-gotchas.xml` | Antipatterns and AI-agent-specific failure modes |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-3.1-skeleton.yaml` | Minimal complete OpenAPI 3.1 spec with auth, pagination, error schemas |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/api-first-check.sh` | Lint spec with Spectral, then start Prism mock server |
