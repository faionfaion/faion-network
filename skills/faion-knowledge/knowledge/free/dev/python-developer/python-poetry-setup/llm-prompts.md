# LLM Prompts for Poetry

Effective prompts for LLM-assisted Python dependency management.

---

## Project Setup Prompts

### Create New Project

```
Create a pyproject.toml for a [FastAPI/Django/CLI/Library] project using Poetry 2.x:

Requirements:
- Python version: 3.12
- Main dependencies: [list your dependencies]
- Dev dependencies: pytest, mypy, ruff
- Optional docs group: mkdocs

Include:
- PEP 621 compliant [project] section
- Proper build-system configuration
- Ruff, mypy, pytest, coverage configs
- Appropriate classifiers for [PyPI/internal use]
```

### Migrate to Poetry 2.x

```
Migrate this pyproject.toml from Poetry 1.x to Poetry 2.x format:

[paste your current pyproject.toml]

Requirements:
- Convert tool.poetry.dependencies to project.dependencies (PEP 508)
- Use [project] section for metadata (PEP 621)
- Keep dev/test groups in tool.poetry.group
- Update build-system to poetry-core>=2.0.0
- Preserve all functionality
```

### Add Feature Dependencies

```
I'm adding [authentication/caching/async tasks/etc.] to my Python project.

Current pyproject.toml:
[paste relevant sections]

Recommend:
1. Best packages for this feature (2025-2026)
2. Poetry add commands
3. Version constraints (compatible with existing deps)
4. Any optional extras needed
5. Config changes if required
```

---

## Dependency Management Prompts

### Resolve Conflicts

```
I'm getting dependency conflicts with Poetry:

Error message:
[paste error]

Current pyproject.toml dependencies:
[paste dependencies section]

Help me:
1. Understand the conflict
2. Find compatible versions
3. Suggest version constraints to resolve
4. Identify which package to pin/relax
```

### Audit Dependencies

```
Audit my Python project dependencies:

[paste pyproject.toml]

Check for:
1. Outdated packages (major updates available)
2. Security concerns (known vulnerabilities)
3. Redundant dependencies
4. Missing dev dependencies (testing, linting, typing)
5. Packages with better alternatives
6. Proper version constraints (not too loose/tight)
```

### Optimize Lock File

```
My poetry.lock is getting large and installs are slow.

Dependencies:
[paste project.dependencies section]

Help me:
1. Identify heavy dependencies
2. Find lighter alternatives
3. Check for unnecessary transitive dependencies
4. Suggest optional extras instead of full packages
```

---

## Configuration Prompts

### Setup Tool Configs

```
Add tool configurations to my pyproject.toml:

Project type: [FastAPI API / Django app / CLI tool / Library]
Python version: 3.12
Style: [strict / moderate / minimal]

Include configs for:
- Ruff (linting + formatting)
- MyPy (strict mode with [pydantic/django/etc.] plugin)
- Pytest (with [asyncio/django/etc.])
- Coverage (minimum [80/90]%)
```

### Setup CI/CD

```
Create GitHub Actions workflow for my Poetry project:

Requirements:
- Python versions: 3.11, 3.12
- Run: lint, type check, tests with coverage
- Cache Poetry dependencies
- [Optional: publish to PyPI on tags]

My project uses:
- Poetry 2.x
- [pytest-asyncio / pytest-django / etc.]
- [Additional requirements]
```

### Setup Docker

```
Create Dockerfile for my Poetry project:

Type: [multi-stage production / development]
Base image: python:3.12-slim
Application: [FastAPI / Django / CLI / etc.]

Requirements:
- Fast builds with caching
- Small final image
- Non-root user
- [Additional requirements]
```

---

## Troubleshooting Prompts

### Debug Installation Issues

```
Poetry install is failing:

Error:
[paste full error]

Environment:
- OS: [Ubuntu/macOS/Windows]
- Python: [version]
- Poetry: [version]

pyproject.toml:
[paste file]

What's wrong and how to fix it?
```

### Fix Lock File Issues

```
My poetry.lock seems corrupted or out of sync:

Symptoms:
[describe the issue]

I've tried:
- poetry lock
- poetry install

pyproject.toml:
[paste file]

How do I regenerate a clean lock file?
```

### Virtual Environment Issues

```
Poetry virtual environment problems:

Issue:
[describe - wrong Python, can't activate, missing packages, etc.]

Environment info:
[paste output of: poetry env info]

Configuration:
[paste output of: poetry config --list]

How do I fix this?
```

---

## Publishing Prompts

### Prepare for PyPI

