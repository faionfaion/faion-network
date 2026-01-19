# faion-software-developer

Full-stack software development skill covering Python, JavaScript/TypeScript, backend languages, testing, API design, and browser automation. Contains 70+ methodologies and 14,690+ lines of technical reference.

## Overview

This skill orchestrates all software development activities. It provides patterns, best practices, and code examples for modern development across multiple languages and frameworks. Used by code and test agents for consistent, production-quality output.

## Structure

| Path | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition, quick reference, methodology index |
| `references/` | Technical reference documents (14 files, ~14,000 lines) |
| `references/django/` | Django-specific patterns and conventions (7 files) |

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
| python.md | Python, Django, FastAPI, pytest, typing | ~1760 |
| javascript.md | TypeScript, React, Node.js, Bun, testing | ~1350 |
| backend.md | Go, Ruby, PHP, Java, C#, Rust backend patterns | ~3180 |
| api-design.md | REST, GraphQL, OpenAPI, versioning | ~2250 |
| testing.md | pytest, Jest, Vitest, E2E testing | ~1810 |
| browser-automation.md | Puppeteer, Playwright, scraping | ~1490 |
| methodologies.md | 68 development methodologies (M-DEV-*) | ~1573 |
| best-practices-2026.md | AI-assisted development, modern patterns | ~600 |

## Methodologies

32 core methodologies organized by domain:

- **M-PY-001 to M-PY-008**: Python (Poetry, Django, FastAPI, pytest, typing)
- **M-JS-001 to M-JS-008**: JavaScript/TypeScript (React, Node.js, testing)
- **M-BE-001 to M-BE-008**: Backend (architecture, databases, caching, auth)
- **M-API-001 to M-API-008**: API design (REST, OpenAPI, versioning, security)

## Quick Commands

```bash
# Python
black src/ && isort src/           # Format
pytest --cov=src                   # Test

# JavaScript/TypeScript
prettier --write .                 # Format
eslint . --fix                     # Lint
vitest run --coverage              # Test
```

## Language Selection

| Language | Use Case |
|----------|----------|
| Python | Backend APIs, data processing, ML, scripting |
| TypeScript | Frontend, Node.js backend, full-stack |
| Go | High-performance services, CLI tools |
| Rust | Systems programming, WASM |

## Framework Selection

| Framework | Use Case |
|-----------|----------|
| Django | Full-featured web apps, admin panels |
| FastAPI | Modern async APIs, microservices |
| React | Complex UIs, SPAs |
| Next.js | Full-stack React, SSR/SSG |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops | Deployment, CI/CD, infrastructure |
| faion-ml | AI/ML integrations |
| faion-sdd | Specification-driven development |
