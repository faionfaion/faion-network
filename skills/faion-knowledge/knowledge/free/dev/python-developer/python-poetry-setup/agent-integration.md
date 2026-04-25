# Agent Integration — Poetry Project Setup

## When to use

- Bootstrapping a new Python service that will live for years and be published or vendored (lock file + PEP 621 metadata required).
- Migrating a Python 1.x Poetry project to Poetry 2.x (PEP 621 layout) — the migration is mechanical and ideal for an agent run.
- Adding/removing dependencies on an established repo where `poetry.lock` is the source of truth and CI fails on drift.
- Splitting deps into groups (`dev`, `test`, `docs`) when ad-hoc `requirements*.txt` files have multiplied and started to disagree.
- Producing a deterministic build artifact (wheel/sdist) for PyPI or an internal index.

## When NOT to use

- One-shot scripts, notebooks, throwaway experiments — `uv` or plain `pip install` is faster and the lock file overhead is not worth it.
- CI hot paths where install time matters (Poetry resolves slowly on large trees; `uv pip install -r` or `uv lock` is 10-100x faster).
- Memory-constrained agents/containers (<512 MB) — Poetry resolver can spike to 1-2 GB on big trees and OOM-kill the agent.
- Repos already standardised on `uv` / `pdm` / `hatch` — don't introduce a second tool; convert via `poetry export -f requirements.txt` or migrate fully.
- Cross-language monorepos where a Bazel/Pants build graph already pins versions.

## Where it fails / limitations

- **Resolver explosions.** Big scientific stacks (numpy + scipy + torch + tensorflow) can take 5-30 min to resolve; agents time out and retry, corrupting `poetry.lock`. Mitigate with `poetry lock --no-update` and constraining version ranges.
- **`poetry.lock` merge conflicts** are unsolvable by line edits — must regenerate. Agents that try `Edit` on lock files always break it.
- **Mixed `pip` + `poetry` in same venv** silently desyncs. `poetry install` will not see packages added with `pip install` and may "fix" them away.
- **Private indexes.** `[[tool.poetry.source]]` config is order-sensitive (`primary` vs `supplemental` vs `explicit`); a wrong order causes Poetry to publish to the wrong index or hang on auth.
- **Plugin churn.** `poetry-plugin-export`, `poetry-plugin-bundle`, monorepo plugins each pin to a Poetry minor version. After upgrading Poetry, plugins may break silently.
- **Poetry 2.0 migration** of the `[tool.poetry]` table to `[project]` is partial; some fields (e.g. dynamic versioning, plugins) still live under `[tool.poetry]`. Agents that "fully migrate" by deleting `[tool.poetry]` will lose config.
- **`poetry shell`** was removed/renamed across versions. Agents memorising `poetry shell` will fail on 2.x where `poetry env activate` is the new path.

## Agentic workflow

Drive Poetry as a deterministic CLI runner: never edit `pyproject.toml` dependency tables by hand — call `poetry add/remove/update` and let the tool rewrite the file plus the lock together. After every mutation, run `poetry check`, `poetry lock --check`, and `poetry install --sync` to keep the venv canonical. Commit `pyproject.toml` and `poetry.lock` together in the same commit; reject any diff that touches one without the other. For long-running resolves, dispatch them as background bash with a timeout and a status file the orchestrator polls.

### Recommended subagents

- `faion-python-developer` — Owns Python project bootstrap; knows Poetry 2.x layout and group conventions used in this workspace.
- `faion-devops-engineer` / `faion-cicd-engineer` — Wires `poetry install --no-root --only main` into CI, caches `~/.cache/pypoetry`, configures private index auth.
- `faion-sdd-executor-agent` — Runs the bootstrap as an SDD task: read spec, run commands, validate gates (lock present, `poetry check` clean, tests run via `poetry run pytest`).
- General-purpose `Task` subagent for migrations — given `llm-prompts.md` from this methodology and the existing `pyproject.toml`, produce a migration plan + apply it sequentially.

### Prompt pattern

Bootstrap a new package:

```
Goal: bootstrap Python 3.12 package "<name>" with Poetry 2.x.
Steps: poetry new --src <name>; cd <name>; poetry config virtualenvs.in-project true;
poetry add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg;
poetry add -G dev pytest pytest-asyncio mypy ruff pre-commit;
poetry install --sync; poetry run pre-commit install.
Commit pyproject.toml + poetry.lock together. Run `poetry check` as gate.
Do not hand-edit poetry.lock. If resolver fails, paste error verbatim, do not retry blindly.
```

