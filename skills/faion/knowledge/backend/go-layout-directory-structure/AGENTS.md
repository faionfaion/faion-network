# Go Standard Layout — Directory Structure

## Summary

**One-sentence:** Produces a canonical Go service tree: `cmd/<bin>`, `internal/<feature>`, `pkg/<lib>`, `migrations/` with file-naming conventions; one agreed layout that scales from single service to multi-binary monorepo.

**Ефективно для:**

- New Go services scaffolded from scratch.
- Refactoring a flat / chaotic Go repo to a standard layout.
- Multi-binary monorepos under one `cmd/` parent.
- Onboarding new devs to a repeatable convention.

**One-paragraph:** Organize every Go service under a four-directory skeleton: `cmd/` (binaries), `internal/` (private app code), `pkg/` (public libraries), `migrations/` (schema files). The layout is a community convention — not enforced by the toolchain — so teams must agree on it once and commit it to docs.

## Applies If (ALL must hold)

- Go ≥1.17 (workspace mode optional).
- Service has both binaries and shared libraries.
- Project committed to `internal/` privacy semantics.
- Team agreed on the layout via ADR.

## Skip If (ANY kills it)

- Library-only repos (use Go module + `pkg/` only).
- Single-file CLIs — overhead not worth it.
- Existing layout already documented; do not introduce a second style.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| ADR adopting the layout | doc | tech lead |
| Migration tool (Goose / Atlas / golang-migrate) | ADR | tech lead |
| Module name | go.mod | team |
| Binary inventory | ops doc | team |

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
| `draft-tree` | haiku | Mechanical: emit dirs + placeholder files. |
| `audit-existing` | sonnet | Maps current dirs to canonical slots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-layout-directory-structure.json` | JSON Schema for the Go Standard Layout — Directory Structure output contract |
| `templates/go-layout-directory-structure.md.j2` | Markdown skeleton with the required fields |
| `templates/go-layout-directory-structure.md` | Markdown skeleton with the required fields Generated from `templates/go-layout-directory-structure.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-layout-directory-structure.py` | Enforce the Go Standard Layout — Directory Structure output contract | After subagent returns, before downstream consumer reads |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[go-layout-layer-rules]]
- [[go-layout-toolchain]]
- [[go-layout-agentic-workflow]]
- [[go-backend]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-layout-directory-structure.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-layout-directory-structure.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^gold\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
