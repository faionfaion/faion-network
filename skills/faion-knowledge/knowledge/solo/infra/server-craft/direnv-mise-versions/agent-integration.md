# Agent Integration — direnv + mise Version Management

## When to use
- Setting up a new project directory that needs isolated Python or Node version and virtualenv
- Onboarding a server that runs multiple projects with conflicting runtime requirements
- Replacing pyenv + nvm + manual venv activation with a single automated setup
- Ensuring the agent's shell environment matches the project's pinned versions before running dev commands
- Debugging "wrong Python version" or "venv not active" issues in CI or on the server

## When NOT to use
- Docker-based development environments — the container already isolates the runtime; adding direnv/mise adds complexity without benefit
- Servers where the runtime is installed system-wide and all projects use the same version — overhead is not justified
- One-off script execution — use explicit shebang (`#!/usr/bin/env python3.12`) instead
- CI/CD pipelines — use the CI system's built-in language version management (GitHub Actions `setup-python`, etc.)

## Where it fails / limitations
- direnv requires `direnv allow` after any `.envrc` change — agent cannot pre-trust directories in advance; human must run `direnv allow` once after agent creates or modifies `.envrc`
- Shell hook order matters: `eval "$(mise activate bash)"` must come before `eval "$(direnv hook bash)"` in `.bashrc`; wrong order causes mise runtimes to not be visible inside `.envrc`
- `layout python` creates a new venv on first run — if a `.venv` already exists with the wrong Python version, the layout command uses the existing one without error; agent must delete and recreate
- mise downloads runtimes from the internet on first `mise install` — air-gapped servers need a pre-populated mise cache or system-installed runtimes
- `use mise` in `.envrc` does not work if mise is not activated in the shell — on non-interactive shells (cron, systemd services), mise must be sourced explicitly

## Agentic workflow
An agent can read `.envrc` and `.tool-versions` / `mise.toml` to understand a project's runtime configuration, then verify that the versions are installed with `mise ls` and that direnv is loading correctly with `direnv status`. For new project setup, the agent writes the `.envrc` and `mise.toml` files, runs `mise install` to download the pinned runtimes, then instructs the user to run `direnv allow` (the only step requiring human interaction). For debugging, the agent checks `direnv status` and `mise current` to identify which versions are active.

### Recommended subagents
- `faion-sdd-executor-agent` — execute server bootstrap tasks that include runtime version setup as a step

### Prompt pattern
```
Set up direnv + mise for the project at ~/workspace/projects/myapp/backend.
Requirements:
- Python 3.12.8 (via mise)
- virtualenv in .venv directory (auto-activated by direnv)
- Load .env file if it exists
- Add scripts/ to PATH
Output: .tool-versions content, mise.toml content, and .envrc content.
Also list the commands to run after writing the files.
```

```
Debug why the Python version is wrong in the project at ~/projects/myapp.
Run:
1. `direnv status` — check if .envrc is loaded
2. `mise current` — show active runtimes
3. `python --version` — actual version in use
4. `which python` — which python binary is being used
Report: what is misconfigured and the exact commands to fix it.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `direnv` | Shell extension for per-directory environment | `apt install direnv` / [direnv.net](https://direnv.net/) |
| `mise` | Polyglot runtime manager (Python, Node, Ruby, Go, etc.) | `curl https://mise.run \| sh` / [mise.jdx.dev](https://mise.jdx.dev/) |
| `mise ls` | List installed runtimes | Built-in |
| `mise current` | Show active versions in current directory | Built-in |
| `direnv status` | Show direnv load status for current directory | Built-in |
| `direnv reload` | Force reload .envrc without re-entering directory | Built-in |
| `python -m venv` | Create virtualenv manually (fallback) | Built-in (Python) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| mise (jdx.dev) | OSS | Yes | CLI-driven; all operations are non-interactive; mirrors Python.org, nodejs.org for runtime downloads |
| python.org | Source | Partial | mise fetches from here; no API needed |
| asdf (legacy) | OSS | Yes | mise is a drop-in replacement; `.tool-versions` format is compatible |
| pyenv | OSS | Partial | Use only if mise cannot be installed; direnv integrates with both |

## Templates & scripts
See templates.md for full shell hook setup. Key complete `.envrc` for a Python API project:

```bash
# .envrc — Python API project
# After editing: run `direnv allow`

# 1. Load mise-managed runtime versions (.tool-versions or mise.toml)
use mise

# 2. Activate virtualenv (creates .venv with mise's Python if not exists)
layout python-venv .venv

# 3. Load secrets from .env file (gitignored)
dotenv_if_exists .env

# 4. Reload when dependency files change (triggers re-eval of .envrc)
watch_file requirements.txt
watch_file pyproject.toml

# 5. Add project scripts to PATH
PATH_add scripts

# 6. Non-secret project config
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export LOG_LEVEL=DEBUG
```

```gitignore
# Add to .gitignore
.direnv/
.envrc.local
.mise.local.toml
.venv/
venv/
```

## Best practices
- Shell hook order in `.bashrc`: mise activate → direnv hook (direnv hook must be last)
- Use `layout python-venv .venv` instead of `layout python` — the latter creates venv in `.direnv/python-X.Y.Z/` which is harder to find and inspect
- Use `watch_file requirements.txt` to auto-reload `.envrc` when requirements change (triggers a reminder to rerun `pip install`)
- Commit `.tool-versions` or `mise.toml` to git; never commit `.env`, `.direnv/`, or `.venv/`
- Use `mise use --global python@3.12.8` to set a global fallback version; per-project overrides via `mise use python@X.Y.Z` (writes `.tool-versions`)
- On servers running multiple projects, install all needed runtime versions up front with `mise install` rather than on-demand — avoids surprise download during a deploy
- For systemd services, do not rely on direnv — source the venv explicitly in the `ExecStart` path (`/path/to/project/.venv/bin/python`)

## AI-agent gotchas
- `direnv allow` is the one operation the agent cannot perform on behalf of the user — it is an explicit trust grant that requires human action; agent must note this in its output
- After the agent writes `.envrc`, changes are not visible until `direnv allow` is run — agent must not test commands that depend on the new environment immediately after writing the file
- `mise install` without arguments reads `.tool-versions` in the current directory — agent must be in the correct directory when running this command
- `layout python-venv .venv` fails silently if the Python version from mise is not installed — agent must run `mise install` first
- direnv hooks in non-interactive shells (cron, systemd) do not execute — agent must use explicit venv activation paths in systemd unit `ExecStart`, not rely on `.envrc`
- Editing `.envrc` invalidates the trust grant — direnv blocks loading until `direnv allow` is re-run, even for minor changes; agent should batch all `.envrc` changes into one write

## References
- https://direnv.net/docs/installation.html
- https://mise.jdx.dev/getting-started.html
- https://mise.jdx.dev/configuration.html
- https://direnv.net/man/direnv-stdlib.2.html (stdlib functions reference)
- https://github.com/jdx/mise
