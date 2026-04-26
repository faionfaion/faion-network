# Agent Integration — Poetry Project Setup

## When to use
- Bootstrapping a new Python service or library that will be agent-managed (Claude Code as primary contributor).
- Locking dependency closures so a CI agent and a local agent produce byte-identical environments.
- Wrapping a Django/FastAPI repo where you want `poetry add` / `poetry remove` to be the only mutation surface for `pyproject.toml`.
- Publishing a wheel to PyPI/private index with token-based auth (Poetry handles upload state without manual `twine`).

## When NOT to use
- Throwaway scripts or notebooks → `uv pip install` or `pipx run` is faster.
- Projects already standardized on `pip-tools`, `uv`, or `pdm` — don't migrate just for novelty; lockfile semantics differ.
- Containers built from `requirements.txt` with no need for solver runtime → keep pip; export from Poetry only at build time.
- Monorepos with native workspace tooling (Pants, Bazel) — Poetry has no first-class workspace concept (until 2.0 plugins).

## Where it fails / limitations
- Solver can hang on large constraint sets (e.g., many `numpy`/`scipy`/`torch` extras); `poetry lock --no-update` is mandatory for partial bumps.
- `poetry install` in Docker is ~2-3x slower than `pip install -r requirements.txt`; production images should `poetry export` at build time and use plain pip.
- `poetry shell` was removed in Poetry 2.0 (replaced by `poetry env activate` echo + manual `source`); older docs and many agent scripts still call `poetry shell` and break.
- `poetry update` without arguments rewrites the entire lockfile — destructive when a teammate has staged a different solver result.
- Hash mismatch errors from a partially populated cache (`~/.cache/pypoetry`) require `poetry cache clear --all pypi` to recover.

## Agentic workflow
A code-writing subagent proposes the dependency change, then a separate command executor runs `poetry add ... --dry-run`, parses the diff, and only after human/coordinator approval runs the real command. The lockfile diff is treated as a reviewable artifact (committed alongside `pyproject.toml`). For CI, agents should call `poetry install --sync --no-interaction --no-root` so removed deps get pruned and the run is reproducible.

### Recommended subagents
- `faion-sdd-executor-agent` — drives task-level changes; can own a TASK that says "add httpx and pin to ^0.27".
- `password-scrubber-agent` — sanity-check before publishing; ensures no `pypi-token`, repo URLs with creds, or `private` index credentials slipped into `pyproject.toml`.
- A purpose-built `dependency-bumper` subagent (not yet in repo) for routine `poetry update --dry-run` → PR loop.

### Prompt pattern
```
You may only mutate pyproject.toml via `poetry add|remove|update`.
Run with --dry-run first. Print the lockfile diff. Stop before committing.
```
```
Audit pyproject.toml: list each dep, group, version pin, and whether the
constraint is open-ended (^/~). Flag anything in [tool.poetry.dependencies]
that should be in [tool.poetry.group.dev.dependencies].
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `poetry` | Solver, env mgmt, build, publish | `curl -sSL https://install.python-poetry.org \| python3 -` · https://python-poetry.org/docs/ |
| `poetry-plugin-export` | Emit requirements.txt for Docker | `poetry self add poetry-plugin-export` |
| `poetry-plugin-bundle` | Bundle env into a venv directory | `poetry self add poetry-plugin-bundle` |
| `pipx` | Isolate Poetry itself from project venvs | `apt install pipx` |
| `tomlq` / `dasel` | Read/edit `pyproject.toml` from scripts | https://github.com/TomWright/dasel |
| `pip-audit` | CVE scan against the lockfile | `pipx install pip-audit` then `poetry export \| pip-audit -r /dev/stdin` |
| `deptry` | Detect unused/missing imports vs declared deps | `pipx install deptry` |
| `uv` | Drop-in faster resolver/installer; can read Poetry projects | https://github.com/astral-sh/uv |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PyPI | SaaS | Yes | `poetry config pypi-token.pypi <token>` from env; tokens in 1Password vault. |
| Test PyPI | SaaS | Yes | Use `poetry publish -r testpypi` before real release. |
| GitHub Packages | SaaS | Partial | Works for private; agent must inject `POETRY_HTTP_BASIC_*` envs. |
| Gemfury / Cloudsmith / JFrog | SaaS | Yes | Configure once with `poetry config repositories.<name>` then publish via env-based auth. |
| Renovate / Dependabot | SaaS | Yes | Both understand `pyproject.toml` + `poetry.lock`; prefer Renovate for grouped updates. |
| `pypiserver` (self-hosted) | OSS | Yes | Drop-in private index for offline agent loops. |

