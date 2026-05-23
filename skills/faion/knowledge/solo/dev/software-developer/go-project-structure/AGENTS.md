---
slug: go-project-structure
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Lay out a Go project with cmd/, internal/, pkg/ (only when public), migrations/, and a single Makefile-driven workflow.
content_id: "50a320b0762ea1de"
complexity: medium
produces: code
est_tokens: 4000
tags: [go, project-structure, architecture, best-practices, devops]
---
# Go Project Structure

## Summary

**One-sentence:** Lay out a Go project with cmd/, internal/, pkg/ (only when public), migrations/, and a single Makefile-driven workflow.

**One-paragraph:** Standard Go project layout following community conventions: cmd/ for entry points, internal/ for private app code, pkg/ only for truly public API surface that external consumers will import, migrations/ for DB DDL, and a single Makefile orchestrating build/test/lint. Imports flow inward (cmd → internal/<feature>); cross-feature dependencies in internal/ go through interfaces declared at consumer side. Output is the directory layout + Makefile + initial wiring.

**Ефективно для:**

- Greenfield Go services adopting community-standard layout.
- Refactoring projects that grew into ad-hoc top-level dirs.
- Multi-binary repos (cmd/api, cmd/worker, cmd/migrate).
- Establishing reviewable boundaries before features compound.

## Applies If (ALL must hold)

- Go module project (Go 1.21+).
- Project size >=1kloc OR contains >=2 binaries.
- Team works in the repo (more than one author).
- Engineering wants enforceable import boundaries (internal/ enforcement).

## Skip If (ANY kills it)

- Single-file CLI experiment — pkg/cmd separation has no payoff.
- Library-only repo (no main) — different conventions apply.
- Project follows a different established pattern (Kubernetes-style, Buf) — adapt instead.
- Monorepo with framework-specific layout (Bazel rules) that overrides.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Module path (go.mod) chosen | go.mod | tech-lead |
| Entry point count (cmd/<name>) | list | tech-lead |
| Public-vs-private API decision: anything in pkg/? | ADR | tech-lead |
| Tooling decision: Make vs Mage vs Justfile | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-error-handling-patterns]] | apperror package lives under internal/. |
| [[go-concurrency-patterns]] | Worker packages live under internal/. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (cmd for entries, internal for private, pkg only for public, no cyclic deps, makefile orchestration, no top-level loose files) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for project structure spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: skeleton → entries → internal split → makefile → enforce import boundaries | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `skeleton_scaffold` | sonnet | Mechanical: create dirs + go.mod + Makefile. |
| `import_boundary_check` | sonnet | Run import-boundary linter; flag violations. |
| `makefile_authoring` | sonnet | Standard targets: build/test/lint/run/docker. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scaffold-go.sh` | Bootstrap script: create cmd/, internal/, pkg/, migrations/, Makefile |
| `templates/Makefile` | Build/test/lint/run/docker targets |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-project-structure.py` | Validate project structure spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-standard-layout]]
- [[go-error-handling-patterns]]
- [[go-concurrency-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps project size, binary count, and public-API intent to a rule from `01-core-rules.xml`, telling the agent whether to apply the layout or skip in favour of an alternate convention. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
