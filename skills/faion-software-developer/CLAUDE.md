# faion-software-developer

<<<<<<< HEAD
Full-stack software development skill covering Python, JavaScript/TypeScript, backend languages, testing, API design, and browser automation. Contains 111 methodologies and 14,690+ lines of technical reference.
=======
Software development orchestrator coordinating 7 specialized sub-skills.
>>>>>>> claude

## Overview

**Type:** Orchestrator skill
**Sub-skills:** 7
**Total methodologies:** 184
**Version:** 2.0

## Structure

<<<<<<< HEAD
| Path | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, quick reference, methodology index |
| `ref-*.md` | Technical reference documents (28 files, ~14,000 lines) |
| `django-*.md` | Django-specific patterns and conventions (7 files) |
| `*.md` | Methodologies (112 files) |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

## Key References

| File | Content | Lines |
|------|---------|-------|
| ref-python.md | Python, Django, FastAPI, pytest, typing | ~1760 |
| ref-javascript.md | TypeScript, React, Node.js, Bun, testing | ~1350 |
| ref-go-backend.md | Go backend, Gin, Echo, concurrency | ~500 |
| ref-testing.md | pytest, Jest, Vitest, E2E testing | ~1810 |
| ref-browser-automation.md | Puppeteer, Playwright, scraping | ~1490 |
| ref-methodologies.md | 68 development methodologies | ~1573 |
| ref-best-practices-2026.md | AI-assisted development, modern patterns | ~600 |

## Methodologies

Organized by domain with semantic naming:

- **Python**: python.md, testing.md, django/ (7 files)
- **JavaScript/TypeScript**: javascript.md, testing.md, frontend-design.md
- **Backend**: go-backend.md, ruby-rails.md, php-laravel.md, java-spring.md, csharp-dotnet.md, rust-backend.md
- **API Design**: rest-api-design.md, graphql-api.md, openapi-specification.md, api-versioning.md, api-authentication.md

## Quick Commands

```bash
# Python
black src/ && isort src/           # Format
pytest --cov=src                   # Test

# JavaScript/TypeScript
prettier --write .                 # Format
eslint . --fix                     # Lint
vitest run --coverage              # Test
=======
```
faion-software-developer/          (Orchestrator)
├── SKILL.md                        (Routing logic)
├── CLAUDE.md                       (This file)
├── files-reference.md              (File catalog)
└── language-framework-guide.md     (Framework selection)

Sub-skills:
├── faion-python-developer/         (24 methodologies)
├── faion-javascript-developer/     (18 methodologies)
├── faion-backend-developer/        (47 methodologies)
├── faion-frontend-developer/       (18 methodologies)
├── faion-api-developer/            (19 methodologies)
├── faion-testing-developer/        (12 methodologies)
└── faion-devtools-developer/       (46 methodologies)
>>>>>>> claude
```

## Sub-Skills Quick Reference

| Sub-skill | Focus | Methodologies |
|-----------|-------|---------------|
| [faion-python-developer](../faion-python-developer/CLAUDE.md) | Django, FastAPI, async, pytest | 24 |
| [faion-javascript-developer](../faion-javascript-developer/CLAUDE.md) | React, Node.js, Next.js, TypeScript | 18 |
| [faion-backend-developer](../faion-backend-developer/CLAUDE.md) | Go, Rust, Java, C#, PHP, Ruby | 47 |
| [faion-frontend-developer](../faion-frontend-developer/CLAUDE.md) | Tailwind, CSS-in-JS, UI libs, PWA | 18 |
| [faion-api-developer](../faion-api-developer/CLAUDE.md) | REST, GraphQL, OpenAPI, auth | 19 |
| [faion-testing-developer](../faion-testing-developer/CLAUDE.md) | Unit, integration, E2E, TDD | 12 |
| [faion-devtools-developer](../faion-devtools-developer/CLAUDE.md) | Automation, architecture, quality | 46 |

## Routing Logic

**Python projects:** faion-python-developer
**JavaScript/TypeScript:** faion-javascript-developer
**Other backends:** faion-backend-developer
**Styling/UI:** faion-frontend-developer
**API design:** faion-api-developer
**Testing:** faion-testing-developer
**Tools/architecture:** faion-devtools-developer

## Usage

Invoked via `/faion-net` or directly as `/faion-software-developer`. Automatically delegates to appropriate sub-skill based on task requirements.

## Related Skills

- [faion-net](../faion-net/CLAUDE.md) - Parent orchestrator
- [faion-software-architect](../faion-software-architect/CLAUDE.md) - Architecture decisions
- [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) - Infrastructure
- [faion-sdd](../faion-sdd/CLAUDE.md) - Specification-driven development

---

*faion-software-developer v2.0 | Orchestrator | 184 methodologies across 7 sub-skills*
