# direnv + mise Version Management

## Summary

Per-project environment management on Ubuntu 24.04 with direnv (auto-loads .envrc on directory entry) and mise (polyglot runtime manager replacing pyenv/nvm/asdf). Key pattern: `use mise` + `layout python-venv .venv` in .envrc auto-activates the correct Python version and virtualenv when entering a project directory. Shell integration order is critical: mise hook must come BEFORE direnv hook in .bashrc.

## Why

Servers running multiple Python projects need isolated runtimes — Python 3.11 for one project, 3.12 for another, without manual `source .venv/bin/activate`. direnv automates activation and de-activation on directory change. mise replaces three separate tools (pyenv, nvm, asdf) with one binary and integrates cleanly with direnv via `use mise`.

## When To Use

- Multiple Python/Node projects on the same server needing different runtime versions
- Automatically activating virtualenvs when entering project directories
- Loading project-specific .env variables securely without shell leakage
- Setting up a new development server with reproducible runtime environments

## When NOT To Use

- Single-project servers where a single system Python or one venv is sufficient
- Managed platforms (Heroku, Railway) that provide runtime isolation at the container level
- When the project already uses Docker for isolation — runtime pinning is handled in the image
- Production systemd services — pin the venv path explicitly in ExecStart, don't rely on direnv

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | direnv trust model, mise as asdf replacement, activation order, .envrc stdlib functions |
| `content/02-configuration.xml` | .bashrc integration order, .envrc patterns (dotenv, layout, use mise, PATH_add), .tool-versions vs mise.toml |
| `content/03-examples.xml` | NERO multi-version Python setup, full project .envrc, troubleshooting wrong version |

## Templates

| File | Purpose |
|------|---------|
| `templates/bashrc-integration.sh` | Shell hook lines for .bashrc: mise activate before direnv hook |
| `templates/envrc-python-project` | Full .envrc for Python project: use mise, layout python-venv, dotenv, watch_file |
| `templates/envrc-node-project` | .envrc for Node project: use mise, layout node, dotenv |
| `templates/tool-versions` | .tool-versions example: python + node pinned versions |
| `templates/mise.toml` | mise-native config with tools, env vars, and task definitions |
| `templates/gitignore-additions` | .gitignore entries for .direnv/, .venv/, .mise.local.toml |
