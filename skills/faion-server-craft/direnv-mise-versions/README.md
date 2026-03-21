# direnv + mise Version Management

## Overview

Per-project environment and runtime version management using direnv (automatic .envrc loading) and mise (modern asdf replacement). Covers automatic venv activation, per-directory environment variables, Python/Node version pinning, .tool-versions files, trusted directories, and shell integration. Essential for servers hosting multiple projects with different runtime requirements.

**Target:** Ubuntu 24.04 VPS running multiple Python/Node projects with different version needs.

## When to Use

| Scenario | Fit |
|----------|-----|
| Multiple Python projects needing different versions | Essential |
| Auto-activating virtualenvs when entering project dirs | Essential |
| Loading project-specific .env automatically | Recommended |
| Managing Node.js versions for frontend builds | Recommended |
| Consistent dev/prod runtime versions | Recommended |
| Replacing pyenv + nvm with a single tool | Good |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **direnv** | Shell extension that loads/unloads .envrc when you enter/leave a directory |
| **mise** | Polyglot runtime manager (Python, Node, Ruby, Go, etc.), replaces asdf/pyenv/nvm |
| **.envrc** | Per-directory environment configuration file for direnv |
| **.tool-versions** | File specifying runtime versions (mise/asdf compatible) |
| **mise.toml** | Mise-native config file (alternative to .tool-versions) |
| **layout python** | direnv command that auto-creates and activates a Python venv |
| **Trusted directories** | direnv security: .envrc must be explicitly allowed before execution |

## direnv

### Installation

```bash
# Ubuntu 24.04
sudo apt install direnv

# Or latest version via binary
curl -sfL https://direnv.net/install.sh | bash
```

### Shell Integration

```bash
# For bash (~/.bashrc) - MUST be at the end of the file
eval "$(direnv hook bash)"

# For zsh (~/.zshrc)
eval "$(direnv hook zsh)"
```

### .envrc Patterns

#### Basic: Load Environment Variables

```bash
# .envrc
dotenv                          # Load .env file from current dir
dotenv_if_exists .env.local     # Load if exists, no error if missing
```

#### Python: Auto-activate Virtualenv

```bash
# .envrc
layout python python3.12        # Create .direnv/python-3.12 venv and activate
# OR
layout python-venv .venv        # Use specific venv directory
```

#### Full Project .envrc

```bash
# .envrc - Full project setup
# Load mise runtimes
use mise

# Activate Python virtualenv
layout python-venv .venv

# Load environment variables
dotenv_if_exists .env

# Add local bin to PATH
PATH_add bin
PATH_add scripts

# Project-specific variables (non-secret)
export PROJECT_NAME=nero-core
export LOG_LEVEL=DEBUG
```

### Trust Model

direnv requires explicit trust for each .envrc file. This prevents malicious .envrc from executing arbitrary code when you `cd` into a directory.

```bash
# Allow .envrc in current directory
direnv allow

# Deny (block) .envrc
direnv deny

# Re-allow after editing .envrc
direnv allow

# Check status
direnv status
```

### direnv stdlib Functions

| Function | Description |
|----------|-------------|
| `dotenv` | Load .env file |
| `dotenv_if_exists` | Load .env if it exists |
| `layout python` | Create and activate Python venv |
| `layout python-venv DIR` | Use specific venv directory |
| `layout node` | Setup Node.js environment |
| `PATH_add DIR` | Prepend to PATH |
| `path_add VAR DIR` | Prepend to any variable |
| `use mise` | Activate mise-managed runtimes |
| `source_env FILE` | Source another envrc file |
| `watch_file FILE` | Reload when file changes |
| `log_status MSG` | Print status message |

## mise (Modern asdf Replacement)

### Installation

```bash
# Official installer
curl https://mise.run | sh

# Or via apt
sudo apt install -y gpg
wget -qO - https://mise.jdx.dev/gpg-key.pub | \
  gpg --dearmor | sudo tee /usr/share/keyrings/mise-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/mise-archive-keyring.gpg arch=amd64] https://mise.jdx.dev/deb stable main" | \
  sudo tee /etc/apt/sources.list.d/mise.list
sudo apt update && sudo apt install -y mise
```

