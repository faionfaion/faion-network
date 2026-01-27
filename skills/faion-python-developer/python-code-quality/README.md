# Python Code Quality

**Ruff, mypy/pyright, pre-commit hooks, SOLID principles, clean code patterns**

---

## Overview

Modern Python code quality in 2025-2026 centers on a streamlined toolchain that replaces the traditional Black + isort + flake8 stack with **Ruff** - an all-in-one linter and formatter written in Rust that runs 10-100x faster.

### Modern Stack (2025-2026)

| Tool | Purpose | Replaces |
|------|---------|----------|
| **Ruff** | Linting + formatting | flake8, black, isort, pyupgrade, autoflake, pydocstyle |
| **mypy/pyright** | Type checking | - |
| **pre-commit** | Git hooks | manual linting |
| **pytest + coverage** | Testing + coverage | - |
| **bandit** | Security scanning | - |

### Why Ruff?

- **Speed**: 10-100x faster than traditional tools (written in Rust)
- **800+ rules**: Native re-implementations of flake8-bugbear, pyupgrade, isort, etc.
- **Single config**: One `pyproject.toml` section replaces multiple config files
- **Adoption**: Used by FastAPI, pandas, pydantic, Apache Airflow

### Type Checkers: mypy vs pyright

| Aspect | mypy | pyright |
|--------|------|---------|
| Speed | Slower (~5s on large files) | Faster (~50ms on large files) |
| Strictness | Configurable | More strict by default |
| IDE integration | Good | Excellent (VS Code, Pylance) |
| Best for | CI/CD, large codebases | IDE, iterative development |

**Recommendation**: Use **Ruff + mypy** for CI/CD pipelines. Pyright edges ahead in IDE environments and ML prototyping due to speed.

---

## Quick Start

### 1. Install Tools

```bash
# Using uv (recommended)
uv add --dev ruff mypy pytest pytest-cov pre-commit bandit

# Using pip
pip install ruff mypy pytest pytest-cov pre-commit bandit
```

### 2. Initialize Configuration

```bash
# Create pyproject.toml with Ruff + mypy config
# See templates.md for complete configurations

# Install pre-commit hooks
pre-commit install
```

### 3. Run Checks

```bash
# Lint and format
ruff check src/
ruff format src/

# Type check
mypy src/

# Run all via pre-commit
pre-commit run --all-files
```

---

## Core Concepts

### SOLID Principles in Python

| Principle | Description | Python Pattern |
|-----------|-------------|----------------|
| **S**ingle Responsibility | One class = one responsibility | Small, focused modules |
| **O**pen/Closed | Open for extension, closed for modification | ABCs, protocols, composition |
| **L**iskov Substitution | Subtypes must be substitutable | Proper inheritance hierarchies |
| **I**nterface Segregation | Many specific interfaces > one general | Protocols, ABCs |
| **D**ependency Inversion | Depend on abstractions | Dependency injection, protocols |

### Clean Code Patterns

1. **Meaningful names**: `calculate_total_price()` not `calc()`
2. **Small functions**: Max 20-30 lines, single purpose
3. **No magic numbers**: Use named constants
4. **Early returns**: Reduce nesting with guard clauses
5. **Type hints**: Always use for public APIs
6. **Docstrings**: Follow Google/NumPy style consistently

### Code Smells to Avoid

- **Long functions** (>50 lines)
- **Deep nesting** (>3 levels)
- **God classes** (too many responsibilities)
- **Primitive obsession** (use dataclasses/models)
- **Feature envy** (method uses other class's data excessively)
- **Dead code** (unused imports, functions)

---

## LLM Usage Tips

### When to Use AI Code Review

| Use Case | Effectiveness |
|----------|---------------|
| Style/formatting issues | High |
| Common bug patterns | High |
| Type hint suggestions | High |
| Security vulnerabilities | Medium |
| Architecture decisions | Low (needs context) |
| Business logic validation | Low |

### Best Practices for LLM-Assisted Review

1. **Provide context**: Include relevant files, constraints, project conventions
2. **Human-in-the-loop**: AI suggests, human decides
3. **Verify suggestions**: Don't blindly accept AI fixes
4. **Use for education**: Learn from AI explanations
5. **Combine with static analysis**: AI + Ruff + mypy = comprehensive coverage

### Warning Signs

- PRs getting larger without proportional review time
- Over-reliance on automated reviews
- Accepting "technically correct but contextually wrong" suggestions

---

## Documentation Standards

### Docstring Formats

| Format | Best For |
|--------|----------|
| **Google style** | Most projects, readable |
| **NumPy style** | Scientific/data projects |
| **Sphinx style** | Complex API documentation |

### What to Document

- **All public functions/classes/modules**
- Parameters with types and descriptions
- Return values
- Exceptions raised
- Usage examples (can double as doctests)

---

## CI/CD Integration

### Quality Gates

| Gate | Tool | Threshold |
|------|------|-----------|
| Linting | Ruff | Zero errors |
| Type checking | mypy | Zero errors |
| Test coverage | pytest-cov | >80% |
| Security | bandit | No high/critical |
| Complexity | Ruff (C901) | <10 cyclomatic |

### GitHub Actions Workflow

See `templates.md` for complete workflow configurations with:
- Multi-Python version testing
- Coverage reports on PRs
- Security scanning
- Pre-commit hooks in CI

---

## File Structure

| File | Content |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Step-by-step code quality checklist |
| [examples.md](examples.md) | Real code quality examples |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | Effective LLM code review prompts |

---

## External Resources

### Official Documentation

- [Ruff Documentation](https://docs.astral.sh/ruff/) - Linter + formatter
- [mypy Documentation](https://mypy.readthedocs.io/) - Type checker
- [pyright Documentation](https://microsoft.github.io/pyright/) - Type checker
- [pre-commit Framework](https://pre-commit.com/) - Git hook management
- [pytest Documentation](https://docs.pytest.org/) - Testing framework

### Style Guides

- [PEP 8](https://peps.python.org/pep-0008/) - Python style guide
- [PEP 257](https://peps.python.org/pep-0257/) - Docstring conventions
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Learning Resources

- [Real Python - SOLID Principles](https://realpython.com/solid-principles-python/)
- [Clean Code in Python](https://www.oreilly.com/library/view/clean-code-in/9781788835831/)
- [Python Design Patterns for Clean Architecture](https://www.glukhov.org/post/2025/11/python-design-patterns-for-clean-architecture/)

### Tools & Extensions

- [Ruff VS Code Extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) - Pyright for VS Code
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage plugin
- [Codecov](https://about.codecov.io/) - Coverage reporting service

### AI-Assisted Code Review

- [CodeDog](https://github.com/codedog-ai/codedog) - LLM-powered code review
- [Addy Osmani's LLM Coding Workflow](https://addyosmani.com/blog/ai-coding-workflow/)
- [Code Review in the Age of AI](https://addyo.substack.com/p/code-review-in-the-age-of-ai)

---

## Agent

Executed by: faion-python-developer, faion-code-quality, faion-devops-engineer
