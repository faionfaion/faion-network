# references/

Technical reference documents for software development. Contains detailed patterns, code examples, and best practices across languages and frameworks.

## Overview

This folder provides in-depth technical context for development tasks. Each file focuses on a specific technology or domain area. Total: 19 files, ~14,000 lines of reference material.

## Files

### Language References

| File | Content | Size |
|------|---------|------|
| `python.md` | Python ecosystem: Django, FastAPI, pytest, Poetry, typing, async patterns | ~1760 lines |
| `javascript.md` | TypeScript 5.x, React 19.x, Node.js 22, Bun, ESLint 9, testing | ~1350 lines |

### Backend Languages (6 files)

| File | Content |
|------|---------|
| `go-backend.md` | Go: Gin, Echo, project structure, concurrency, error handling |
| `ruby-rails.md` | Ruby: Rails patterns, ActiveRecord, RSpec, Sidekiq |
| `php-laravel.md` | PHP: Laravel patterns, Eloquent, PHPUnit, Queues |
| `java-spring.md` | Java: Spring Boot, JPA/Hibernate, JUnit, Async |
| `csharp-dotnet.md` | C#: ASP.NET Core, Entity Framework, xUnit, Background Services |
| `rust-backend.md` | Rust: Axum, Actix, Tokio async patterns, testing |

### API and Testing

| File | Content | Size |
|------|---------|------|
| `api-design.md` | REST conventions, GraphQL, OpenAPI/Swagger, versioning, pagination, error handling | ~2250 lines |
| `testing.md` | pytest, Jest, Vitest, Playwright, Cypress; fixtures, mocking, parametrization | ~1810 lines |
| `browser-automation.md` | Puppeteer and Playwright: scraping, screenshots, PDF generation, form automation | ~1490 lines |

### Frontend

| File | Content | Size |
|------|---------|------|
| `frontend-design.md` | UI brainstorming workflow, Storybook integration, component structure | ~90 lines |
| `shadcn-ui.md` | shadcn/ui architecture: CVA variants, compound components, theming | ~160 lines |
| `tailwind.md` | Tailwind patterns: class ordering, design tokens, cn() helper, dark mode | ~250 lines |

### Architecture and Process

| File | Content | Size |
|------|---------|------|
| `methodologies.md` | 68 development methodologies (M-DEV-*): merged from multiple skills | ~1573 lines |
| `documentation.md` | CLAUDE.md creation templates for different project types | ~180 lines |
| `best-practices-2026.md` | AI-assisted development, modern tooling (Claude Code, Cursor, Copilot) | ~600 lines |

### Subfolders

| Folder | Content |
|--------|---------|
| `django/` | Django-specific patterns: models, services, API, testing, Celery (7 files) |

## Usage

Reference files are loaded by agents when working on specific technology areas. For example:

- Working with Django models -> read `python.md` + `django/models.md`
- Building REST API -> read `api-design.md`
- Setting up tests -> read `testing.md`
- Creating UI components -> read `tailwind.md` + `shadcn-ui.md`
- Go backend development -> read `go-backend.md`
- Java Spring Boot -> read `java-spring.md`
- Rust web services -> read `rust-backend.md`

## Key Patterns

- **Service layer**: Business logic in services, thin views/controllers
- **Type safety**: Type hints (Python) / TypeScript strict mode everywhere
- **Testing pyramid**: 70% unit, 20% integration, 10% E2E
- **Code quality**: Automated formatting (Black/Prettier), linting, pre-commit hooks