### Shell Integration

```bash
# For bash (~/.bashrc) - before direnv hook
eval "$(mise activate bash)"

# For zsh (~/.zshrc)
eval "$(mise activate zsh)"
```

### Managing Runtimes

```bash
# List available Python versions
mise ls-remote python

# Install specific Python version
mise install python@3.12.8

# Set global default
mise use --global python@3.12.8

# Set project-local version (creates .tool-versions)
mise use python@3.12.8

# Install Node.js
mise install node@22.12.0
mise use node@22.12.0

# List installed runtimes
mise ls

# Show current active versions
mise current
```

### .tool-versions File

```
# .tool-versions - compatible with asdf
python 3.12.8
node 22.12.0
```

### mise.toml (Native Config)

```toml
# mise.toml - mise-native format, more features

[tools]
python = "3.12.8"
node = "22.12.0"

[env]
PROJECT_NAME = "nero-core"

[tasks.lint]
run = "ruff check ."

[tasks.test]
run = "pytest"
```

## Integration: direnv + mise Together

### Recommended Setup Order

1. Install mise
2. Install direnv
3. Shell integration: mise hook BEFORE direnv hook
4. Per-project: mise.toml or .tool-versions for versions
5. Per-project: .envrc for environment activation

### .bashrc Order

```bash
# ~/.bashrc (relevant section)

# 1. mise activation (manages runtime versions)
eval "$(mise activate bash)"

# 2. direnv hook (loads per-directory .envrc)
# MUST be LAST in .bashrc
eval "$(direnv hook bash)"
```

### Complete .envrc for a Python Project

```bash
# .envrc

# Load mise-managed runtime versions
use mise

# Create/activate virtualenv with mise-managed Python
layout python-venv .venv

# Load secrets from .env file
dotenv_if_exists .env

# Reload when these files change
watch_file requirements.txt
watch_file pyproject.toml

# Project PATH additions
PATH_add scripts

# Non-secret project config
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
```

## Multi-Version Python Setup

### Scenario: Different Projects Need Different Python Versions

```
~/workspace/repos/nero-core/       # Python 3.12
~/workspace/repos/nero-channel-tg/ # Python 3.12
~/projects/meetingtax/be/          # Python 3.11
~/projects/eulaguard/              # Python 3.12
```

```bash
# Install multiple versions
mise install python@3.11.11
mise install python@3.12.8

# Set per-project
cd ~/workspace/repos/nero-core
mise use python@3.12.8       # Creates .tool-versions

cd ~/projects/meetingtax/be
mise use python@3.11.11      # Creates .tool-versions

# Global fallback
mise use --global python@3.12.8
```

## Security Considerations

| Concern | Mitigation |
|---------|-----------|
| .envrc runs arbitrary code | direnv trust model: must `direnv allow` explicitly |
| .env in git | .envrc loads .env, but .env is in .gitignore |
| Cloned repo with .envrc | direnv blocks until you `direnv allow` |
| mise installs from internet | Verify checksums, use `mise self-update` |
| Venv in git | Add `.direnv/` and `.venv/` to .gitignore |

### .gitignore Additions

```gitignore
# direnv
.direnv/
.envrc.local

# mise
.mise.local.toml

# Python virtualenv
.venv/
venv/
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| direnv: not hooked | Ensure `eval "$(direnv hook bash)"` is in .bashrc |
| .envrc is not allowed | Run `direnv allow` in the directory |
| mise: command not found | Ensure `eval "$(mise activate bash)"` in .bashrc |
| Wrong Python version | Check `mise current`, run `mise use python@X.Y.Z` |
| Venv not activating | Check `.envrc` has `layout python-venv .venv` |
| Changes not loading | Run `direnv reload` or re-enter the directory |

## Related Methodologies

| Methodology | Relationship |
|-------------|-------------|
| [secrets-management](../secrets-management/) | .envrc loads .env for secrets |
| [server-init-bootstrap](../server-init-bootstrap/) | Install mise + direnv during bootstrap |
| [deploy-scripts](../deploy-scripts/) | Deploy uses pinned runtime versions |
| [dotfiles-management](../dotfiles-management/) | Shell hooks in dotfiles |
