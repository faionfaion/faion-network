<!--
purpose: Project constitution — vision, tech stack, architecture patterns, code standards, git workflow, project structure, quality gates, principles.
consumes: nothing — canonical SDD constitution skeleton, filled directly by the author at project onboarding
produces: constitution artefact (canonical SDD template; this methodology's own content/02-output-contract.xml is an unfilled migration stub, so conformance to it cannot be claimed)
depends-on: nothing
token-budget-impact: ~500-800 tokens when loaded as context
-->

# Constitution: <project_name>

**Version:** 1.0
**Created:** YYYY-MM-DD
**Status:** Active

## Vision

{1-2 sentences: what is this project and why does it exist}

## Tech Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Language | <lang> | {ver} | {why} |
| Framework | {framework} | {ver} | {why} |
| Database | <db> | {ver} | {why} |
| Hosting | <platform> | - | {why} |

## Architecture Patterns

| Pattern | Description |
|---------|-------------|
| <pattern> | <brief_explanation> |

## Code Standards

### Naming Conventions
- Files: `{convention}`
- Classes: `{convention}`
- Functions: `{convention}`
- Variables: `{convention}`

### Formatting
- Formatter: <tool>
- Linter: <tool>
- Config: <location>

### Testing
- Framework: {framework}
- Coverage target: {X}%
- Test location: <path>

## Git Workflow

- Branch strategy: <strategy>
- Commit format: `{format}`
- PR requirements: <requirements>

## Project Structure

```
{project}/
├── {folder}/     # {purpose}
├── {folder}/     # {purpose}
└── {folder}/     # {purpose}
```

## Quality Gates

| Gate | Criteria | When |
|------|----------|------|
| Lint | Zero errors | Pre-commit |
| Types | Zero errors | Pre-commit |
| Tests | 100% pass | Pre-push |
| Coverage | >{X}% | Pre-merge |

## Principles

1. <principle_1>
2. <principle_2>
3. <principle_3>
