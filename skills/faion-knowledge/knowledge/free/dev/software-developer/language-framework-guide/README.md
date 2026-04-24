# Language & Framework Selection Guide

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

## Quick Commands

### Python

```bash
# Format
black src/ && isort src/

# Test
pytest --cov=src
```

### JavaScript/TypeScript

```bash
# Format
prettier --write .

# Lint
eslint . --fix

# Test
vitest run --coverage
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
