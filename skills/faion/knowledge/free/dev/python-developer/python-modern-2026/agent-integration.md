# Agent Integration — Modern Python 2026

Methodology covers Python 3.12, 3.13, 3.14 features (PEP 695 generics, PEP 701 f-strings, free-threaded mode, JIT, t-strings, deferred annotations, multiple interpreters) plus modern tooling (uv, ruff, pyright, hatchling). Use this file when an agent must bootstrap, migrate, or modernize a Python project to current best practices.

## When to use
- Bootstrapping a new Python project — `uv init`, `pyproject.toml`, ruff + mypy + pytest pre-wired.
- Migrating 3.10/3.11 code to 3.12+ — built-in generics, PEP 695 type parameters, modern f-strings.
- Switching from pip/poetry/venv to uv for 10-100x install speed and unified Python version management.
- Replacing Black + Flake8 + isort + pyupgrade with a single Ruff config.
- Adopting free-threaded Python 3.13t / 3.14 for CPU-bound parallelism (no GIL).
- Setting up CI/CD that pins Python with `uv python pin` and uses lockfile-aware caching.

## When NOT to use
- Locked legacy environments (Python 3.8, RHEL system Python, vendored interpreters) — features described break or aren't available.
- Production at scale on free-threaded mode without thorough thread-safety audit — many C extensions are still GIL-required (3.13 free-threaded is experimental, 3.14 stabilizes).
- Pure data-science notebooks — conda/mamba ecosystem is still entrenched; uv adoption mixed.
- Existing healthy poetry/PDM project with strong tooling — switching to uv just for fashion costs more than it returns.
- Code that depends on synchronous import side-effects — PEP 649 / PEP 810 lazy annotations and lazy imports change timing.

## Where it fails / limitations
- README assumes Linux/macOS shell — Windows agents need `powershell` install command for uv.
- Free-threaded benchmarks shown without workload context — pure CPU-bound is best case; mixed loads show smaller wins, sometimes regressions.
- t-strings (PEP 750) are 3.14+ — agents writing for 3.12/3.13 must not emit `t"..."`.
- PEP 695 `type` statement is lazy — circular references resolve at first access; subtle bugs not flagged here.
- README does not pick a build backend — hatchling shown, but `uv_build`, `setuptools`, `flit_core`, `poetry-core` are all viable. Agents pick inconsistently across repos.
- Performance numbers (1.55x at 3.14) are headline benchmarks, not your workload — README presents them as gospel.
- `python3.13t` (free-threaded build) is a *separate* binary; agents conflate it with stock `python3.13` and produce broken `uv python install 3.13` recipes.
- No coverage of `uv tool install` (replaces pipx) or `uv run --with` (ad-hoc deps) — common agent shortcuts.
- ruff config snippet is a starting point — security rules `S` need per-project tuning (false positives in tests, asserts).

## Agentic workflow
New project: (1) `uv init proj --python 3.13`, (2) draft `pyproject.toml` from `templates.md`, (3) `uv add fastapi pydantic`, (4) `uv add --dev pytest pytest-asyncio ruff mypy pre-commit`, (5) commit lockfile, (6) `pre-commit install` and verify hook runs ruff + mypy on touched files. Migration: (1) read current Python version, (2) bump `requires-python = ">=3.12"` after team consensus, (3) `ruff check --select UP --fix` to auto-modernize syntax, (4) run tests under new interpreter, (5) flip ruff `target-version = "py312"`. Free-threaded experiment: isolate to a single CPU-bound module first, install `python3.13t` separately, run benchmark before/after.

### Recommended subagents
- `faion-devtools-developer` — Owns `pyproject.toml`, ruff/mypy/uv config, pre-commit.
- `faion-code-agent` — Default for code modernization edits (PEP 585 / PEP 604 / PEP 695 rewrites).
- `faion-software-architect` — Decides Python version pin, build backend, free-threading viability.
- `faion-sdd-execution` — Drives the migration as a multi-task feature with rollback gates.
- `faion-test-agent` — Verifies pytest config and that all tests pass on target interpreter.

### Prompt pattern

Bootstrap a new project:

