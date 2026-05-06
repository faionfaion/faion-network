---
name: faion-automation-tooling
description: "Automation & tooling specialist: browser automation, CI/CD, monorepo, performance testing, feature flags. 23 methodologies."
tier: solo
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Automation & Tooling Sub-Skill

Browser automation, CI/CD pipelines, monorepo management, and developer tooling.

## Purpose

Handles browser automation, web scraping, CI/CD pipelines, monorepo management, performance testing, feature flags, and development tooling.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| CI/CD config | `.github/workflows/`, `.gitlab-ci.yml` | Pipeline automation |
| Monorepo structure | `turbo.json`, `pnpm-workspace.yaml` | Monorepo tooling |
| Testing setup | Performance test suites, k6 scripts | Testing automation |
| Feature flag config | LaunchDarkly, Unleash SDK | Feature flag usage |
| Browser automation | Puppeteer/Playwright scripts | Automation scripts |

### Discovery Questions

```yaml
questions:
  - question: "What automation do you need?"
    options:
      - label: "Browser automation/scraping"
        description: "Use puppeteer-automation or playwright-automation"
      - label: "CI/CD pipeline"
        description: "Use cd-basics, cd-pipelines"
      - label: "Monorepo management"
        description: "Use monorepo-turborepo, pnpm-package-management"
      - label: "Performance testing"
        description: "Use perf-test-basics, perf-test-tools"

  - question: "What's your monorepo scale?"
    options:
      - label: "Small (2-5 packages)"
        description: "Simple workspace setup"
      - label: "Medium (5-15 packages)"
        description: "Use Turborepo for caching"
      - label: "Large (15+ packages)"
        description: "Full Turborepo + pnpm optimization"

  - question: "Are you using feature flags?"
    options:
      - label: "Yes, in production"
        description: "Use feature-flags for best practices"
      - label: "Planning to implement"
        description: "Start with feature-flags basics"
      - label: "No"
        description: "Skip feature flag methodologies"
```

---

## When to Use

- Browser automation (Puppeteer, Playwright)
- Web scraping
- CI/CD pipelines
- Monorepo management (Turborepo, pnpm)
- Performance testing
- A/B testing
- Feature flags
- Trunk-based development
- Logging patterns
- Internationalization
- AI-assisted development

## Methodologies (49 files)

**Browser Automation (4):** puppeteer-automation, playwright-automation, browser-automation-overview, web-scraping

**DevOps (3):** cd-basics, cd-pipelines, continuous-delivery

**Dev Methodologies (3):** dev-methodologies-architecture, dev-methodologies-practices, dev-methodologies-testing

**Tooling (5):** pnpm-package-management, monorepo-turborepo, feature-flags, internationalization, logging-patterns

**Testing & Quality (4):** perf-test-basics, perf-test-tools, ab-testing-basics, ab-testing-implementation

**Trunk-Based Dev (2):** trunk-based-dev-principles, trunk-based-dev-patterns

**Modern Practices (2):** ai-assisted-dev, best-practices-2026

### Puppeteer (split methodologies)

- `puppeteer-launch-setup` — launch flags, browser context, env
- `puppeteer-page-interaction` — clicks, forms, waits, selectors
- `puppeteer-session-management` — cookies, storage, persistent state
- `puppeteer-output-capture` — screenshots, PDFs, traces
- `puppeteer-stealth-proxy` — stealth, proxy chains, fingerprinting
- `puppeteer-agent-workflow` — agent-driven Puppeteer flows

### Web scraping (split methodologies)

- `web-scraping-element-extraction` — selectors, attributes, text
- `web-scraping-pagination` — paged lists, infinite scroll, cursors
- `web-scraping-resilience` — retries, backoff, rate limits, errors
- `web-scraping-agentic-workflow` — agent-driven scraping pipelines

### Feature flags (split methodologies)

- `feature-flags-types-lifecycle` — flag types and lifecycle
- `feature-flags-core-implementation` — flag core impl patterns
- `feature-flags-rollout-targeting` — rollouts, segments, targeting
- `feature-flags-services-testing` — testing flagged services

### Trunk-based development (split methodologies)

- `trunk-based-ci-gates` — CI gates for trunk-based dev
- `trunk-based-feature-flags` — flags as branch-by-config
- `trunk-based-branch-by-abstraction` — branch by abstraction patterns
- `trunk-based-challenges` — common trunk-based challenges

### Practices (per stack)

- `practices-python-ecosystem` — Python ecosystem practices
- `practices-django-coding` — Django-specific coding practices
- `practices-backend-languages` — backend language practices
- `practices-js-ts-stack` — JS/TS stack practices
- `practices-frontend-components` — frontend component practices

### Testing (per stack)

- `testing-django-pytest` — Django + pytest practices
- `testing-backend-languages` — backend language testing
- `testing-js-ts-frontend` — JS/TS frontend testing

## Tools

**Automation:** Puppeteer, Playwright, Selenium
**Monorepo:** Turborepo, Nx, pnpm workspaces
**CI/CD:** GitHub Actions, GitLab CI, Jenkins
**Performance:** Lighthouse, k6, Artillery
**Feature flags:** LaunchDarkly, Unleash, PostHog

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-code-quality | Code quality and architecture |
| faion-devops-engineer | Infrastructure and deployment |
| faion-cicd-engineer | Advanced CI/CD |

## Integration

Invoked by parent skill `faion-devtools-developer` for automation and tooling work.

---

*faion-automation-tooling v1.0 | 49 methodologies*
