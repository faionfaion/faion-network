# LLM-Friendly Architecture

## Summary

Architecture patterns that keep individual source files between 100-300 lines, use flat directory structures (max 3 levels), self-documenting file names, and explicit imports — designed to reduce LLM edit errors caused by large files and hidden import chains.

## Why

LLMs make measurably more errors editing files over 300 lines: context truncation causes wrong line numbers, missed dependencies, and dropped code. Barrel re-exports hide actual file locations causing agents to edit the wrong file. File size and explicitness are correctness requirements for AI-assisted work, not just style choices.

## When To Use

- Planning a new codebase where Claude Code or similar AI tools will handle ongoing development.
- Refactoring an existing repo where AI-assisted edits frequently produce wrong line numbers or missed imports.
- Code review: auditing PRs where files exceed 300 lines before merging.
- After a retrospective identifies "AI tool makes mistakes in large files" as a recurring problem.

## When NOT To Use

- Generated code (protobuf outputs, ORM migrations, auto-generated clients) — file size limits don't apply to machine-generated files.
- Legacy monolith stabilization where any structural change risks regressions; defer until test coverage is in place.
- Performance-critical CLI hot paths where splitting files increases import overhead.
- Teams not using AI tooling — enforced decomposition overhead may outweigh benefit.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core rules: file size limits, flat structure, self-documenting names, explicit imports, data extraction, type colocation. |
| `content/02-antipatterns.xml` | God components, utils dumping grounds, deep re-exports, inline large data, ambiguous file names. |

## Templates

| File | Purpose |
|------|---------|
| `templates/llm-arch-audit.sh` | Bash script to find files exceeding line limit and list barrel re-exports. |
| `templates/claude-md-project.md` | CLAUDE.md skeleton explaining project structure conventions for LLMs. |
