---
slug: go-project-structure
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Standard Go project layout following community conventions: cmd/ for entry points, internal/ for private app code, pkg/ only for truly public API.
content_id: "50a320b0762ea1de"
tags: [go, project-structure, architecture, best-practices, devops]
---
# Go Project Structure

## Summary

**One-sentence:** Standard Go project layout following community conventions: cmd/ for entry points, internal/ for private app code, pkg/ only for truly public API.

**One-paragraph:** Standard Go project layout following community conventions: cmd/ for entry points, internal/ for private app code, pkg/ only for truly public API. Dependencies wired by hand in cmd/.../main.go; no DI framework until hand-wiring exceeds ~100 lines. Core rules: internal/ default, CGO_ENABLED=0 in containers, one .golangci.yml shared by local dev and CI.

## Applies If (ALL must hold)

- Bootstrapping a new Go service, CLI, or library
- Refactoring a flat single-package program that has crossed ~3 entry points or ~5 domain concepts
- Standardizing across multiple Go services so agents can navigate predictably
- Wiring DI manually with constructors in cmd/<bin>/main.go
- Producing repeatable Docker + Makefile + module hygiene that LLMs can replicate

## Skip If (ANY kills it)

- One-file scripts and learning exercises — flat layout beats premature internal/cmd/pkg
- Pure libraries: don't add internal/ and cmd/ if all you ship is exported packages
- Code generators that already define their own layout (buf, kubebuilder, cobra-cli)
- Multi-language monorepos where Go is one of N — use the org-wide layout, not Go-specific defaults
- When team consensus differs: enforcing golang-standards/project-layout against the team will lose

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-developer/`
