---
slug: project-docs-convention
tier: geek
group: ai
domain: claude-code
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Two-file CLAUDE.md + AGENTS.md pattern per directory: CLAUDE.md is @AGENTS.md reference; AGENTS.md is the 20-80 line essential context for both Claude Code and Agent SDK.
content_id: "2304a3937d967da5"
complexity: medium
produces: spec
est_tokens: 4400
tags: [documentation, claude-code, agents, convention, multi-agent]
---
# Project Documentation Convention

## Summary

**One-sentence:** Two-file CLAUDE.md + AGENTS.md pattern per directory: CLAUDE.md is @AGENTS.md reference; AGENTS.md is the 20-80 line essential context for both Claude Code and Agent SDK.

**One-paragraph:** Claude Code auto-loads `CLAUDE.md`; standalone Agent SDK does not. Putting all context in CLAUDE.md makes it invisible to non-Claude-Code agents; putting it elsewhere makes Claude Code unaware. This convention partitions docs: `CLAUDE.md` = single line `@AGENTS.md`; `AGENTS.md` = essential 20-80 line context for this directory (auto-loaded by both); `.agents/` = on-demand detailed reference. Per-module coverage required — every directory with source code carries the pair. Output is a validated docs spec + scaffold script.

**Ефективно для:**

- Мультиагент-команди: CLAUDE.md для Claude Code, AGENTS.md для Agent SDK / autoheal / cron workers.
- Onboarding нового репо: scaffold script створює всі pair'и за одну команду.
- Audit існуючого репо: validator показує які dirs не мають pair'у.
- Migration з 'все в CLAUDE.md' → two-file pattern.

## Applies If (ALL must hold)

- Directory contains source code (not empty stub, not vendored).
- Both Claude Code and standalone agents will work on the codebase.
- Team uses faion-network conventions OR wants Agent-SDK-compatible docs.

## Skip If (ANY kills it)

- Trivial directories with &lt; 3 files and no logic (empty `__init__.py` stubs).
- External vendored code (`node_modules/`, `vendor/`).
- Temporary scratch dirs created during build / test.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Directory tree | repo source | git |
| Per-directory context | what each dir does + commands + gotchas | team / owners |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: claude-md-is-just-ref, agents-md-line-budget, per-module-coverage, agents-md-required-sections, agents-dir-for-deep-content | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-existing-tree` | haiku | Walk + glob. |
| `scaffold-missing-pairs` | haiku | Template fill. |
| `split-or-trim-long` | sonnet | Light judgment on what to keep in AGENTS.md vs `.agents/`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/CLAUDE.md` | Single-line CLAUDE.md template: `@AGENTS.md` |
| `templates/AGENTS.md` | AGENTS.md skeleton with required sections (dir purpose, file table, key types/commands, gotchas) |
| `templates/.agents-INDEX.md` | Skeleton INDEX.md for `.agents/` directories |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-project-docs-convention.py` | Validate the spec artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[skills]]
- [[agents]]
- [[commands]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
