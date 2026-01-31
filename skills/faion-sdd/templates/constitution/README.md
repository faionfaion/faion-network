# Constitution Template

Copy and customize for your project. Remove sections that don't apply.

---

```markdown
---
version: "1.0"
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
project: {project-name}
---

# Constitution: {Project Name}

## Vision

{1-2 sentences: what is this project and why does it exist}

---

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | {lang} | {ver} | {why chosen} |
| Framework | {framework} | {ver} | {why chosen} |
| Database | {db} | {ver} | {why chosen} |
| Cache | {cache} | {ver} | {why chosen} |
| Hosting | {platform} | - | {why chosen} |
| CI/CD | {tool} | - | {why chosen} |

---

## Architecture

### Patterns

| Pattern | Scope | Description |
|---------|-------|-------------|
| {pattern} | {where used} | {brief explanation} |

### Directory Structure

```
{project}/
├── {folder}/         # {purpose}
│   ├── {subfolder}/  # {purpose}
│   └── {subfolder}/  # {purpose}
├── {folder}/         # {purpose}
└── {folder}/         # {purpose}
```

### Key Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| {name} | {path} | {what it does} |

---

## Code Standards

### Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Files | {convention} | {example} |
| Classes | {convention} | {example} |
| Functions | {convention} | {example} |
| Variables | {convention} | {example} |
| Constants | {convention} | {example} |

### Formatting

| Tool | Config | Purpose |
|------|--------|---------|
| Formatter | {tool} ({config path}) | {auto-format} |
| Linter | {tool} ({config path}) | {code quality} |

### Import Order

```
1. {category} (e.g., stdlib)
2. {category} (e.g., third-party)
3. {category} (e.g., local)
```

---

## Testing

### Strategy

| Level | Framework | Coverage Target | Location |
|-------|-----------|-----------------|----------|
| Unit | {framework} | {X}% | {path} |
| Integration | {framework} | {X}% | {path} |
| E2E | {framework} | Critical paths | {path} |

### Commands

```bash
# Run all tests
{command}

# Run with coverage
{command}

# Run specific test
{command}
```

---

## Git Workflow

### Branch Strategy

| Branch | Purpose | Naming |
|--------|---------|--------|
| main | Production | - |
| develop | Integration | - |
| feature | New features | `feature/{description}` |
| fix | Bug fixes | `fix/{description}` |

### Commit Format

```
{type}: {short description}

{optional body}
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Requirements

- [ ] Tests pass
- [ ] Linter passes
- [ ] Coverage maintained
- [ ] Documentation updated

---

## Quality Gates

| Gate | Criteria | When | Blocks |
|------|----------|------|--------|
| Lint | Zero errors | Pre-commit | Commit |
| Types | Zero errors | Pre-commit | Commit |
| Unit Tests | 100% pass | Pre-push | Push |
| Coverage | >{X}% | Pre-merge | Merge |
| Security | No critical | Pre-deploy | Deploy |

---

## Dependencies

### Adding Dependencies

1. Check license compatibility
2. Evaluate maintenance status (last update, issues)
3. Consider bundle size impact
4. Document in this file if significant

### Pinned Versions

| Package | Version | Reason for Pin |
|---------|---------|----------------|
| {package} | {ver} | {reason} |

---

## Security

### Secrets Management

- **Never commit secrets** to repository
- Use environment variables or secret manager
- Required secrets documented in `.env.example`

### Authentication

| Method | Used For |
|--------|----------|
| {method} | {scope} |

---

## Deployment

### Environments

| Environment | URL | Branch | Auto-deploy |
|-------------|-----|--------|-------------|
| Production | {url} | main | {yes/no} |
| Staging | {url} | develop | {yes/no} |
| Development | localhost | - | - |

### Deploy Commands

```bash
# Deploy to staging
{command}

# Deploy to production
{command}
```

---

## Principles

1. **{Principle 1}** - {explanation}
2. **{Principle 2}** - {explanation}
3. **{Principle 3}** - {explanation}

---

## Constraints

### Technical

- {Constraint 1}
- {Constraint 2}

### Business

- {Constraint 1}
- {Constraint 2}

---

## Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| {pattern} | {why forbidden} | {what to use instead} |

---

## Related Documents

| Document | Path |
|----------|------|
| Roadmap | `.aidocs/roadmap.md` |
| API Docs | `{path}` |

---

*Constitution v1.0*
*Last updated: YYYY-MM-DD*
```

---

## Usage Notes

### When to Create

Create constitution.md when:
- Starting a new project
- Onboarding a new team member
- Introducing LLM assistance to existing project

### When to Update

Update when:
- Adding/changing major technology
- Establishing new conventions
- Learning from repeated mistakes

### LLM Context

Constitution is always loaded into context when executing tasks. Keep it concise but complete. Target: 2-5k tokens.