Add a dependency safely:

```
Run: poetry add "<pkg>@^<version>" --group <main|dev|docs>.
After success: poetry lock --check; poetry install --sync; poetry run pytest -x.
If resolver picks an unexpected version, run: poetry show <pkg> --tree.
Stage pyproject.toml + poetry.lock in one commit.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `poetry` | Core CLI: deps, lock, build, publish | https://python-poetry.org/docs/ (use `pipx install poetry`) |
| `pipx` | Install Poetry isolated from project venvs | `apt install pipx` / https://pipx.pypa.io |
| `uv` | Fast alternative resolver; can run `uv pip install` against `poetry export` output for CI | `pipx install uv` / https://docs.astral.sh/uv/ |
| `poetry-plugin-export` | Export `requirements.txt` for Docker/CI that doesn't speak Poetry | `poetry self add poetry-plugin-export` |
| `poetry-plugin-bundle` | Build self-contained venv bundles for offline deploy | `poetry self add poetry-plugin-bundle` |
| `poetry-plugin-up` | Upgrade dependencies respecting constraints | `poetry self add poetry-plugin-up` |
| `poetry-plugin-shell` | Restores `poetry shell` on 2.x | `poetry self add poetry-plugin-shell` |
| `poetry-monoranger-plugin` | Shared lock + venv across monorepo packages | `poetry self add poetry-monoranger-plugin` |
| `pre-commit` | Hook `poetry-check` + `poetry-lock --check` into git | https://pre-commit.com |
| `pyenv` | Manage Python versions Poetry will use | https://github.com/pyenv/pyenv |
| `cibuildwheel` | Build wheels in CI for native-extension packages | https://cibuildwheel.pypa.io |
| `twine` | Fallback to publish if `poetry publish` is restricted | https://twine.readthedocs.io |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PyPI | OSS index | Yes — token auth via `poetry config pypi-token.pypi <token>` | Default publish target |
| Test PyPI | OSS index | Yes — `poetry config repositories.testpypi https://test.pypi.org/legacy/` | Use for pre-publish dry runs |
| GitHub Packages (PyPI) | SaaS | Yes — supplemental source + token | Per-org private packages |
| Artifactory / Nexus / Azure Artifacts | SaaS/self-host | Yes — `[[tool.poetry.source]]` | Enterprise private index |
| Cloudsmith | SaaS | Yes — REST + Poetry source | Smaller orgs |
| Read the Docs | SaaS | Indirect — uses `poetry export` to feed `requirements.txt` | Doc builds |
| Renovate / Dependabot | SaaS | Yes — both understand `poetry.lock` | Auto-PRs for upgrades |
| GitHub Actions / GitLab CI | SaaS | Yes — official `snok/install-poetry` action | Cache `~/.cache/pypoetry` and `.venv` |
| Docker Hub / GHCR | SaaS | Yes — multi-stage with `poetry export` then `pip install` for slim runtime images | Avoid Poetry in final image |
| `pypi-stubs` / `mypy --install-types` | OSS | Indirect — agent runs after `poetry install` | Type-stub bootstrap |

## Templates & scripts

See methodology `templates.md` for full `pyproject.toml` examples. Inline helper to verify Poetry health on any repo (≤30 lines):

```bash
#!/usr/bin/env bash
# poetry-doctor.sh — fails non-zero if repo is not Poetry-clean.
set -euo pipefail
test -f pyproject.toml || { echo "no pyproject.toml"; exit 2; }
test -f poetry.lock    || { echo "no poetry.lock";    exit 2; }
poetry --version
poetry check                                   # validates pyproject.toml
poetry lock --check                            # lock matches pyproject
poetry env info --path >/dev/null              # venv exists / can be created
poetry run python -c "import sys; assert sys.version_info >= (3, 11)"
poetry run pip check                           # no broken deps
poetry show --outdated || true                 # informational
echo "OK: poetry repo is healthy"
```

Multi-stage Docker build that produces a Poetry-free runtime (≤25 lines):

```dockerfile
FROM python:3.12-slim AS builder
RUN pip install --no-cache-dir poetry==2.0.1 poetry-plugin-export
WORKDIR /src
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes --only main -o /tmp/req.txt
COPY src/ ./src/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/req.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels ./

FROM python:3.12-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels
USER 1000
CMD ["python", "-m", "myapp"]
```

