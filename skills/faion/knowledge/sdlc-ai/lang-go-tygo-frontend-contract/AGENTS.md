# Go → TypeScript DTO Contract via tygo

## Summary

**One-sentence:** In any Go-backend / TS-frontend repo, Go struct definitions are the single source of truth — generate TS types with tygo from a committed tygo.yaml and check the diff in CI.

**One-paragraph:** Go → TypeScript DTO Contract via tygo produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Go backend + TS/JS frontend sharing DTOs.
- Drift between Go struct and TS type repeatedly breaks the frontend.
- Monorepo with both languages and a single PR can change both sides.
- API surface stable enough to codegen (not gRPC + protoc).

## Applies If (ALL must hold)

- Backend is Go, frontend is TS/JS.
- DTOs live in identifiable Go packages (e.g. internal/api/dto/).
- Repo can commit generated TS to a known dir (frontend/src/api-types/).
- CI can run `tygo generate` and diff the output.

## Skip If (ANY kills it)

- Both sides own their own types deliberately (loose contract).
- gRPC + protoc already covers the surface.
- DTOs change daily during prototype — codegen churn slows everyone.
- Frontend not in TS — tygo target unavailable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| tygo binary | go install github.com/gzuidhof/tygo | dev-env |
| tygo.yaml | committed tygo config | platform |
| Output dir | frontend/src/api-types/ | frontend lead |
| CI gate | `tygo generate && git diff --exit-code` | ci-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Local pre-commit can also run tygo |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tygo_config_draft` | sonnet | Pick packages + naming + tag handling. |
| `ci_gate_wire` | haiku | Add the codegen-diff stage. |
| `migration_initial_run` | sonnet | Resolve naming collisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tygo.yaml` | Committed tygo config. |
| `templates/ci-tygo-diff.yml` | CI job that fails on uncommitted regen. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-tygo-frontend-contract.py` | Validate the tygo-config artefact. | pre-merge of tygo config |

## Related

- [[mr-codemod-refactor-agent]]
- [[lint-precommit-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
