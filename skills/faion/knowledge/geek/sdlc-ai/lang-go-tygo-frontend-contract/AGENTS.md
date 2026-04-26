# Go → TypeScript DTO Contract via tygo

## Summary

In any Go-backend / TypeScript-frontend repo, treat the Go DTO struct definitions as the single source of truth and generate the TypeScript counterpart with `tygo generate` from a checked-in `tygo.yaml`. The frontend never hand-writes API types; it imports the generated `.d.ts`/`.ts` file. CI runs `tygo generate` and fails the build with `git diff --exit-code` if the committed output diverges from the regenerated output.

## Why

Cross-language contract drift is the most common origin of LLM hallucinations on full-stack PRs: the agent invents a frontend field that exists in the backend's mental model, or vice versa, and tests pass because both sides agreed on the wrong shape. tygo runs over Go AST + struct tags, so the TS types are mechanically derived rather than transcribed. CI's `git diff --exit-code` gate makes "I forgot to regenerate" a deterministic failure. This puts the agent in a position where it can read one Go file and trust the generated TS shape — the contract is enforced by the toolchain, not by review discipline.

## When To Use

- Go backend + TypeScript frontend in the same repo or coupled repos.
- Internal RPC endpoints where OpenAPI is overkill but type safety still matters.
- Monorepos where backend struct edits should propagate to frontend types in one PR.
- Any team that has shipped a "frontend used wrong field name" production incident.

## When NOT To Use

- OpenAPI-first projects — the spec, not Go, is the source of truth; use `oapi-codegen` for Go and `openapi-typescript` for TS instead.
- gRPC services — protobuf already gives you typed bindings on both sides.
- Polyglot backends (Go + Python + Java) where a single language can't be the source — adopt OpenAPI or protobuf.
- Throwaway prototypes — drift cost is below the tooling overhead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tygo-rule.xml` | The `tygo generate` rule, struct-tag convention, CI diff gate. |
| `content/02-type-mappings.xml` | `time.Time`, `uuid.UUID`, custom enums — how to map without losing type safety. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tygo.yaml` | Minimal config mapping a `dto` package to a TS file with the standard mappings. |
| `templates/ci-check.sh` | One-liner CI check: regenerate, fail on diff. |
