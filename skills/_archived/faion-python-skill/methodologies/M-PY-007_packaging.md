# M-PY-007: Python Packaging

## Metadata
- **Category:** Development/Python
- **Difficulty:** Intermediate
- **Tags:** #dev, #python, #packaging, #methodology
- **Agent:** faion-code-agent

---

## Problem

Sharing Python code is confusing. Multiple packaging formats, different installation methods, and PyPI publishing quirks make distribution painful. You need a clear path from code to installable package.

## Promise

After this methodology, you will create professional Python packages that install cleanly, work reliably, and publish to PyPI with confidence.

## Overview

Modern Python packaging uses pyproject.toml for configuration, build backends for building, and twine for publishing.

---

## Framework

### Step 1: Package Structure

```
my-package/
├── pyproject.toml          # Package configuration
├── README.md               # Package description
├── LICENSE                 # License file
├── CHANGELOG.md            # Version history
├── src/                    # Source layout (recommended)
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── py.typed        # PEP 561 marker
├── tests/
│   ├── __init__.py
│   └── test_core.py
└── docs/
    └── index.md
```

### Step 2: pyproject.toml Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "you@example.com"},
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Typing :: Typed",
]
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "mypy>=1.8",
    "ruff>=0.1",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
]

[project.urls]
Homepage = "https://github.com/username/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/username/my-package.git"
Changelog = "https://github.com/username/my-package/blob/main/CHANGELOG.md"

[project.scripts]
my-cli = "my_package.cli:main"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins.plugin1:Plugin"
```

### Step 3: Package __init__.py

```python
# src/my_package/__init__.py
"""My Package - A short description."""

from my_package.core import main_function, MainClass
from my_package.utils import helper_function

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "main_function",
    "MainClass",
    "helper_function",
]
```

### Step 4: Build Package

```bash
# Install build tools
pip install build twine

# Build source and wheel distributions
python -m build

# Output in dist/
# my_package-0.1.0.tar.gz (source)
# my_package-0.1.0-py3-none-any.whl (wheel)

# Verify package
twine check dist/*
```

### Step 5: Test Installation

```bash
# Install in virtual environment
python -m venv test-env
source test-env/bin/activate

# Install from local wheel
pip install dist/my_package-0.1.0-py3-none-any.whl

# Test import
python -c "import my_package; print(my_package.__version__)"

# Install in editable mode for development
pip install -e ".[dev]"
```

### Step 6: Publish to PyPI

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ my-package

# Upload to PyPI
twine upload dist/*

# Or use trusted publishing (GitHub Actions)
```

### Step 7: GitHub Actions Publishing

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for trusted publishing

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - name: Install build tools
      run: pip install build

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      # No credentials needed with trusted publishing
```

### Step 8: Version Management

```toml
# pyproject.toml - Dynamic versioning with hatch
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_package/__init__.py"
```

```bash
# Bump version with hatch
hatch version minor  # 0.1.0 -> 0.2.0
hatch version patch  # 0.2.0 -> 0.2.1
hatch version major  # 0.2.1 -> 1.0.0
```

---

## Templates

### Minimal pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
requires-python = ">=3.10"
```

### CLI Entry Point

```python
# src/my_package/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="My CLI tool")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        print(f"Verbose mode enabled")
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
```

### Plugin System

```python
# src/my_package/plugins/__init__.py
from importlib.metadata import entry_points

def load_plugins():
    """Load all registered plugins."""
    eps = entry_points(group="my_package.plugins")
    return {ep.name: ep.load() for ep in eps}
```

### MANIFEST.in (if needed)

```
include LICENSE
include README.md
include CHANGELOG.md
recursive-include src/my_package *.pyi py.typed
recursive-include tests *.py
prune tests/__pycache__
```

---

## Examples

### Data Files

```toml
# pyproject.toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.hatch.build]
include = [
    "src/my_package/data/*.json",
    "src/my_package/templates/*.html",
]
```

```python
# Access data files
from importlib.resources import files

data = files("my_package").joinpath("data/config.json")
config = json.loads(data.read_text())
```

### Namespace Packages

```
# Multiple packages under same namespace
my-namespace-core/
└── src/
    └── my_namespace/
        └── core/
            └── __init__.py

my-namespace-utils/
└── src/
    └── my_namespace/
        └── utils/
            └── __init__.py
```

```toml
# pyproject.toml for namespace package
[tool.hatch.build.targets.wheel]
packages = ["src/my_namespace"]
```

---

## Common Mistakes

1. **Wrong package name** - Underscores in code, hyphens in PyPI name
2. **Missing py.typed** - Required for type hints in installed packages
3. **Hardcoded version** - Use dynamic versioning
4. **No MANIFEST.in** - Data files not included in sdist
5. **Wrong Python version** - Test on all supported versions

---

## Checklist

- [ ] pyproject.toml complete
- [ ] README.md with examples
- [ ] LICENSE file present
- [ ] CHANGELOG.md maintained
- [ ] py.typed marker for typed packages
- [ ] Tests pass
- [ ] Build succeeds locally
- [ ] TestPyPI upload successful
- [ ] GitHub Actions CI/CD configured
- [ ] Trusted publishing enabled

---

## Next Steps

- M-DO-001: CI/CD GitHub Actions
- M-PY-008: Code Quality

---

*Methodology M-PY-007 v1.0*
