# direnv + mise Templates

## .envrc: Python Project with venv

Basic Python project with automatic virtualenv activation.

```bash
# .envrc - Python project
# Run `direnv allow` after creating or editing this file

# Activate mise-managed runtime versions
use mise

# Create and activate Python virtualenv in .venv/
layout python-venv .venv

# Load environment variables from .env (if exists)
dotenv_if_exists .env

# Reload when dependency files change
watch_file requirements.txt
watch_file pyproject.toml

# Python settings
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
```

## .envrc: Full Project (Python + Secrets + Scripts)

Complete project setup with all common features.

```bash
# .envrc - Full project environment
# Run `direnv allow` after creating or editing this file

# ============================================================
# Runtime versions (from .tool-versions or mise.toml)
# ============================================================
use mise

# ============================================================
# Python virtualenv
# ============================================================
layout python-venv .venv

# ============================================================
# Environment variables
# ============================================================
# Load secrets (never committed to git)
dotenv_if_exists .env

# Load local overrides (developer-specific, never committed)
dotenv_if_exists .env.local

# ============================================================
# PATH additions
# ============================================================
PATH_add bin
PATH_add scripts

# ============================================================
# Reload triggers
# ============================================================
watch_file requirements.txt
watch_file pyproject.toml
watch_file .tool-versions

# ============================================================
# Non-secret project config
# ============================================================
export PROJECT_NAME=nero-core
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export LOG_LEVEL="${LOG_LEVEL:-DEBUG}"

# Status message
log_status "Project: $PROJECT_NAME | Python: $(python --version 2>&1 | cut -d' ' -f2) | venv: .venv"
```

## .envrc: Node.js Project

```bash
# .envrc - Node.js project
use mise

# Load environment
dotenv_if_exists .env

# Add local node_modules/.bin to PATH
PATH_add node_modules/.bin

# Reload triggers
watch_file package.json
watch_file package-lock.json

export NODE_ENV="${NODE_ENV:-development}"
```

## .envrc: Multi-Runtime Project (Python + Node)

```bash
# .envrc - Full-stack project (Python backend + Node frontend)
use mise

# Python virtualenv for backend
layout python-venv .venv

# Node.js binaries
PATH_add node_modules/.bin

# Load environment
dotenv_if_exists .env

# Reload triggers
watch_file requirements.txt
watch_file pyproject.toml
watch_file package.json
watch_file .tool-versions

export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export NODE_ENV="${NODE_ENV:-development}"

log_status "Python: $(python --version 2>&1 | cut -d' ' -f2) | Node: $(node --version 2>&1)"
```

## .envrc: Workspace Root (Load Master .env)

For the workspace root that loads the master .env for all projects.

```bash
# ~/workspace/.envrc - Workspace root
# Loads master .env so all sub-projects inherit secrets

dotenv_if_exists .env

# Don't set up runtimes here - let sub-projects handle that
log_status "Workspace env loaded ($(wc -l < .env 2>/dev/null || echo 0) vars)"
```

## .tool-versions

```
# .tool-versions - Runtime versions (mise/asdf compatible)
python 3.12.8
node 22.12.0
```

## mise.toml (Native Config)

```toml
# mise.toml - mise native configuration

[tools]
python = "3.12.8"
# node = "22.12.0"  # Uncomment if needed

[env]
# Non-secret project variables
PYTHONDONTWRITEBYTECODE = "1"
PYTHONUNBUFFERED = "1"

# Tasks (run with `mise run <task>`)
[tasks.lint]
run = "ruff check ."
description = "Run linter"

[tasks.format]
run = "ruff format ."
description = "Format code"

[tasks.test]
run = "pytest -x"
description = "Run tests"

[tasks.dev]
run = "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
description = "Run dev server"
```

## mise.toml: Global Config

```toml
# ~/.config/mise/config.toml - Global mise configuration

[tools]
python = "3.12.8"       # Global default Python
node = "22.12.0"        # Global default Node.js

[settings]
experimental = false
yes = true              # Auto-confirm tool installs
```

## Shell Integration (.bashrc additions)

```bash
# ~/.bashrc - mise + direnv integration
# Order matters: mise BEFORE direnv

# ============================================================
# mise: runtime version management
# ============================================================
if command -v mise &>/dev/null; then
    eval "$(mise activate bash)"
fi

# ============================================================
# direnv: per-directory environment
# MUST be LAST in .bashrc (or at least after mise)
# ============================================================
if command -v direnv &>/dev/null; then
    eval "$(direnv hook bash)"
fi
```

## install-mise-direnv.sh

Complete installation script for both tools.

```bash
#!/bin/bash
# install-mise-direnv.sh - Install mise and direnv
set -euo pipefail

echo "=== Installing mise ==="
if command -v mise &>/dev/null; then
    echo "mise already installed: $(mise --version)"
else
    curl https://mise.run | sh
    echo "mise installed"
fi

echo ""
echo "=== Installing direnv ==="
if command -v direnv &>/dev/null; then
    echo "direnv already installed: $(direnv --version)"
else
    sudo apt install -y direnv
    echo "direnv installed"
fi

echo ""
echo "=== Configuring shell integration ==="

BASHRC="$HOME/.bashrc"

# Add mise hook if not present
if ! grep -q 'mise activate' "$BASHRC"; then
    echo '' >> "$BASHRC"
    echo '# mise: runtime version management' >> "$BASHRC"
    echo 'if command -v mise &>/dev/null; then eval "$(mise activate bash)"; fi' >> "$BASHRC"
    echo "Added mise hook to $BASHRC"
else
    echo "mise hook already in $BASHRC"
fi

# Add direnv hook if not present (MUST be after mise)
if ! grep -q 'direnv hook' "$BASHRC"; then
    echo '' >> "$BASHRC"
    echo '# direnv: per-directory environment (MUST be last)' >> "$BASHRC"
    echo 'if command -v direnv &>/dev/null; then eval "$(direnv hook bash)"; fi' >> "$BASHRC"
    echo "Added direnv hook to $BASHRC"
else
    echo "direnv hook already in $BASHRC"
fi

echo ""
echo "=== Installing default runtimes ==="
# Source mise to use it immediately
eval "$(mise activate bash)"

mise install python@3.12
mise use --global python@3.12
echo "Python $(mise current python) installed as global default"

echo ""
echo "=== Done ==="
echo "Restart your shell: source ~/.bashrc"
echo "Then create .envrc and .tool-versions in your projects."
```

## .gitignore Additions

```gitignore
# direnv
.direnv/
.envrc.local

# mise
.mise.local.toml

# Python virtualenv
.venv/
venv/

# Environment files
.env
.env.local
.env.*.local
```
