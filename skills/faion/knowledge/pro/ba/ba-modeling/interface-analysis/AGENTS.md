# Interface Analysis

## Summary

Identifies, documents, and validates all connection points between a solution and external systems, users, hardware, or communication channels. Each interface gets a stable ID (IF-XXX) referenced from requirements.md, design.md, and test-plan.md. Specs are generated from or synced to OpenAPI / AsyncAPI / Protobuf — never hand-typed as the primary source of truth. Breaking changes detected via `oasdiff` in CI.

## Why

Integration failures and late surprises happen when interface requirements are discovered during development rather than before design. A stable IF-XXX catalog with mandatory error-handling and auth fields prevents the most common integration failures: mismatched timeouts, undefined retry semantics, hallucinated error codes, and auth-rotation blind spots. Consumer-driven contract tests (Pact) close the loop between spec and live system.

## When To Use

- A new feature in SDD `design.md` introduces system-to-system data flow and the spec lacks payload schemas, error codes, auth, or SLA fields.
- Onboarding a third-party SaaS (Stripe, SendGrid, Twilio) before writing client code.
- Migrating between providers where direction, format, and protocol diff must be documented.
- Decomposing a monolith into services: each split point needs a contract before the team commits.
- Drafting acceptance criteria for `test-plan.md` tasks that test integration boundaries (contract tests, mocks, error scenarios).

## When NOT To Use

- Pure-internal refactor where caller and callee live in the same process and module boundary — an ADR is enough.
- Throwaway scripts and one-off data migrations.
- Greenfield prototype before product-market fit — defer formal specs until the contract starts changing under multiple consumers.
- UI-only changes that do not alter the data envelope.

## Content

| File | What's inside |
|------|---------------|
| `content/01-interface-types.xml` | Four interface types (user / system / hardware / communication), attribute set per interface, data-element specification rules. |
| `content/02-agentic-workflow.xml` | Three-pass loop: research subagent (crawl docs) → BA/spec subagent (fill template, link to requirements) → reviewer subagent (diff against live captures). Prompt patterns. |
| `content/03-antipatterns.xml` | Static spec drift, volume/SLA guessing, async-flow mismatch, hallucinated error codes, cross-team auth-rotation blindspot. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interface-spec.md` | Per-interface specification: IF-XXX, type, direction, data fields, technical spec, operational spec, error handling, security. |
| `templates/interface-catalog.md` | Summary table of all interfaces with IF-IDs, types, directions, and external systems. |
| `templates/interface-drift-check.sh` | CI script: lints committed OpenAPI spec and live API URL with oasdiff; exits non-zero on breaking changes. |
| `templates/prompt-interface-analyst.txt` | LLM prompt for filling the IF-XXX spec from OpenAPI or vendor docs; error-code verification rule. |
