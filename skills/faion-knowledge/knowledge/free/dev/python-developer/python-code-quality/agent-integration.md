# Agent Integration — Python Code Quality

## When to use

- Setting up the lint + format + type-check + security gate on a new Python repo (Ruff + mypy + bandit + pytest-cov + pre-commit).
- Migrating a legacy repo off `flake8 + black + isort + autoflake + pyupgrade` to Ruff in a single pass.
- Onboarding a Django/FastAPI codebase to strict typing — adding `mypy --strict` or `pyright strict` and fixing the long tail iteratively.
- Wiring CI quality gates: zero Ruff errors, zero mypy errors on touched files, ≥80% coverage, no high/critical bandit findings.
- Reviewing PRs with an agent that runs the full quality stack and reports findings (style, types, security, complexity) per file.

## When NOT to use

- One-off scripts, hackathon code, notebook spikes — friction from tooling exceeds value; rely on the editor's built-in linter.
- Repos where the user explicitly chose a different stack (Pylint + Black + flake8). Don't impose Ruff if the team owns its choice.
- Generated code (protobuf stubs, `*.pyi`, migration files) — exclude from Ruff/mypy via `extend-exclude` instead of "fixing".
- Code that must run on Python <3.8 — modern Ruff/mypy releases drop those targets; pin older tool versions instead.
- When a refactor and a quality cleanup land in the same PR — split them; reviewers can't tell behavioural changes from formatter noise.

## Where it fails / limitations

- **Ruff auto-fix can be lossy.** `ruff check --fix --unsafe-fixes` on `B008` (mutable default arg) or `UP` rewrites can change runtime behaviour. Always run tests after `--fix`.
- **mypy + Django dynamic patterns.** ORM `objects.filter(**kwargs)`, `ForeignKey` reverse accessors, `request.user` typing are weak without `django-stubs`/`mypy-django-plugin`. Strict-mode breaks badly without them.
- **pyright vs mypy disagreement.** Same code, different verdicts on `Optional` narrowing, generics, and `TypedDict` partials. Pick one for CI; using both creates noise.
- **`# type: ignore` rot.** Once an agent adds a few, the count compounds. Need a rule + audit step (`mypy --warn-unused-ignores`) to drive the count down.
- **bandit false positives** on `assert` in tests, `subprocess` with constructed args, `MD5` for non-crypto hashing. Suppress per-line with `# nosec B###` and a justification — not bulk-disable.
- **pre-commit drift.** Tool versions in `.pre-commit-config.yaml` and `pyproject.toml` must match; otherwise contributors and CI report different errors. Easy for agents to skew.
- **Coverage gaming.** `pytest-cov` % is local optimum; agents add tests that touch lines without asserting behaviour. Combine with mutation testing (`mutmut`) for real signal.
- **SOLID/clean-code "smells"** are fuzzy; LLMs over-refactor. Treat structural advice as suggestions, not mechanical fixes.

## Agentic workflow

Run a four-stage pipeline per change: format (`ruff format`) → lint (`ruff check --fix`) → type-check (`mypy` or `pyright`) → security (`bandit`) → tests + coverage (`pytest --cov`). Each stage is a hard gate; on first failure, return diagnostics and stop. The agent never edits config files mid-run — it surfaces violations and proposes a config edit only as a separate step. For PR review, run the same stack on `git diff main..HEAD --name-only`-filtered files to keep feedback scoped.

### Recommended subagents

- `faion-python-developer` — Owns Python tooling config; produces `pyproject.toml` Ruff/mypy sections aligned with the workspace standard.
- `faion-code-quality` — Runs the four-stage pipeline; emits structured findings (file, line, rule, severity, suggested fix).
- `faion-devops-engineer` / `faion-cicd-engineer` — Wires pre-commit, GitHub Actions matrix, coverage upload, branch protection rules.
- `faion-sdd-executor-agent` — Treats "quality gate" as an SDD acceptance criterion: blocks task `done` until all stages pass.
- `faion-improver` — Periodic audits: count `# type: ignore`, complexity hotspots, low-coverage modules; produce remediation tickets.
- General-purpose `Task` subagent for the legacy migration (Black/flake8/isort → Ruff) — large mechanical change, easy to verify.

### Prompt pattern

Per-PR review:

```
Run on changed Python files only:
  ruff format --check; ruff check; mypy <files>; bandit -q -ll <files>; pytest -q --cov.
Emit findings as table: file | line | tool | rule | severity | snippet | fix.
Do NOT auto-edit code. Stop on first hard-gate failure (ruff errors, mypy errors, bandit high).
```

Repo bootstrap:

```
Add Ruff + mypy + bandit + pre-commit to pyproject.toml.
Use rule groups: E, W, F, I, B, C4, UP, SIM, T20 (no print), DJ if Django.
mypy: strict = true on src/, ignore_missing_imports = true.
Install pre-commit; run --all-files once; commit only if zero diff after that run.
Output the proposed pyproject.toml diff first; apply only after approval.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Lint + format (replaces black/isort/flake8/pyupgrade/autoflake/pydocstyle) | https://docs.astral.sh/ruff/ |
| `mypy` | Static type-check | https://mypy.readthedocs.io |
| `pyright` / `pylance` | Faster type-check (Microsoft) | https://microsoft.github.io/pyright/ |
| `bandit` | AST-based security linter | https://bandit.readthedocs.io |
| `pip-audit` | Vulnerability scan of installed deps | https://pypi.org/project/pip-audit/ |
| `safety` | Alternative dep CVE scanner | https://pyup.io/safety/ |
| `pytest` + `pytest-cov` | Test runner + coverage | https://docs.pytest.org / https://pytest-cov.readthedocs.io |
| `coverage` | Lower-level coverage tool | https://coverage.readthedocs.io |
| `mutmut` | Mutation testing (real coverage signal) | https://mutmut.readthedocs.io |
| `pre-commit` | Git hook orchestrator | https://pre-commit.com |
| `interrogate` | Docstring coverage | https://interrogate.readthedocs.io |
| `vulture` | Dead-code finder | https://github.com/jendrikseipp/vulture |
| `radon` / `xenon` | Cyclomatic complexity | https://radon.readthedocs.io |
| `django-stubs` / `djangorestframework-stubs` | mypy plugins for Django | https://github.com/typeddjango |
| `pydantic.mypy` | mypy plugin for Pydantic v1/v2 | https://docs.pydantic.dev/latest/concepts/mypy/ |
| `ruff-action` | GitHub Action wrapper | https://github.com/astral-sh/ruff-action |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes — `astral-sh/ruff-action`, `setup-python`, `actions/cache` | Standard CI runner |
| GitLab CI | SaaS/self-host | Yes — same tools, native pipeline syntax | Mirror of GH workflow |
| Codecov | SaaS | Yes — `codecov-action` uploads `coverage.xml` | PR coverage diff comments |
| Coveralls | SaaS | Yes — REST API + `coveralls` CLI | Alternative to Codecov |
| Sonar / SonarCloud | SaaS | Yes — `sonar-scanner` CLI, supports Ruff/mypy reports | Quality gate aggregation |
| Snyk | SaaS | Yes — `snyk test` CLI | Dep CVE + IaC scanning |
| GitHub Advanced Security (CodeQL) | SaaS | Yes — `github/codeql-action` | Deeper SAST than bandit |
| Semgrep / Semgrep Cloud | SaaS+OSS | Yes — `semgrep ci` | Custom rule writing, agent-friendly DSL |
| Dependabot / Renovate | SaaS | Yes — read `pyproject.toml` + lock | Auto-PRs for dep upgrades |
| Codecov Bundle Analyzer | SaaS | Indirect | Mostly relevant for JS bundles |
| pre-commit.ci | SaaS | Yes — auto-runs `pre-commit run --all-files` on PRs and pushes fix commits | Free for OSS |
| Read the Docs | SaaS | Indirect — runs `interrogate` and `pydocstyle` checks during build | Doc-quality gate |
| Codacy / DeepSource | SaaS | Yes — agent-friendly REST + PR comments | Alternative aggregators |

## Templates & scripts

See `templates.md` for full `pyproject.toml`, `.pre-commit-config.yaml`, GitHub Actions workflows. Inline single-pass quality runner (≤30 lines) used by sub-agents:

```bash
#!/usr/bin/env bash
# qa.sh — full local quality gate. Mirrors CI.
set -euo pipefail
files="${1:-.}"
echo "==> ruff format (check)" && poetry run ruff format --check "$files"
echo "==> ruff check"          && poetry run ruff check "$files"
echo "==> mypy"                && poetry run mypy "$files"
echo "==> bandit"              && poetry run bandit -q -ll -r "$files"
echo "==> pytest + cov"        && poetry run pytest -q --cov --cov-report=term-missing --cov-fail-under=80
echo "==> pip-audit"           && poetry run pip-audit
echo "OK"
```

Per-file diff-scoped runner (≤25 lines) for PR feedback:

```bash
#!/usr/bin/env bash
# qa-diff.sh — only check files changed vs main.
set -euo pipefail
mapfile -t files < <(git diff --name-only --diff-filter=ACMR origin/main...HEAD -- '*.py')
[[ ${#files[@]} -eq 0 ]] && { echo "no python diff"; exit 0; }
poetry run ruff format --check "${files[@]}"
poetry run ruff check          "${files[@]}"
poetry run mypy                "${files[@]}"
poetry run bandit -q -ll        "${files[@]}"
```

## Best practices

- **One config file (`pyproject.toml`)** for Ruff, mypy, pytest, coverage, bandit; no `setup.cfg`, no `.flake8`, no `mypy.ini`.
- **Ruff rule groups** as a base (`E,W,F,I,B,C4,UP,SIM,T20`) plus framework-specific (`DJ` for Django); add narrow rules per repo, never `select = ALL`.
- **`T20` (no print)** in production code — agents that `print(...)` for debugging leak into commits; force `logging`.
- **Strict typing on the public surface** (`src/<pkg>/api/`, `services/`); allow `--no-strict` on legacy modules with a TODO and a ticket.
- **Pre-commit + CI must run the same versions.** Pin in both places; bump via Renovate.
- **Coverage threshold ≥80% on touched files**, not global — global threshold rewards adding trivial tests; per-file rewards covering new code.
- **Treat `# type: ignore[<code>]`** as a code smell; require an inline comment with reason and a `# TODO(name): fix when …`. Run `mypy --warn-unused-ignores` weekly.
- **Bandit allowlist via comments**, not `skips = []` in config; comments document intent at the call site.
- **Do not let agents bulk-`--unsafe-fixes`** on a stale repo. Run safe fixes first, commit, then run `--unsafe-fixes` interactively with tests after each chunk.
- **Run `pre-commit autoupdate` monthly**, not per-commit; otherwise tool churn buries real changes.

## AI-agent gotchas

- **`ruff --fix` masks deeper bugs.** Auto-removed unused vars or simplified comprehensions can hide a logic mistake. Run tests after every `--fix` batch.
- **`# noqa: E501` blanket waivers** propagate. Agents add them to silence Ruff; reviewers miss them. Lint config: forbid bare `# noqa` (require a rule code).
- **mypy `Any` cascades** when an agent fills in unknown types with `Any` "to make it pass". Forbid via `disallow_any_explicit = true` on new files.
- **pyright in editor + mypy in CI** report different errors → infinite loop of fixes that satisfy one but break the other. Pick one for CI authority, use the other only as IDE hint.
- **Agents copy-paste old SOLID examples** with `abc.ABC` boilerplate where Python `Protocol` is idiomatic. Force `typing.Protocol` for structural interfaces.
- **`bandit B404` (subprocess)** flags every shell-out. Agents over-suppress. Allow `subprocess.run(..., check=True, shell=False)` patterns and document.
- **Coverage-driven test generation** by LLMs creates `assert True` and "smoke" tests that hit lines without checking outputs. Reject tests that don't assert on observable state.
- **`pre-commit run --all-files` after every change** is slow on big repos (1000+ files). Agents that loop "edit → run all" stall. Use `pre-commit run --files <changed>` instead.
- **Generated/migration files** (Alembic, Django migrations, gRPC stubs) trigger noisy violations. Always exclude them in Ruff/mypy config; don't suppress per-file.
- **Renaming via Ruff (`UP`/`SIM`)** can break public APIs. For library packages, treat `UP`/`SIM` as warning-only or run only on internal modules.
- **`pip-audit` against a non-locked env** misses transitive pins. Always run after `poetry install --sync` or `pip install -r locked-requirements.txt`.

## References

- Ruff docs: https://docs.astral.sh/ruff/
- Ruff rule reference: https://docs.astral.sh/ruff/rules/
- mypy docs: https://mypy.readthedocs.io
- pyright docs: https://microsoft.github.io/pyright/
- bandit docs: https://bandit.readthedocs.io
- pip-audit: https://github.com/pypa/pip-audit
- pre-commit framework: https://pre-commit.com
- pre-commit.ci: https://pre-commit.ci
- pytest-cov: https://pytest-cov.readthedocs.io
- mutmut: https://mutmut.readthedocs.io
- django-stubs (typed-django): https://github.com/typeddjango/django-stubs
- Pydantic mypy plugin: https://docs.pydantic.dev/latest/concepts/mypy/
- Semgrep Python rules: https://semgrep.dev/p/python
- Codecov: https://about.codecov.io
- Renovate Python: https://docs.renovatebot.com/modules/manager/pep621/
- PEP 8: https://peps.python.org/pep-0008/
- PEP 257 (docstrings): https://peps.python.org/pep-0257/
