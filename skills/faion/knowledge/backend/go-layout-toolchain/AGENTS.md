# Go Standard Layout — Toolchain Reference

## Summary

**One-sentence:** Produces a toolchain map per layout slot: `cmd/` (cobra), `internal/handler` (Gin/Echo/Chi), `internal/repository` (sqlc/sqlx), `migrations/` (Goose/Atlas), tests (testify, goleak), live-reload (air), CI services.

**Ефективно для:**

- Selecting tools for a new Go service.
- Auditing an existing service against best practice.
- Standardising toolchain across multiple services in a team.
- Avoiding tool-bikeshedding per PR.

**One-paragraph:** The Go standard layout is toolchain-agnostic, but each slot in the layout (`cmd/`, `internal/handler`, `internal/repository`, `migrations/`) maps to a preferred set of tools. This reference pairs tools to layout slots so agents select the right binary for the job rather than inventing combinations.

## Applies If (ALL must hold)

- Layout follows `cmd/` + `internal/` + `pkg/` + `migrations/`.
- Team open to standardising toolchain.
- CI environment supports the chosen tools.
- License / org constraints checked.

## Skip If (ANY kills it)

- Greenfield experiments with bespoke layout — choose tools freely.
- Polyglot service where Go is one of many runtimes — broader cross-stack ref applies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Layout adopted (`go-layout-directory-structure`) | doc | tech lead |
| CI runtime constraints | doc | SRE |
| License policy | doc | legal / org |
| Inventory of current tools | spreadsheet | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-layout-directory-structure]]` | layout convention |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-tools` | sonnet | Reads existing repo + lists tools per slot. |
| `draft-toolchain-table` | haiku | Slot → tool map. |
| `write-stack-md` | sonnet | Persisted decision in `.aidocs/stack.md`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-layout-toolchain.json` | JSON Schema for the Go Standard Layout — Toolchain Reference output contract |
| `templates/go-layout-toolchain.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-layout-toolchain.py` | Enforce the Go Standard Layout — Toolchain Reference output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-layout-directory-structure]]
- [[go-layout-layer-rules]]
- [[go-layout-agentic-workflow]]
- [[go-backend]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
