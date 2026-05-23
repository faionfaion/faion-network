---
slug: best-practices-2026
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Audit rubric for a 2026 codebase: TypeScript 5 strict, React 19, Next.js 15 App Router, Python 3.13 strict typing, ruff + uv, AI-assisted SDD with quality gates.
content_id: "9d51bb92a40a964e"
complexity: deep
produces: rubric
est_tokens: 4300
tags: [typescript-5, react-19, python-313, ruff, ai-assisted-sdd]
---
# Software Development Best Practices 2026

## Summary

**One-sentence:** Audit rubric for a 2026 codebase: TypeScript 5 strict, React 19, Next.js 15 App Router, Python 3.13 strict typing, ruff + uv, AI-assisted SDD with quality gates.

**One-paragraph:** Audit rubric for a 2026 codebase: TypeScript 5 strict, React 19, Next.js 15 App Router, Python 3.13 strict typing, ruff + uv, AI-assisted SDD with quality gates. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Auditing or modernising a TS/Python codebase against current-year best practice.
- Onboarding a new agent to a project where tooling baseline must be confirmed before edits.
- Pre-launch hardening pass on a solo or small-team product.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Auditing or modernising a TS/Python codebase against current-year best practice.
- Onboarding a new agent to a project where tooling baseline must be confirmed before edits.
- Pre-launch hardening pass on a solo or small-team product.

## Skip If (ANY kills it)

- Stack is not TypeScript or Python — use stack-specific practice methodology instead.
- Codebase is on a frozen legacy version with no upgrade budget — rubric will only generate frustration.
- Bare-repo prototype with <100 LOC — premature standardisation.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Codebase root | git repo | team |
| package.json or pyproject.toml | manifest | repository |
| Lint+test command list | Makefile or package scripts | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[practices-python-ecosystem]] | stack-specific Python practices |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan-stack` | haiku | Detect framework versions from manifests. |
| `apply-rubric` | sonnet | Score each rubric item with citation. |
| `propose-remediation` | sonnet | Order fixes by blast radius. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | 2026 baseline rubric: each item has weight + acceptance criteria |
| `templates/audit_report.md` | Markdown audit report skeleton: per-item PASS/WARN/FAIL with remediation |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-best-practices-2026.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[practices-python-ecosystem]]
- [[practices-js-ts-stack]]
- [[practices-frontend-components]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the stack TS or Python AND repo >100 LOC?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
