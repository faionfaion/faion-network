# E2E Testing

End-to-end testing with Playwright and Cypress: real browser automation, POM architecture, and CI/CD integration.

## Summary

Guides writing maintainable E2E tests using the Page Object Model, handling authentication, API mocking, visual regression, and sharded CI pipelines. Covers Playwright (primary) and Cypress (secondary).

## Why

E2E tests validate full user journeys across real browsers. Without structure (POM, fixtures, data factories), suites become brittle and slow. This methodology enforces patterns that reduce flakiness and keep CI times bounded.

## When To Use

- Writing or reviewing Playwright / Cypress test suites
- Setting up E2E infrastructure from scratch (config, auth, CI sharding)
- Debugging flaky tests or selector failures
- Adding visual regression checks
- Migrating from Cypress to Playwright

## When NOT To Use

- Unit or integration tests (no browser needed) → use `unit-testing` or `testing-pytest`
- API-only testing → use HTTP client directly
- OAuth flows with real external providers (use storageState workaround instead)

## Content

| File | What it covers |
|------|---------------|
| `content/01-architecture.xml` | POM pattern, test pyramid (70/20/10), project layout, selector strategy |
| `content/02-patterns.xml` | Auth (storageState), API mocking (MSW/route), data factories, visual regression, mobile, multi-tab |
| `content/03-ci-and-flakiness.xml` | GitHub Actions sharding, retries, trace artifacts, flaky test prevention rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/playwright.config.ts` | Full Playwright config: projects, sharding, reporter, retries |
| `templates/pom-base.ts` | Abstract base Page class with navigation helpers |
| `templates/auth-setup.ts` | storageState auth setup fixture |
| `templates/factory.ts` | Data factory with faker, builder pattern |
| `templates/ci-workflow.yml` | GitHub Actions sharded Playwright workflow |
