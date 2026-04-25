# Agent Integration — Django Code Quality

Methodology covers Django code quality across linting (Ruff), type checking (mypy + django-stubs), security (Django 6.0+ CSP, django-axes, django-ratelimit), performance (debug toolbar, silk, select_related/prefetch_related), and observability (structlog, Sentry). Use this file when an agent sets up quality gates, audits a Django app, or remediates findings.

## When to use
- New Django project — wire pre-commit + ruff + mypy + django-stubs + Sentry on day one.
- Quality audit of an existing project — run a checklist sweep, file issues per dimension.
- N+1 hunt — debug toolbar / silk / nplusone instrumentation, then fix with `select_related`/`prefetch_related`.
- Security hardening before launch — CSP headers, brute-force protection, rate limiting, input validation review.
- Logging migration — stdlib `logging` to `structlog` with JSON output for cloud log aggregation.
- CI gate setup — block PRs on ruff, mypy, security scan, coverage threshold.

## When NOT to use
- Throwaway prototypes — full quality stack costs more than the prototype is worth; use ruff alone.
- Codebases on Django < 4.2 — examples assume 6.0 features (native CSP, async views) that don't backport.
- Pure data pipelines without HTTP — security stack (CSP, rate limiting) doesn't apply.
- Internal admin-only tools — much of the security stack is external-facing; relax for trusted networks.
- Legacy projects under feature freeze — ROI on adding quality tooling is low; reserve for rewrites.

## Where it fails / limitations
- README's "Performance Stack" lumps debug toolbar (dev) with Sentry (prod) and django-silk (heavy) — agents enable silk in prod and 2x request latency.
- `select_related` vs `prefetch_related` rule of thumb is correct, but doesn't cover `prefetch_related_objects` for already-fetched querysets.
- django-axes config example missing IP-aware lockout vs username-aware — agents lock out shared NAT pools.
- django-ratelimit covers per-view but not per-API endpoint with DRF throttle classes (preferred for DRF projects).
- structlog setup is shown but no migration path from existing `logging` calls — agents end up with a hybrid that's worse than either alone.
- Sentry section assumes SaaS — self-hosted (OSS Sentry, GlitchTip) needs different DSN handling.
- mypy + django-stubs + DRF: DRF's serializer typing is incomplete; agents add `# type: ignore[misc]` everywhere instead of fixing root cause.
- No coverage of `bandit` (or ruff `S` rules) for security-specific lints — agents miss subprocess/pickle issues.

## Agentic workflow
Bootstrap: (1) install ruff + mypy + django-stubs + pre-commit + sentry-sdk, (2) `pyproject.toml` with ruff (E/F/I/B/UP/N/S/C4/PT/DJ rules), mypy strict + django-stubs plugin, (3) pre-commit hooks: ruff, mypy on touched files, secrets scan, (4) settings: CSP middleware, axes, structlog config, sentry init, (5) per-app security review checklist. Audit existing: (a) run `ruff check .` and `mypy --strict apps/`, (b) install debug toolbar + silk, capture top 10 slow endpoints, (c) profile for N+1 with `nplusone`, (d) review security checklist, (e) file issues per dimension.

### Recommended subagents
- `faion-devtools-developer` — Owns ruff/mypy/pre-commit/CI config, version pins.
- `faion-software-architect` — Reviews layering, decides quality thresholds, security model.
- `faion-code-agent` — Applies remediations (N+1 fixes, type annotations, security hardening).
- `faion-test-agent` — Writes regression tests for security findings (auth bypass, SQL injection vectors).
- `faion-improver` — Session loop: audit → prioritize → fix → log → commit.
- `faion-sdd-execution` — Quality gates per PR.

### Prompt pattern

Quality audit:

```
Audit Django app apps/<app>/ per
free/dev/python-developer/django-quality/README.md.
Produce a markdown report with sections:
  1. Lint — `ruff check apps/<app>/` output, count by rule.
  2. Types — `mypy --strict apps/<app>/` output, count by error code.
  3. N+1 — top 5 endpoints by query count (run debug toolbar / silk).
  4. Security — checklist results: CSP, CSRF, auth backends, input validation,
     S-rule findings.
  5. Logging — list of `print()` (T20), `logger.info` without structured context.
  6. Performance — list of querysets without select_related/prefetch_related on FKs.
For each finding: severity (high/med/low), file:line, suggested fix.
Do NOT apply fixes — report only.
```

Fix N+1:

```
Fix N+1 queries in apps/<app>/<file>.py per
free/dev/python-developer/django-quality/README.md.
For each queryset:
  - FK access in loop → add .select_related('fk_field').
  - Reverse FK / M2M access in loop → add .prefetch_related('related_set').
  - Already-fetched objects → use Prefetch(...) with custom queryset or `prefetch_related_objects`.
Add or extend assertNumQueries test in tests/test_<file>.py to lock the query count.
Verify: `pytest tests/test_<file>.py -v` and `python manage.py shell -c "..."` smoke.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ruff check` (E/F/I/B/UP/N/S/C4/PT/DJ) | Lint + format | https://docs.astral.sh/ruff |
| `mypy --strict` + `django-stubs` | Type-check Django ORM | https://github.com/typeddjango/django-stubs |
| `bandit` (or ruff `S`) | Security lints (subprocess, pickle, asserts in prod) | https://bandit.readthedocs.io |
| `pip-audit` / `safety` | Dependency CVE scan | https://pypi.org/project/pip-audit |
| `python manage.py check --deploy` | Built-in production-readiness check | https://docs.djangoproject.com/en/stable/ref/checks/ |
| `python manage.py makemigrations --check --dry-run` | CI gate against missing migrations | bundled |
| `django-axes` | Brute-force lockout | https://django-axes.readthedocs.io |
| `django-ratelimit` | Per-view rate limit | https://django-ratelimit.readthedocs.io |
| `django-silk` | Request profiler (web UI) | https://github.com/jazzband/django-silk |
| `django-debug-toolbar` | Dev profiling, queries, templates | https://django-debug-toolbar.readthedocs.io |
| `nplusone` | N+1 auto-detection | https://github.com/jmcarp/nplusone |
| `django-extensions show_urls` | URL graph dump | https://django-extensions.readthedocs.io |
| `structlog` + `django-structlog` | Structured logging | https://django-structlog.readthedocs.io |
| `sentry-sdk[django]` | Error tracking | https://docs.sentry.io/platforms/python/guides/django/ |
| `import-linter` / `tach` | Architecture lints | https://import-linter.readthedocs.io |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Sentry | SaaS | Yes — Django integration auto-instruments | Self-hosted variant available |
| GlitchTip | OSS Sentry alt | Yes — same SDK | Self-host for cost control |
| Datadog APM | SaaS | Yes — `ddtrace-run` | Per-request traces |
| Honeycomb | SaaS | Yes — OTel | Tail sampling for cost |
| Snyk / Dependabot | SaaS | Yes — PR-driven CVE alerts | GitHub-native |
| GitHub Code Scanning | SaaS | Yes — CodeQL on push | Free for public repos |
| pre-commit.ci | SaaS hook runner | Yes | Auto-fix PRs on push |
| Codecov | SaaS coverage | Yes | PR coverage delta gates |
| Mozilla Observatory | Free scanner | Yes (manual) | HTTP header / TLS audit |

## Templates & scripts

See `templates.md` for full pre-commit, ruff, mypy configs. Add this `python manage.py check --deploy` CI script (≤45 lines):

```bash
#!/usr/bin/env bash
# scripts/quality-gate.sh — Django pre-deploy quality gate.
set -euo pipefail
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.production}"

echo "==> ruff (lint + format check)"
ruff check . --no-fix
ruff format --check .

echo "==> mypy --strict on apps/"
mypy --strict apps/

echo "==> Django deploy checks"
python manage.py check --deploy --fail-level WARNING

echo "==> Missing migrations?"
python manage.py makemigrations --check --dry-run

echo "==> Dependency CVE scan"
pip-audit --strict || { echo "FAIL: pip-audit found vulnerable deps"; exit 1; }

echo "==> Tests + coverage"
pytest -n auto --cov=apps --cov=core --cov-fail-under=80 --cov-branch

echo "==> Quality gate passed."
```

