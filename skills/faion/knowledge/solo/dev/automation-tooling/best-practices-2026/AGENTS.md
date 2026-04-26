# Software Development Best Practices 2026

## Summary

A navigation hub for modern JS/TS/Python development standards as of 2026: TypeScript 5 strict config, React 19 server components, Next.js 15 patterns, Python 3.13 features, and AI-assisted development guidelines. Content is split into three focused sub-docs; always load the relevant sub-doc — reading the hub alone gives only a table of contents.

## Why

Stack currency directly affects build-time performance, type safety, and developer velocity. The 2026 baseline documents which features are now default (TS strict mode, React server-first, ruff over flake8), which are adopted gradually (exactOptionalPropertyTypes), and which AI-tooling practices reduce rather than increase rework. Quarterly review against this hub prevents stack drift.

## When To Use

- Auditing whether a project's stack aligns with current standards (TS version, eslint config, Python tooling).
- Generating the standards section of CONTRIBUTING.md or AGENTS.md for a new project.
- Choosing which React 19 / Next.js 15 / Python 3.13 features to adopt in a modernization sprint.
- Defining an AI-assisted dev playbook: tool selection, prompt patterns, AI test generation guardrails.

## When NOT To Use

- Deep language-specific patterns (services, views, handlers) — see `dev-methodologies-practices`.
- Architecture decisions (monolith vs microservice) — see `dev-methodologies-architecture`.
- When the project has a stricter or newer house standard than this 2026 baseline — defer to that.
- One-shot bug fixes — load only the specific section, not the full hub.

## Content

| File | What's inside |
|------|---------------|
| `content/01-typescript.xml` | TS 5 strict config flags, module resolution `bundler`, `verbatimModuleSyntax`, advanced patterns. |
| `content/02-react-python.xml` | React 19 server components/actions, Next.js 15 caching, Python 3.13 features, ruff config. |
| `content/03-ai-dev.xml` | AI tool selection (Copilot/Cursor/Claude Code), prompt patterns, AI test generation guardrails. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig-strict-2026.json` | TS 5 strict baseline with all 2026 recommended flags. |
| `templates/pyproject-2026.toml` | Python 3.13 + ruff + mypy strict baseline for `pyproject.toml`. |