## Best practices

- **Pin Poetry itself** in CI (`pipx install poetry==2.0.1`); agents that use "latest" introduce non-reproducible breakage.
- **`poetry config virtualenvs.in-project true`** so the venv is `./.venv` — agents can introspect `python -c` without `poetry run` overhead.
- **One commit = pyproject + lock.** Add a pre-commit hook that fails if only one of the two changed.
- **Use `poetry add --lock --no-update`** when adding to a frozen lock during hotfixes — prevents the resolver from "helpfully" upgrading siblings.
- **Cache `~/.cache/pypoetry`** keyed on `poetry.lock` hash in CI, not on date — invalidates correctly.
- **Never put `poetry` in the runtime container.** Export to `requirements.txt` or wheels and `pip install` at runtime — slimmer image, no resolver in prod.
- **Group convention:** `dev` for lint/format/type, `test` for pytest stack, `docs` for mkdocs, `notebook` optional. One purpose per group, all named consistently across repos.
- **Use `^` only for libraries you trust to follow semver**; `~` for pre-1.0 packages; pin exact (`==`) for tools whose output matters (e.g. `ruff`, `black`).
- **Do `poetry update --dry-run`** before `poetry update`; review the diff. Bulk update without review is the #1 source of CI breakage.

## AI-agent gotchas

- **Agents will try to `Edit` `poetry.lock`.** Block it: lock is generated, never hand-edited. If the agent's "fix" is to tweak the lock, reject the patch.
- **Agents conflate `poetry add` and `pip install`.** Mixing in the same venv silently desyncs. Enforce: any dependency change must go through `poetry add/remove`.
- **Long resolves get killed.** A 5-15 min resolve looks like a hang; agents kill and retry, corrupting state. Set `POETRY_REQUESTS_TIMEOUT=60` and run `poetry lock` in `run_in_background` with a status file.
- **`poetry shell` doesn't exist on Poetry 2.x by default.** Either install `poetry-plugin-shell` or use `poetry env activate` (returns shell-eval string). Agents copy-pasting blogs from 2023 will get errors.
- **Migration partials.** Migrating from 1.x to 2.x via `poetry-plugin-migrate` keeps `[tool.poetry]` as a transition table. Agents that "clean it up" by deleting the section will lose plugin config and dynamic versioning.
- **PEP 621 vs Poetry 1.x dep syntax.** `python = "^3.11"` is Poetry 1.x; `requires-python = ">=3.11,<4.0"` is PEP 621. Mixing both yields contradictory constraints. Pick one tree.
- **Authentication for private indexes** is split across `poetry config` and env vars. Agents that set only env vars miss `keyring` lookups. Always run `poetry config --list` to verify.
- **Network-flaky resolves** look identical to "package doesn't exist". Agents must distinguish HTTP 5xx (retry) from 4xx (real error). `poetry add -vvv` exposes the distinction.
- **`poetry install` without `--sync`** leaves stale packages from previous installs; tests pass locally, fail in clean CI. Always `--sync` in CI; `--sync` warns locally.
- **Lock-file churn from `poetry update`** can rewrite hundreds of lines for unrelated transitives. Diff review is mandatory; auto-merging is dangerous.

## References

- Poetry docs (2.x): https://python-poetry.org/docs/
- Poetry 2.0 announcement: https://python-poetry.org/blog/announcing-poetry-2.0.0/
- PEP 621 (project metadata): https://peps.python.org/pep-0621/
- PEP 735 (dependency groups): https://peps.python.org/pep-0735/
- `snok/install-poetry` GitHub Action: https://github.com/snok/install-poetry
- `poetry-plugin-export`: https://github.com/python-poetry/poetry-plugin-export
- `poetry-plugin-bundle`: https://github.com/python-poetry/poetry-plugin-bundle
- `poetry-plugin-shell`: https://github.com/python-poetry/poetry-plugin-shell
- `poetry-plugin-migrate`: https://github.com/zyf722/poetry-plugin-migrate
- `poetry-monoranger-plugin`: https://github.com/ag14774/poetry-monoranger-plugin
- uv (alt resolver): https://docs.astral.sh/uv/
- Renovate Poetry config: https://docs.renovatebot.com/modules/manager/poetry/
