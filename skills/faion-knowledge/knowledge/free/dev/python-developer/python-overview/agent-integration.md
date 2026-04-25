# Agent Integration — Python Ecosystem Overview

## When to use
- Routing layer: agent receives "we need a Python solution for X" and uses this README to pick the domain (web / data / ML / automation) and ecosystem (FastAPI vs pandas vs PyTorch vs Airflow).
- Onboarding a new repo: an agent surveys imports/dependencies and maps them to a domain bucket so the right specialized methodology is loaded next.
- Picking a Python version, package manager (uv vs poetry vs pip), and lint/typecheck stack at project bootstrap.
- "Should we rewrite this hot loop in Rust?" decisions — agent uses the optimization-strategy table to recommend Numba/Cython/PyO3.
- Auditing a codebase for outdated tooling (`black` + `isort` + `flake8` → `ruff`; `pip-tools` → `uv`; `mypy` → `mypy + pyright + ty`).

## When NOT to use
- Inside a feature task that's already scoped — load the specific methodology (`python-fastapi`, `django-models`, `python-typing`) instead of this overview, which is too broad.
- Non-Python work — wrong tree.
- Choosing between Python web frameworks specifically — route to `python-web-frameworks/` which has the actual decision matrix; this overview only mentions them.
- Performance work where a real profile already exists — the overview's optimization table is qualitative, not predictive.

## Where it fails / limitations
- README pitches `uv` heavily but doesn't address `uv`'s limitations: it's still pre-1.0, lockfile format has changed, large monorepos hit `uv sync` cliffs, and Python interpreter management is opinionated. Agents will swap `poetry`/`pip` for `uv` even where it makes things worse (e.g., corporate proxies, custom indexes that need pip's `--index-url` semantics).
- "Use Python 3.12+ for new projects" — fine, but agents will then upgrade existing 3.10/3.11 codebases without checking dependency compat (`numpy<2` lockstep, `tensorflow` lag, `psycopg2` vs `psycopg[binary]` story, etc.).
- Performance table claims "Algorithm optimization 10-1000x speedup, Low complexity" — encourages agents to suggest "rewrite the algorithm" as the first answer, which is misleading without a profile.
- "Free-threading (experimental)" in 3.13 — agents will recommend it for production. It's not production-ready in 2025-2026.
- Package management section omits: monorepo workspaces, private indexes (Artifactory/Nexus/Azure Artifacts), `pyproject.toml` PEP 621 quirks, and the difference between `uv pip install` and `uv add`.
- ML stack section lumps "PyTorch / TensorFlow / scikit-learn / Hugging Face / LangChain / pydantic-ai" without saying when to use which. Agents will pull all of them.
- "Rust + PyO3 10-100x speedup, High complexity" — true headline, but ignores build/distribution complexity (manylinux wheels, maturin, ABI3). Agents under-estimate the maintenance burden.
- The trend "25-33% of new PyPI packages use Rust" is true for top packages by download but misleading as a general stat. Agents quote it in greenfield decisions where it doesn't apply.

## Agentic workflow
This methodology should run as a **first-pass routing step**, not as instructions. A sonnet/opus subagent reads the project brief plus the dependency list, classifies the domain (web/data/ML/automation/embedded/quantum/etc.), picks tooling (`uv` vs `poetry`, `ruff`, type-checker), and emits a `BOOTSTRAP.md` summary. A second subagent loads the specific methodology and executes. Always re-anchor on a profile (cProfile/line_profiler) before recommending any optimization tier above "algorithm".

### Recommended subagents
- `python-router` (sonnet) — classifies project, picks tooling stack, emits bootstrap.
- `faion-sdd-executor-agent` — picks up bootstrap tasks once the stack is locked.
- `faion-feature-executor` — sequential gate; runs `ruff check`, type-checker, `pytest` per slice.
- `password-scrubber-agent` — sweep `.env*` and config files before commit.

### Prompt pattern
```
Read pyproject.toml + the project brief. Output JSON only:
{
  "python_version": "3.12|3.13|3.14",
  "package_manager": "uv|poetry|pip+pip-tools",
  "linter": "ruff",
  "formatter": "ruff",
  "type_checker": "mypy|pyright|ty",
  "domain": "web-fastapi|web-django|web-flask|data-science|ml|automation|other",
  "next_methodology": "<path under skills/faion-knowledge/knowledge/...>"
}
Justify each in <=1 sentence after the JSON. Do NOT install anything.
```