```
Initialize a Python 3.13 project at ./<name> using uv per
free/dev/python-developer/python-modern-2026/README.md and templates.md.
Include:
  - pyproject.toml: requires-python ">=3.13", build-backend hatchling, src layout.
  - Dev deps: pytest, pytest-asyncio, pytest-cov, ruff>=0.8, mypy>=1.13, pre-commit.
  - ruff: select E F I B UP N S C4 PT, target-version py313.
  - mypy: strict = true, python_version "3.13".
  - .pre-commit-config.yaml: ruff (lint+format), mypy on touched files.
  - GitHub Actions: matrix [3.12, 3.13], `uv sync` + `uv run pytest -v --cov`.
Run `uv sync && uv run pytest` and paste output.
```

Modernize syntax:

```
In <path>, modernize Python typing & f-strings to 3.12+ per
free/dev/python-developer/python-modern-2026/README.md:
  - Replace typing.List/Dict/Tuple/Optional with list/dict/tuple/X|None.
  - Convert TypeVar+Generic to PEP 695 syntax where the change is local.
  - Use PEP 701 f-string features only where they improve readability.
  - Run `ruff check --select UP --fix` first; review the diff; then mypy.
Do NOT introduce t"..." (3.14) or PEP 695 `type` aliases without confirming target version.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `uv` | Package + Python version + venv manager (Rust, 10-100x pip) | https://docs.astral.sh/uv/ |
| `uv python install 3.12 3.13 3.14` | Manage interpreters per-user, no system pollution | bundled |
| `uv tool install <pkg>` | Replaces pipx — install CLIs in isolated envs | bundled |
| `uv run --with <dep> <cmd>` | Ad-hoc execution with extra deps, no env mutation | bundled |
| `ruff check --fix` / `ruff format` | One tool replaces flake8 + black + isort + pyupgrade | https://docs.astral.sh/ruff/ |
| `mypy` | Reference type checker, plugin support | https://mypy.readthedocs.io |
| `pyright` | Microsoft type checker, faster, default in VSCode | https://microsoft.github.io/pyright/ |
| `pytest` + `pytest-asyncio` + `pytest-cov` + `pytest-xdist` | Standard test stack | https://docs.pytest.org/ |
| `pre-commit` | Hook runner — runs ruff/mypy/etc on staged files | https://pre-commit.com |
| `hatch` / `hatchling` | Modern build backend (PEP 517) | https://hatch.pypa.io/ |
| `tox-uv` / `nox` | Test matrix orchestration with uv | https://github.com/tox-dev/tox-uv |
| `python3.13t` (free-threaded) | Separate interpreter binary, no-GIL build | https://docs.python.org/3/howto/free-threading-python.html |
| `python3.13 -X jit script.py` | Enable experimental JIT | https://docs.python.org/3/howto/perf_profiling.html |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| PyPI | Package registry | Yes | uv resolves against PyPI by default |
| GitHub Actions | CI | Yes — `astral-sh/setup-uv@v5` action | Lockfile-aware caching |
| GitLab CI | CI | Yes — install uv in `before_script` | Same caching pattern |
| Docker `python:3.13-slim` | Base image | Yes | Use `COPY --from=ghcr.io/astral-sh/uv` for prod images |
| Read the Docs | Docs hosting | Yes | Use uv via `tool.uv` build config |
| Codecov / Coveralls | Coverage | Yes | `uv run pytest --cov --cov-report=xml` |
| pyOpenSci, scientific-python | OSS communities | Yes | Modern build backends accepted |
| conda-forge | Alt registry | Partial | uv does NOT resolve conda packages |

## Templates & scripts

See `templates.md` for full `pyproject.toml`, `pre-commit-config.yaml`, GitHub Actions matrix. Add this minimal bootstrap helper (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/bootstrap.sh — fresh modern-Python project from zero.
set -euo pipefail
NAME="${1:?usage: bootstrap.sh <project-name>}"
PYVER="${2:-3.13}"

uv init "$NAME" --python "$PYVER" --package
cd "$NAME"

uv add --dev pytest pytest-asyncio pytest-cov ruff mypy pre-commit
uv add fastapi 'pydantic>=2.0' 'uvicorn[standard]'

cat > .pre-commit-config.yaml <<'YAML'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-requests]
YAML

uv run pre-commit install
uv run pytest -v || true
echo "Project '$NAME' ready. Activate with: cd $NAME && uv run python ..."
```

