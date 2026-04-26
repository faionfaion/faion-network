# Documentation (AGENTS.md / CLAUDE.md)

## Summary

Methodology for creating and maintaining AI-readable `AGENTS.md` + `CLAUDE.md` documentation for modules, packages, and directories. Each directory gets one `AGENTS.md` (20-80 lines) describing what the dir is, its file table, key types, and commands, paired with `CLAUDE.md` containing only `@AGENTS.md`.

## Why

AI agents entering a codebase cold need a machine-readable routing doc to decide which files to load. Without `AGENTS.md`, the agent must scan all files to form context, wasting tokens and hallucinating structure. Two-pass generation (discovery → write → verify) keeps docs accurate; a nightly drift check catches stale tables before they mislead agents.

## When To Use

- Bootstrapping AI-readable docs in a new repo, sub-package, or refactored directory.
- After a refactor where the file tree changed and existing `AGENTS.md` tables are stale.
- Multi-repo monorepos: each package needs its own `AGENTS.md` per the project convention.
- Legacy codebases with only a top-level README — rolling out per-module coverage.

## When NOT To Use

- Repos under ~200 lines with one obvious entry point — a README suffices.
- Generated/derived directories (`dist/`, `build/`, `node_modules/`) — docs just repeat tooling output.
- Short-lived experiments where the doc rots faster than the code iterates.
- Public-facing user docs (Docusaurus/Mintlify) — this methodology targets AI readers, not customers.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Required sections, line caps, file-table rules, when to split to subfolders. |
| `content/02-generation-workflow.xml` | Two-pass pipeline: discovery agent → writer agent → verifier agent; prompt patterns. |
| `content/03-antipatterns.xml` | Hallucinated files, length creep, ASCII art, stale tables, self-referential loops. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agents-md-universal.md` | Universal AGENTS.md skeleton with all required sections. |
| `templates/doc-outline.sh` | Discovery script: emits JSON outline from `git ls-files` + `tokei`. |