## Best practices
- **One config source: `pyproject.toml`** — ruff, mypy, pytest, coverage all under `[tool.*]`. No legacy `setup.cfg`.
- **Pre-commit on developers, ruff/mypy on CI on changed files**, full sweep on `main` nightly. Dev iteration stays fast.
- **`mypy --strict` per-module incrementally** — allowlist in `[tool.mypy]` `files = [...]` or per-module overrides. Don't run repo-wide `--strict` from day 1.
- **`django-stubs` requires `django_settings_module`** in `[tool.django-stubs]`. Without it, errors are spurious.
- **CSP via Django 6.0 native** for new projects; `django-csp` only when fine-grained control is needed (e.g., per-view nonces).
- **Rate limit DRF endpoints with `DEFAULT_THROTTLE_CLASSES`**, not `django-ratelimit` decorators — DRF's stack is more idiomatic in DRF projects.
- **Structured logging with `structlog`** + `django-structlog` for request context middleware. Send JSON to stdout; cloud platforms ingest natively.
- **Sentry `traces_sample_rate` low in prod** (0.1) and `profiles_sample_rate` (0.1) — full sampling is expensive.
- **N+1 prevention**: enable `nplusone` middleware in dev only; CI runs sample requests with it on.
- **`select_related` for FK / OneToOne (single SQL JOIN)**, `prefetch_related` for M2M / reverse FK / GFK (extra SQL). Apply at selector level so views don't worry.
- **`assertNumQueries` regression tests** on hot endpoints — locks query count, catches accidental N+1 reintroduction.
- **`bandit` / ruff `S` selective**: relax `S101` (asserts) in tests, keep strict in prod code; `S603` (subprocess) needs review per case.
- **`makemigrations --check --dry-run` in CI** — catches engineers who edited models without generating the migration.

## AI-agent gotchas
- **`select_related` on a NULL FK**: outer join is correct but multiplies rows when chained — agents profile and miss the cost.
- **`prefetch_related` does NOT use the connection from the original query** — large prefetches can hit a different DB replica with different visibility.
- **`Prefetch(...)` with custom queryset** must filter on the related model, not the parent — agents reverse and get empty results.
- **`@ratelimit` decorator vs DRF throttles** — both work, but stacking double-counts; pick one per project.
- **`django-axes` and django-ratelimit** ignore `X-Forwarded-For` unless `AXES_IPWARE_PROXY_COUNT` and `RATELIMIT_USE_CACHE` are configured. Agents test locally (no proxy) and ship broken.
- **CSP nonces**: `django-csp` requires regenerating per request; caching responses breaks CSP — agents add Cloudflare cache and lose CSP integrity.
- **structlog and stdlib logging mixed** — without `ProcessorFormatter`, half the logs are unstructured. README does not show the bridge.
- **Sentry `before_send` filter** that drops PII can also drop critical errors if too aggressive — agents over-filter.
- **`debug_toolbar` middleware in prod** if `DEBUG=True` slips through — exposes secrets via SQL panel. Use `INTERNAL_IPS` whitelisting always.
- **`silk` profiles every request** by default — toggle with `SILKY_INTERCEPT_PERCENT = 1` for low overhead.
- **`mypy_django_plugin` + DRF** needs `drf-stubs` (separate install) for serializer typing.
- **`pip-audit` + private PyPI mirrors** without `--index-url` config silently passes (no DB to check). Configure explicitly.
- **Coverage on `if settings.DEBUG:`** branches — code only runs locally, never in CI; agents see uncovered and add tests that mock settings (incorrect approach). Use `# pragma: no cover`.
- **`ruff` rule `DJ001`** (avoid `null=True` on string-based fields) is good but conflicts with legacy DBs — relax per-file.
- **`makemigrations --check`** fails when there's a model field default that's a callable evaluated at migration time — agents add `lambda: ...` and break replay.

## References
- README: `./README.md`
- Sibling: `../django-coding-standards/`, `../django-imports/`, `../python-code-quality/`, `../python-type-hints/`
- Django checks: https://docs.djangoproject.com/en/stable/ref/checks/
- Django CSP (6.0+): https://docs.djangoproject.com/en/stable/ref/csp/
- django-stubs: https://github.com/typeddjango/django-stubs
- django-axes: https://django-axes.readthedocs.io
- django-ratelimit: https://django-ratelimit.readthedocs.io
- django-silk: https://github.com/jazzband/django-silk
- django-debug-toolbar: https://django-debug-toolbar.readthedocs.io
- nplusone: https://github.com/jmcarp/nplusone
- structlog: https://www.structlog.org/
- django-structlog: https://django-structlog.readthedocs.io
- Sentry Django: https://docs.sentry.io/platforms/python/guides/django/
- ruff DJ rules: https://docs.astral.sh/ruff/rules/#flake8-django-dj
- ruff S rules: https://docs.astral.sh/ruff/rules/#flake8-bandit-s
- pip-audit: https://pypi.org/project/pip-audit/