## Best practices
- **Pin one Python version per repo** via `.python-version` (uv reads it). CI matrix can fan out, but development is single-version.
- **Lockfile is a first-class artifact.** `uv.lock` committed; CI runs `uv sync --frozen` to detect drift.
- **`requires-python` matches `target-version`** — `pyproject.toml` `requires-python = ">=3.13"` ↔ ruff `target-version = "py313"` ↔ mypy `python_version = "3.13"`. Drift causes silent rule mismatches.
- **Use src layout** (`src/<pkg>/`) — keeps tests from accidentally importing from the working directory.
- **Don't enable free-threading in production** until your full dependency tree is audited. Most C extensions still use the GIL; running them under `python3.13t` either works (slow) or crashes.
- **`ruff check --select UP --fix`** is safe — it only modernizes syntax. Run it as a one-shot migration, not constantly.
- **Reserve `S` (bandit) rules** for prod code; relax in tests via `[tool.ruff.lint.per-file-ignores] "tests/**" = ["S101"]` (assert is fine in tests).
- **`uv tool install ruff mypy`** for global tooling — keeps project venvs lean.
- **Cache `~/.cache/uv` in CI** keyed on `uv.lock` hash — full installs are seconds, not minutes.
- **JIT is opt-in** via `-X jit`; don't ship apps assuming it's on. Profile to confirm wins.

## AI-agent gotchas
- **`t"..."` template strings only exist in Python 3.14+.** Agents grab the syntax from this README and paste into 3.12 code; runtime `SyntaxError`.
- **PEP 695 `type Vec[T] = list[T]` requires 3.12+.** Mixing with `from typing import TypeAlias` is fine but redundant; pick one.
- **`uv python install 3.13t`** is the free-threaded build — not the same as `3.13`. Don't conflate.
- **`uv run` invokes the project's venv automatically** — no `source .venv/bin/activate`. Agents that activate manually break uv's cache logic.
- **`uv sync` removes packages not in `pyproject.toml`** — surprise for agents who `pip install` ad-hoc. Use `uv add` or `uv run --with`.
- **`ruff format` does NOT obey Black exactly** — small differences (string quotes, trailing commas in some edges). Pin ruff version per repo.
- **`mypy_django_plugin` requires settings module** — pyright doesn't, so agents flipping checkers see different error counts.
- **`pyproject.toml [tool.uv]` block** controls uv-specific options (index URLs, dev deps groups). Agents miss it and put dev deps in `[project.optional-dependencies]` only.
- **Hatchling `[tool.hatch.build.targets.wheel] packages` must match src layout**. Mismatch → empty wheel, no `ImportError` until install.
- **Free-threaded benchmarks lie** for I/O-bound code — README's table is honest but agents quote 3.3x speedup for code that won't see it.
- **`f"{path.replace('\\', '/')}"` (PEP 701)** only works in 3.12+. Older Python errors at parse time, not runtime.
- **`asyncio_mode = "auto"`** in pytest config means every `async def test_` runs without `@pytest.mark.asyncio` — agents removing the marker on 3.11+ projects without `auto` mode break tests silently.

## References
- README: `./README.md`
- Sibling: `../python-type-hints/`, `../python-async/`, `../python-poetry-setup/`, `../python-code-quality/`
- uv docs: https://docs.astral.sh/uv/
- ruff docs: https://docs.astral.sh/ruff/
- Python 3.12 What's New: https://docs.python.org/3/whatsnew/3.12.html
- Python 3.13 What's New: https://docs.python.org/3/whatsnew/3.13.html
- Python 3.14 What's New: https://docs.python.org/3/whatsnew/3.14.html
- Free-threading HOWTO: https://docs.python.org/3/howto/free-threading-python.html
- PEP 695 (type parameter syntax): https://peps.python.org/pep-0695/
- PEP 703 (no-GIL): https://peps.python.org/pep-0703/
- PEP 750 (t-strings): https://peps.python.org/pep-0750/
- PEP 649 (deferred annotations): https://peps.python.org/pep-0649/
- PEP 734 (multiple interpreters): https://peps.python.org/pep-0734/
- hatchling: https://hatch.pypa.io/latest/
