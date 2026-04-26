# Agent Integration — Django Code Quality Tools

## When to use
- Bootstrapping a Django project: drop in `pyproject.toml` + `.pre-commit-config.yaml` before first commit.
- Migrating an old Django repo to a modern toolchain (replacing `black + isort + flake8` with `ruff`).
- Onboarding agents to a Django codebase — they need a deterministic format/lint baseline so diffs are about logic, not whitespace.
- Adding type-checking gradually — `mypy` + `django-stubs` introduced module by module.
- CI quality gate that blocks PRs failing format/lint/type/security.

## When NOT to use
- Non-Django Python projects — drop the `mypy_django_plugin` and `DJ` rule set; the rest still applies.
- Single-script utilities where pre-commit ceremony exceeds the code itself.
- Legacy migrations that ruff/mypy will mass-rewrite — gate them with `--diff` first or you'll merge a 5,000-line "format" PR that obscures real changes.

## Where it fails / limitations
- The README still pins `black + isort + flake8`; modern equivalent is `ruff format` + `ruff check` (one tool, faster, fewer config files). Treat the README as historical and steer agents to ruff.
- `mypy` + Django is fragile: querysets are typed loosely, `Manager.get_or_create()` returns `tuple[Model, bool]` only with stubs, custom managers need `from_queryset` + explicit annotation.
- Pre-commit doesn't run in CI by default — must be wired with `pre-commit run --all-files` job.
- `flake8` extensions (bugbear, comprehensions) overlap with ruff rules; running both wastes time.
- `bandit`/`pip-audit` produce false positives in Django (e.g., `assert` in tests flagged as B101) — agents will silence with `# noqa` blanket instead of fixing.

## Agentic workflow
A bootstrap subagent writes `pyproject.toml`, `.pre-commit-config.yaml`, `mypy.ini` in one pass and commits before any feature work. A pre-commit fix-loop subagent runs `ruff check --fix && ruff format` and re-stages on every diff. A type-debt subagent works module-by-module to enable `strict = True` mypy in `[[tool.mypy.overrides]]` blocks; never set repo-wide strict at once. CI runs `ruff` (fast), `mypy` (slower, can be on a schedule), and `pip-audit` weekly. Reviewer subagent rejects PRs with `# type: ignore` without an explanation comment.

### Recommended subagents
- `faion-sdd-execution` — quality gates already include format/lint/type checks.
- `password-scrubber-agent` — pairs with `bandit` for secret detection.
- A `quality-bootstrap` subagent (custom) — input: empty repo or repo with old toolchain; output: modern `pyproject.toml` + `.pre-commit-config.yaml` + initial `pre-commit run --all-files` commit.
- A `mypy-incremental` subagent — adds one module to strict mypy at a time, fixing errors as they surface.

### Prompt pattern
```
Bootstrap quality tooling for this Django project. Output:
1. pyproject.toml with [tool.ruff], [tool.ruff.lint] (select E/F/I/B/UP/SIM/DJ/T20/PT/RUF), [tool.ruff.format], [tool.mypy] (with django-stubs).
2. .pre-commit-config.yaml with ruff, ruff-format, end-of-file-fixer, trailing-whitespace, check-yaml hooks. NO black, NO isort, NO flake8.
3. CI step: `pre-commit run --all-files`.
Run pre-commit on the whole repo and fix any errors that auto-fix can resolve.
```