```
Review my library's pyproject.toml before publishing to PyPI:

[paste pyproject.toml]

Check:
1. Required metadata (name, version, description, readme)
2. Author/maintainer info
3. License specification
4. Python version range (wide enough?)
5. Classifiers (appropriate?)
6. URLs (homepage, docs, repo)
7. Package includes (src layout?)
8. Entry points (if CLI)
```

### Private Registry Setup

```
Configure Poetry for a private PyPI registry:

Registry URL: [your registry URL]
Authentication: [token / basic auth]

I need:
1. poetry config commands
2. pyproject.toml source configuration
3. CI/CD environment variable setup
4. Authentication best practices
```

---

## Monorepo Prompts

### Setup Monorepo

```
Setup a Python monorepo with Poetry:

Structure:
- packages/shared-lib (common code)
- services/api (FastAPI)
- services/worker (Celery)

Requirements:
- Shared lock file (or separate?)
- Local path dependencies
- Single dev environment
- Independent versioning

Recommend:
1. Directory structure
2. Root pyproject.toml
3. Package pyproject.toml templates
4. Which monorepo plugin to use (if any)
```

### Add Package to Monorepo

```
Add a new package to my Poetry monorepo:

Current structure:
[paste tree output]

New package:
- Name: [package-name]
- Type: [library / service / cli]
- Depends on: [existing packages]

Generate:
1. Directory structure
2. pyproject.toml
3. Updates to root pyproject.toml
```

---

## Migration Prompts

### From pip/requirements.txt

```
Migrate from requirements.txt to Poetry:

requirements.txt:
[paste file]

requirements-dev.txt:
[paste file if exists]

Project info:
- Name: [project-name]
- Python version: [version]
- Type: [app/library]

Generate complete pyproject.toml with:
- All dependencies with proper version constraints
- Appropriate dependency groups
- Tool configs (ruff, mypy, pytest)
```

### From Pipenv

```
Migrate from Pipenv to Poetry:

Pipfile:
[paste file]

Pipfile.lock (partial):
[paste if relevant]

Generate:
1. pyproject.toml
2. Migration commands
3. Differences to be aware of
```

### To uv

```
I want to migrate from Poetry to uv:

Current pyproject.toml:
[paste file]

Help me:
1. Understand key differences
2. Convert pyproject.toml format
3. Migrate lock file (poetry.lock -> uv.lock)
4. Update CI/CD workflows
5. Things that work differently in uv
```

---

## Best Practice Prompts

### Code Review

```
Review my pyproject.toml for best practices:

[paste pyproject.toml]

Check:
1. Poetry 2.x / PEP 621 compliance
2. Version constraint style
3. Dependency organization
4. Tool config completeness
5. Missing recommended configs
6. Security considerations
```

### Version Constraints

```
Help me set proper version constraints:

Dependencies:
[list your key dependencies]

Project stability: [experimental / production / library]

For each dependency, recommend:
1. Version constraint style (^ ~ >= ==)
2. Specific constraint
3. Reasoning
```

---

## Quick Reference Prompts

### Command Help

```
What's the Poetry command to:
[describe what you want to do]

Include:
- Full command syntax
- Common options
- Example usage
```

### Compare Options

```
Compare these Python packaging options for my use case:

Use case: [describe project]
Requirements: [list key requirements]

Compare:
- Poetry 2.x
- uv
- PDM
- pip + pip-tools

For each, provide:
1. Pros/cons for my use case
2. Setup complexity
3. CI/CD considerations
4. Team adoption ease
```

---

## Prompt Templates with Context

### Full Context Template

```
[CONTEXT]
Project: [name and description]
Type: [application / library / cli / monorepo]
Python: [version]
Poetry: [version]
CI/CD: [GitHub Actions / GitLab CI / etc.]

Current pyproject.toml:
```toml
[paste file]
```

Current issue/goal:
[describe what you're trying to do]

[REQUEST]
[specific ask]

[CONSTRAINTS]
- [any constraints or preferences]
```

### Minimal Context Template

```
Poetry 2.x, Python 3.12, [FastAPI/Django/etc.]

[paste relevant pyproject.toml section]

Question: [your question]
```

---

## Anti-patterns to Avoid

When prompting LLMs about Poetry, avoid:

1. **Asking to edit poetry.lock directly**
   - Lock files are auto-generated
   - Use `poetry lock` to regenerate

2. **Mixing pip and Poetry**
   - Don't ask for `pip install` alongside Poetry
   - Use `poetry add` for all dependencies

3. **Skipping version context**
   - Always specify Poetry 1.x vs 2.x
   - PEP 621 syntax differs significantly

4. **Forgetting environment**
   - Specify OS if relevant
   - Include Python version
   - Mention if Docker/CI environment

5. **Incomplete error context**
   - Include full error messages
   - Show relevant pyproject.toml sections
   - Mention what you've already tried

---

*Last updated: 2026-01*
