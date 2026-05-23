---
slug: go-layout-layer-rules
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an enforced layering plan: handler imports service interface, service imports repository interface, repository implements it. Automated via depguard + golangci-lint; PR review gate."
content_id: "4ad13df133e6f0b9"
complexity: medium
produces: spec
est_tokens: 3700
tags: [go, layout, depguard, layers, import-rules]
---

# Go Standard Layout — Layer Dependency Rules

## Summary

**One-sentence:** Produces an enforced layering plan: handler imports service interface, service imports repository interface, repository implements it. Automated via depguard + golangci-lint; PR review gate.

**Ефективно для:**

- Layered services (handler → service → repository).
- Teams that have suffered cross-layer leakage previously.
- Codebases enforcing testability of the service layer.
- LLM agents generating per-resource handlers + services.

**One-paragraph:** The Go standard layout only enforces package visibility via `internal/` — it does NOT enforce dependency direction between layers. Without `depguard` or equivalent import linting, handler packages freely import repository packages directly, bypassing the service layer. Explicit rules + automated linting are required to make the layout load-bearing.

## Applies If (ALL must hold)

- Layered architecture in use.
- golangci-lint already wired into CI.
- `depguard` (or equivalent) supported in the lint config.
- PR reviewers have the bandwidth to enforce.

## Skip If (ANY kills it)

- Single-layer scripts — no layers to enforce.
- Pure library modules — no layering applies.
- Codebases moving to micro-modules where each module is one layer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Layered architecture diagram | doc | tech lead |
| golangci-lint config | yaml | SRE |
| depguard rules block | yaml | SRE |
| CI gate (block merge on lint fail) | CI config | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-layout-directory-structure]]` | directory tree |

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
| `draft-depguard-rules` | sonnet | Translate diagram into rule yaml. |
| `audit-existing-imports` | sonnet | Finds upward / cross-layer imports. |
| `write-ci-gate` | haiku | CI yaml + reviewer doc. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-layout-layer-rules.json` | JSON Schema for the Go Standard Layout — Layer Dependency Rules output contract |
| `templates/go-layout-layer-rules.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-layout-layer-rules.py` | Enforce the Go Standard Layout — Layer Dependency Rules output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-layout-directory-structure]]
- [[go-layout-toolchain]]
- [[go-layout-agentic-workflow]]
- [[go-backend]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