```
Audit `# type: ignore` and `# noqa` comments. Each must have:
- The specific rule code (e.g. `# type: ignore[arg-type]`, `# noqa: B902`).
- A trailing comment explaining why.
Block PR for blanket suppressions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff` | Format + lint (replaces black/isort/flake8) | https://docs.astral.sh/ruff |
| `mypy` | Static typing | https://mypy.readthedocs.io |
| `django-stubs` | Type stubs for Django | https://github.com/typeddjango/django-stubs |
| `djangorestframework-stubs` | Type stubs for DRF | https://github.com/typeddjango/djangorestframework-stubs |
| `bandit` | Security linter | https://bandit.readthedocs.io |
| `pip-audit` | CVE scanner for installed packages | https://pypi.org/project/pip-audit/ |
| `safety` | Alternative CVE scanner | https://pyup.io/safety/ |
| `pre-commit` | Hook orchestrator | https://pre-commit.com |
| `python manage.py check --deploy` | Django's built-in production audit | Django docs |
| `coverage.py` / `pytest-cov` | Coverage with branch tracking | https://coverage.readthedocs.io |
| `django-upgrade` | Auto-rewrite to current Django idioms | https://github.com/adamchainz/django-upgrade |
| `pyupgrade` | Auto-rewrite to current Python idioms (now part of ruff `UP`) | https://github.com/asottile/pyupgrade |
| `djhtml` | Format Django templates | https://github.com/rtts/djhtml |
| `djade` | Modernize template syntax | https://github.com/adamchainz/djade |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | yes | Run `pre-commit run --all-files` + `pytest` matrix per Python version. |
| Codecov / Coveralls | SaaS | yes | Coverage delta on PR. |
| Snyk / GitHub Dependabot | SaaS | yes | Continuous CVE alerts; complement pip-audit. |
| Sentry | SaaS | yes | Pairs with quality gates: lint/type errors caught locally, runtime errors in Sentry. |
| Sourcery / CodeRabbit / GitHub Copilot review | SaaS | yes | AI review augments human reviewer. |
| Posit Connect / Cloudflare Pages | SaaS | partial | If publishing internal type-coverage dashboards. |

## Templates & scripts
The README has an older `pyproject.toml` snippet (black+isort+flake8). Modern replacement aligned with current best practice:

```toml
# pyproject.toml — modern Django quality stack
[tool.ruff]
target-version = "py311"
line-length = 100
extend-exclude = ["migrations"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "DJ", "T20", "PT", "RUF", "S"]
ignore = ["E501", "S101"]  # E501 handled by formatter, S101 allow assert in tests

[tool.ruff.lint.per-file-ignores]
"**/tests/*.py" = ["S105", "S106"]
"**/settings/*.py" = ["S105"]

[tool.ruff.lint.isort]
known-first-party = ["apps", "core", "config"]

[tool.mypy]
python_version = "3.11"
plugins = ["mypy_django_plugin.main"]
strict = false
warn_unused_ignores = true
warn_redundant_casts = true

[tool.django-stubs]
django_settings_module = "config.settings.development"
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
```

## Best practices
- One source of style truth: `ruff` config in `pyproject.toml`. Don't keep a `.flake8` lying around.
- Run `pre-commit run --all-files` once at adoption, commit the format pass alone, then start feature work — keeps history readable.
- mypy strictness ratchets up per module via overrides; never flip global `strict = true` in a legacy repo.
- Bandit results: triage and either fix or add a per-line `# nosec B<id> reason: ...` comment.
- `python manage.py check --deploy` in production-facing CI catches misconfigured `DEBUG`, `ALLOWED_HOSTS`, `SECURE_*` flags.
- Coverage threshold: start at current measured value, raise in increments. Setting 100% from day one drives gaming.
- Run `pip-audit` weekly via scheduled GHA — daily is noisy, monthly is too late.

## AI-agent gotchas
- Agents will leave the README's outdated `black + isort + flake8` setup intact when generating new projects. Anchor prompts to "Use ruff (format + lint), no black/isort/flake8".
- Agents add `# type: ignore` to silence mypy on first error rather than fix it. Reviewer subagent must enforce explanatory comment.
- `mypy_django_plugin` requires `DJANGO_SETTINGS_MODULE` set in `[tool.django-stubs]`; agents set it as env var only and CI fails.
- Agents add `noqa: E501` everywhere instead of letting the formatter wrap lines. Use `line-length` consistently and remove blanket noqa.
- pre-commit hook revisions go stale — agents won't bump unless prompted. Use `pre-commit autoupdate` quarterly.
- Bandit "high severity" hits on `subprocess.call(..., shell=True)` are usually real; don't let agents suppress without code review.
- Human-in-loop: dependency upgrades (mypy major, ruff version) need human triage because rule changes can mass-flag working code.
- When agent edits `settings/base.py`, force `python manage.py check --deploy` in CI — easy to introduce config regressions silently.

## References
- https://docs.astral.sh/ruff — Ruff (format + lint)
- https://github.com/typeddjango/django-stubs — Django typing
- https://github.com/typeddjango/djangorestframework-stubs — DRF typing
- https://docs.djangoproject.com/en/stable/ref/django-admin/#check — `manage.py check`
- https://bandit.readthedocs.io — Bandit
- https://pypi.org/project/pip-audit/ — pip-audit
- https://pre-commit.com — pre-commit framework
- https://github.com/HackSoftware/Django-Styleguide — companion styleguide that pairs with this toolchain
