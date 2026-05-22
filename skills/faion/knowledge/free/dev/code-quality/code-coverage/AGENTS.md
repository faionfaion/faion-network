---
slug: code-coverage
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a coverage-gate config (branch + diff-cover, per-dir thresholds, exclusion list) plus an uncovered-lines extract feeding LLM test-author subagents.
content_id: "b49a1f353bbb2655"
complexity: medium
produces: config
est_tokens: 4200
tags: [coverage, testing, ci, diff-cover]
---
# Code Coverage

## Summary

**One-sentence:** Configures branch + diff coverage as a CI gate and emits a machine-readable uncovered-lines artefact that LLM test-author subagents can act on.

**One-paragraph:** Line coverage alone passes when an if-branch fires but its else-branch never runs — half the logic is untested with 100% on the dashboard. This methodology forces branch coverage on every project, enforces diff-cover on PRs so legacy gaps don't block ongoing work, sets per-directory thresholds (critical paths 90%+, glue code 70%), and produces a tiny JSON of uncovered lines per touched file so an LLM test-author can write targeted tests without parsing 100KB of XML. Fowler's anchor stays: coverage is a gap-finder, not a goal — the gate is the floor, mutation testing is the ceiling.

**Ефективно для:**

- Стартові проекти: налаштувати branch + diff-cover з нуля, без накопиченого боргу.
- Legacy-репо з низьким покриттям: diff-cover розблоковує нові PR без вимоги "довести покриття до 80% спочатку".
- AI-loop тест-генерації: jq-фільтр витягує лише непокриті рядки → ~2K токенів контексту замість 100K XML.
- Команди, яким нав'язали SaaS-coverage (Codecov), а вони хочуть звести залежність до GitHub-артефакта.

## Applies If (ALL must hold)

- Project has a working test runner (pytest, jest, vitest, go test, cargo test, etc.).
- CI runs on every PR and has write-access to publish artefacts / comments.
- A repo `main` (or `develop`) branch exists to diff against.

## Skip If (ANY kills it)

- One-off script / throwaway prototype — gating cost exceeds the value.
- UI-snapshot-heavy codebase where visual diff is the real signal (line coverage is misleading).
- Generated / migration code (ORM migrations, protobuf stubs) — exclude rather than try to cover.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test runner config | `pyproject.toml` / `jest.config.js` / `vitest.config.ts` | repo root |
| CI workflow file | YAML | `.github/workflows/` |
| Critical-path manifest | Markdown list of dirs requiring ≥90% | repo `AGENTS.md` or docs |
| Baseline branch | git ref | `main` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Coverage is a foundational rubric — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: branch-required, diff-cover-on-pr, per-dir-thresholds, exclusion-policy, no-pragma-ratcheting, mutation-quarterly, extract-don't-paste | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for coverage-gate config + uncovered-lines extract | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: gaming, pragma-ratchet, threshold-lowering, async-config-gap | 700 |
| `content/04-procedure.xml` | essential | 5-step setup procedure from green-field to gating PR | 800 |
| `content/06-decision-tree.xml` | essential | Routing: language → tool → config-stack → gate-mode | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | File-pattern matching; no inference required. |
| `write_config` | haiku | Filling a known template; deterministic. |
| `extract_uncovered` | haiku | `jq` / XPath transform over coverage XML. |
| `write_targeted_tests` | sonnet | Per-file generation with source pinned in context. |
| `mutation_review` | opus | Cross-file synthesis; quarterly batch only. |

## Templates

| File | Purpose |
|------|---------|
| `templates/coverage.pyproject.toml` | Python: branch=true, fail_under=80, exclude_lines |
| `templates/jest.coverage.config.js` | JS/TS: V8 provider, per-dir thresholds, lcov reporter |
| `templates/diff-cov-report.sh` | Runs pytest + diff-cover, emits per-file uncovered-lines prompt fragments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-coverage.py` | Validate a coverage-gate config + extract against the schema | After config write, before PR merge |

## Related

- [[code-review-process]] — the gate this methodology produces runs inside the review process.
- [[refactoring-patterns]] — high-churn + low-coverage → first refactor candidates.

## Decision tree

See `content/06-decision-tree.xml`. The tree first branches on detected stack (Python / JS-TS / Go / Rust / mixed) → picks the canonical coverage tool → asks whether the repo is green-field or legacy. Green-field gets a single global threshold; legacy gets diff-cover only (so historical gaps do not block PRs). All leaves reference rules from `01-core-rules.xml`.