```
You are auditing the dependency list for outdated tooling. Replace:
- black + isort + flake8 -> ruff
- pip-tools -> uv (only if no private index)
- nose/unittest only -> add pytest
- requirements.txt sole source -> add pyproject.toml [project]
Output a unified diff. Do NOT modify CI yet.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `uv` | Project + dep + Python version manager | https://docs.astral.sh/uv/ |
| `poetry` | Dep manager (mature alternative) | https://python-poetry.org/docs/ |
| `pip` / `pip-tools` | Baseline / lock | https://pip.pypa.io/ , https://pip-tools.readthedocs.io/ |
| `pyenv` | Python version manager (without uv) | https://github.com/pyenv/pyenv |
| `ruff` | Lint + format (replaces black/isort/flake8) | https://docs.astral.sh/ruff/ |
| `mypy` / `pyright` / `ty` | Type checking | https://mypy.readthedocs.io/ , https://github.com/microsoft/pyright , https://astral.sh/blog/ty |
| `pytest` + plugins | Testing | https://docs.pytest.org/ |
| `cProfile` / `line_profiler` / `py-spy` / `scalene` | Profiling | https://docs.python.org/3/library/profile.html , https://github.com/pyutils/line_profiler , https://github.com/benfred/py-spy , https://github.com/plasma-umass/scalene |
| `maturin` | Build PyO3/Rust extensions | https://www.maturin.rs/ |
| `cython` / `numba` | JIT/AOT compile hot paths | https://cython.readthedocs.io/ , https://numba.pydata.org/ |
| `bandit` | Security lint | https://bandit.readthedocs.io/ |
| `pip-audit` / `safety` | Vulnerability scan of deps | https://pypi.org/project/pip-audit/ , https://pyup.io/safety/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PyPI | OSS | Yes | Default index. Agents must respect private indexes when set. |
| Artifactory / Nexus / Azure Artifacts | SaaS / Self-hosted | Yes | Corporate Python indexes; require `~/.pip/pip.conf` or `uv` env vars. |
| Astral (uv, ruff, ty) | OSS | Yes | Fastest tooling stack; under active dev. |
| Read the Docs | SaaS | Yes | Hosts Sphinx/MkDocs builds for Python projects. |
| GitHub Actions / GitLab CI | SaaS | Yes | First-class Python CI; `actions/setup-python`, `astral-sh/setup-uv`. |
| Sentry | SaaS | Yes | Error + performance for any Python app. |
| Renovate / Dependabot | SaaS | Yes | Auto-PRs for `pyproject.toml`, `requirements.txt`, `uv.lock`. |
| PyPy.org / cpython.org | OSS | Yes | Alternative interpreters. |

## Templates & scripts
Bootstrap script — produce a sane modern Python project with `uv` + `ruff` + `mypy` + `pytest`.

```bash
#!/usr/bin/env bash
# scripts/bootstrap-python.sh PROJECT
set -euo pipefail
P=${1:?project name required}
uv init "$P" --python 3.12
cd "$P"
uv add --dev ruff mypy pytest pytest-cov
cat > pyproject.toml.append <<'TOML'
[tool.ruff]
line-length = 100
target-version = "py312"
[tool.ruff.lint]
select = ["E","F","I","B","UP","SIM","T20"]
[tool.mypy]
python_version = "3.12"
strict = true
[tool.pytest.ini_options]
addopts = "-q --strict-markers --strict-config"
TOML
cat pyproject.toml.append >> pyproject.toml && rm pyproject.toml.append
mkdir -p src tests
echo "def hello() -> str: return 'world'" > src/__init__.py
echo "from src import hello\n\ndef test_hello(): assert hello() == 'world'" > tests/test_hello.py
uv run ruff check . && uv run mypy src && uv run pytest -q
```

## Best practices
- Lock the Python version in `pyproject.toml` (`requires-python = ">=3.12"`) AND in `.python-version` (uv/pyenv).
- One package manager per project. Don't let agents add `poetry` to a `uv` project or vice versa.
- Pin dev tools (`ruff`, `mypy`, `pytest`) in `[project.optional-dependencies] dev` and run them all in CI on every PR.
- Always profile before optimizing — agents that quote the README's "10-1000x" without a profile waste cycles.
- Treat `uv`/`poetry` lockfiles as source of truth. Agents that regenerate without committing the lock will break colleagues.
- Use `ruff format` + `ruff check --fix` in pre-commit; never let an agent commit unformatted code.
- For ML, pin `torch` / `tensorflow` / `numpy` exactly — minor versions break wheels constantly.
- For Rust integration, set up `maturin` with `abi3` so a single wheel covers Python 3.10-3.14.

## AI-agent gotchas
- Agents pin `python>=3.12` in `pyproject.toml` then use a feature only available in 3.13 (`@override` from `typing` in 3.12 vs `typing_extensions` in earlier). Re-state the floor explicitly.
- Agents replace `requirements.txt` with `pyproject.toml` + `uv.lock` without checking that CI/Dockerfile read the lock file. CI keeps installing the old `requirements.txt`.
- Agents enable `ruff` rule sets ("ALL") and break the build with hundreds of false positives. Curate the rule set per the project's AGENTS.md (`E,W,F,I,B,C4,UP,SIM,DJ,T20`).
- Agents recommend `numba`/`cython` for code that's I/O-bound (network call inside the loop). They speed up CPU only.
- Agents rewrite a hot loop in Rust + PyO3 without measuring; the overhead of the FFI boundary kills the win on small-payload functions.
- Agents quote "free-threading (experimental)" as a reason to use Python 3.13 in production. It's not safe yet — keep GIL-Python until 3.14+ default builds support it.
- Agents collapse `mypy` and `pyright` configs into "use both" without considering CI minutes; pick one for CI, optionally the other in the IDE.
- Human-in-loop checkpoint: any change to lockfile, CI workflow, Dockerfile, or `pyproject.toml [project]` should be reviewed.

## References
- https://docs.python.org/3/whatsnew/index.html
- https://docs.astral.sh/uv/
- https://docs.astral.sh/ruff/
- https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/
- https://www.stuartellis.name/articles/python-modern-practices/
- https://pyo3.rs/
- https://numba.pydata.org/
- https://pydevtools.com/handbook/