## Templates & scripts
See `templates.md` for full `pyproject.toml` and Dockerfile. A minimal agent-callable bootstrap:

```bash
#!/usr/bin/env bash
# poetry-bootstrap.sh — idempotent project init
set -euo pipefail
NAME="${1:?slug required}"
poetry config virtualenvs.in-project true --local || true
[ -f pyproject.toml ] || poetry init --no-interaction --name "$NAME" --python "^3.11"
poetry add --group dev pytest pytest-cov ruff mypy pre-commit
poetry add --group dev --optional ipython ipdb
poetry install --sync --no-interaction
poetry run pre-commit install
echo "OK: $(poetry env info --path)"
```

## Best practices
- Pin Python with a tight constraint (`python = "^3.11"`, not `>=3.8`); broader ranges slow the solver and produce hostile error messages.
- Always use `--sync` in CI install — it removes packages that left the lockfile, preventing zombie deps.
- Split `dev`, `test`, `docs` groups; mark `docs` as `optional = true` so production installs don't pull mkdocs.
- Commit `poetry.lock`. Period. There is no situation where a library should omit it.
- When publishing a library, set `[tool.poetry.dependencies]` ranges loosely (`^x.y`) but keep `poetry.lock` for the dev workflow. Don't ship the lock to PyPI.
- Use `poetry self add` for plugins, never `pip install` into the Poetry interpreter — pip will silently corrupt Poetry's own deps.
- Combine with `pre-commit` running `ruff check --fix`, `ruff format`, and a `poetry check --lock` hook that fails on dirty lockfile.
- For Docker: multi-stage build, run `poetry export --without-hashes -o requirements.txt --with main`, install via pip in final stage, keep image small and free of Poetry runtime.

## AI-agent gotchas
- An agent calling `poetry add X` when the lockfile is dirty (someone added Y locally and didn't commit) will silently lock Y too. Always run `poetry check --lock` before any add/remove.
- `poetry shell` in headless CI hangs forever waiting for a tty. Use `poetry run <cmd>` from agents — never `shell`.
- Network blips during `poetry lock` corrupt the cache; agent retries should `poetry cache clear --all pypi --no-interaction` between attempts.
- Some plugins write absolute paths into `poetry.lock` (`develop = true` editable installs). Agents that copy lockfiles between machines will produce non-reproducible installs — use `--no-editable` when it matters.
- Version-string mistakes are the #1 agent error: `^0.1` means `>=0.1.0,<0.2.0` (NOT `<1.0.0`). Have the agent always run `poetry add --dry-run` and read back the resolved range before commit.
- Token leak risk: `poetry config pypi-token.pypi $TOKEN` writes to `~/.config/pypoetry/auth.toml`. Agents in shared sandboxes must use `POETRY_PYPI_TOKEN_PYPI` env var instead, which is process-scoped.
- `poetry install` without `--no-root` will try to install the current project as a package; for service repos (no `setup.py` install needed) always pass `--no-root` to avoid spurious failures.
- Poetry 2.0 changed plugin and command behavior (e.g., removed `shell`, changed `lock --no-update` to default). Pin Poetry version (`pipx install 'poetry==1.8.5'` or 2.x explicitly) in CI to avoid drift.

## References
- https://python-poetry.org/docs/ — official docs
- https://python-poetry.org/docs/dependency-specification/ — version constraint grammar
- https://python-poetry.org/docs/cli/#add — `poetry add` flags reference
- https://github.com/python-poetry/poetry/blob/master/CHANGELOG.md — breaking changes per release
- https://snarky.ca/what-the-heck-is-pyproject-toml/ — Brett Cannon on PEP 518/621 history
- https://docs.astral.sh/uv/ — uv as a Poetry-compatible alternative resolver
