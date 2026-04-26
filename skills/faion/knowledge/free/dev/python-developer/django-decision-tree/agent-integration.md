# Agent Integration — Django Decision Tree

## When to use

- Pre-spec stage of a new web/API project where the choice between Django, Django + DRF, Django Ninja, FastAPI, Wagtail, etc. is still open.
- Architecture review of a Django repo that has grown past 50 models — deciding when to introduce a service layer, clean architecture, or DDD-light split.
- Picking the API framework for a new endpoint family inside an existing Django repo (DRF vs Ninja vs raw views) — the tree narrows the option space quickly.
- Database/deployment decisions where the team has mixed prior experience and needs explicit trade-off tables (PostgreSQL vs MySQL vs SQLite + Litestream; VPS vs PaaS vs k8s vs serverless).
- Third-party package vetting — comparing two candidate Django packages by maintenance, compatibility, security, and community signals.
- Code-placement reviews ("which directory does this go in?") during code review of Django PRs.

## When NOT to use

- After spec sign-off with deployment chosen — re-running the tree wastes cycles; only trigger on scope change.
- When the choice is already constrained by infra/team policy (e.g. "must be on Django + Postgres + k8s"); skip the framework branch.
- Tiny scripts, ETL jobs, or single-page admin tools — Django is overkill; the tree's smallest leaf still implies app/project structure.
- Greenfield projects where the bottleneck is product-market fit, not architecture; "fat models, simple views" wins, no decision tree needed.
- For a single feature inside a Django project — use code-placement guidance only, not the full tree.

## Where it fails / limitations

- **Trade-off matrices are static.** The README's tables don't price recent changes (e.g. Django Ninja 1.4+ async middleware, DRF 3.16 token refresh). Agents must verify currency before quoting.
- **No quantitative scoring.** "Use service layer for medium" is fuzzy — agents need a heuristic (e.g. "≥10 services-equivalent business operations" or "≥3 places where the same write happens").
- **Hidden coupling to Postgres.** Many "Django" recommendations (full-text search, ArrayField, JSONB queries) silently assume Postgres; the SQLite/MySQL options downgrade silently.
- **Deployment branch ignores cost.** PaaS picks (Render, Fly, Railway) need cost ceilings to stay honest; the tree treats them as binary.
- **Package evaluation criteria** (maintenance, compatibility, security) are subjective. Agents need URLs/numbers (last commit date, open issue count, GH stars trend) to make defensible calls.
- **Architecture-pattern leap** (fat models → service layer → clean architecture) is presented as a step ladder; in reality, codebases mix layers per app and the tree doesn't model that.
- **No exit ramps.** "FastAPI" appears in the tree but the tree doesn't help once chosen; switch to a different methodology.

## Agentic workflow

Treat the decision tree as a structured questionnaire executed by an orchestrator. The agent walks each branch, asks at most 1-2 questions per node via `AskUserQuestion`, and writes the chosen path + rationale to `.aidocs/product_docs/architecture-decisions.md`. Verify "currency claims" (Django, DRF, Django Ninja versions) with a single `WebFetch` of the official changelog before quoting trade-offs. End with a one-page ADR entry summarising decision + alternatives + risks. Hand off the resulting decisions to `faion-sdd` for the spec and `faion-software-developer` for scaffolding.

### Recommended subagents

- `faion-software-architect` — Owns architecture-pattern decisions (service layer, clean arch, DDD-light); produces the ADR.
- `faion-python-developer` — Validates Django-specific choices (DRF vs Ninja, model layout, package picks) against current versions.
- `faion-devops-engineer` — Validates the deployment branch (VPS vs PaaS vs k8s vs serverless) given budget, ops headcount, and uptime targets.
- `faion-research-agent` (when available) — Provides up-to-date package evaluation (last release, CVEs, downloads) before recommending third-party packages.
- `faion-sdd-executor-agent` — Consumes the ADR and emits the scaffolding tasks (manage.py setup, app split, settings module, base model).
- General-purpose `Task` subagent for code-placement reviews — fed the tree's "where does code go?" rules + the diff.

### Prompt pattern

Architecture decision walk:

```
You are walking the Django Decision Tree.
Inputs: project goals, constraints (team size, budget, timeline, infra), known unknowns.
For each node: state options, ask ≤2 clarifying questions, choose, justify (≤3 bullets).
Verify Django/DRF/Ninja versions from official changelog within last 6 months.
Output: .aidocs/product_docs/architecture-decisions.md with one ADR per node.
Stop on missing input — do not guess. No time estimates anywhere.
```

Package evaluation:

```
For Django package "<name>":
- last release date, open issue count, GH stars trend (1y), CVE count
- Django 5.x compatibility per setup.py / pyproject.toml
- maintainer activity (last 90 days)
Compare against alternative "<name-2>". Recommend with one-line rationale.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `django-admin` | Project/app scaffolding once decision is made | bundled with Django |
| `pip-audit` / `safety` | Vulnerability scan during package vetting | https://pypi.org/project/pip-audit/ |
| `gh` | Inspect a candidate package's GitHub activity (issues, releases) | https://cli.github.com |
| `osv-scanner` | Multi-ecosystem CVE scan (Python + JS + others) | https://github.com/google/osv-scanner |
| `cookiecutter-django` | Scaffold Django repos for the chosen architecture | https://github.com/cookiecutter/cookiecutter-django |
| `pyright` / `mypy` + `django-stubs` | Verify the chosen pattern types cleanly | https://github.com/typeddjango/django-stubs |
| `pgcli` / `mycli` / `litecli` | Quickly validate the chosen DB before commit | https://www.pgcli.com / https://www.mycli.net |
| `flyctl` / `railway` / `render-cli` | Validate the chosen PaaS path with a hello-world deploy | https://fly.io/docs/flyctl/ |
| `kustomize` / `helm` | If the tree picks k8s, generate manifests | https://kustomize.io / https://helm.sh |
| `pipreqs` / `deptree` | Audit existing project dependencies during review | https://github.com/bndr/pipreqs |
| `django-upgrade` | Validate forward-compatibility before locking choice | https://github.com/adamchainz/django-upgrade |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Django Packages (djangopackages.org) | OSS index | Yes — REST + scrape | Primary source for package comparison tables |
| GitHub API | SaaS | Yes — `gh` / REST | Last commit, issue counts, releases for evaluation |
| PyPI JSON API | OSS | Yes — REST | Latest version, classifiers, declared Python/Django support |
| Snyk Advisor | SaaS | Yes — `snyk` CLI + web JSON | Quick package-health score for shortlists |
| Libraries.io | SaaS | Yes — REST | Cross-ecosystem package metadata |
| Render / Railway / Fly.io | PaaS | Yes — CLIs + REST | Validate the PaaS deployment branch |
| Hetzner / DigitalOcean / Linode | IaaS | Yes — REST + CLIs | Validate the VPS branch |
| Google Cloud Run / AWS Lambda / Azure Functions | Serverless | Yes — CLIs | Validate the serverless branch (with ASGI adapter) |
| Postgres flavours: RDS / Cloud SQL / Neon / Supabase | SaaS | Yes — REST/CLI | Validate Postgres choice |
| PlanetScale (MySQL) | SaaS | Yes — CLI | If MySQL branch chosen |
| Litestream | OSS | Yes — CLI | Required if SQLite-in-prod branch chosen |
| Wagtail Cloud | SaaS | Yes — CLI | If "CMS with content editing" branch picked |
| GraphQL Hive / Apollo Studio | SaaS | Yes — CLI | If GraphQL branch chosen (Strawberry/Graphene) |
| Sonar / Codacy / DeepSource | SaaS | Yes — CI integrations | Continuous quality after the decision lands |

## Templates & scripts

See methodology `templates.md` for ADR templates and decision worksheets. Inline package-evaluation script (≤30 lines) for shortlist scoring:

```bash
#!/usr/bin/env bash
# eval-django-pkg.sh <pypi-name>
# Prints: last_release, days_since, gh_stars, gh_open_issues, classifiers Django/Python.
set -euo pipefail
pkg="${1:?pypi name required}"
meta=$(curl -fsSL "https://pypi.org/pypi/${pkg}/json")
ver=$(jq -r .info.version <<<"$meta")
upload=$(jq -r ".releases[\"$ver\"][0].upload_time" <<<"$meta" | cut -dT -f1)
days=$(( ( $(date +%s) - $(date -d "$upload" +%s) ) / 86400 ))
home=$(jq -r '.info.project_urls.Source // .info.project_urls.Homepage // .info.home_page' <<<"$meta")
classifiers=$(jq -r '.info.classifiers[]' <<<"$meta" | grep -E "Framework :: Django|Programming Language :: Python ::" | sort -u)
printf '%-30s ver=%s last=%s (%dd ago)\n' "$pkg" "$ver" "$upload" "$days"
printf 'home: %s\n' "$home"
printf 'classifiers:\n%s\n' "$classifiers"
if [[ "$home" =~ github.com/([^/]+)/([^/?#]+) ]]; then
  gh api "repos/${BASH_REMATCH[1]}/${BASH_REMATCH[2]}" \
    --jq '{stars:.stargazers_count, open_issues:.open_issues_count, archived:.archived, default_branch:.default_branch}'
fi
```

ADR skeleton (`.aidocs/product_docs/adr/NNN-<slug>.md`):

```markdown
# ADR-NNN: <decision title>
## Context
## Options considered
- A: …
- B: …
## Decision
## Consequences (good / bad)
## Risks & mitigations
## Revisit when
```

## Best practices

- **One ADR per branch of the tree** that produced a non-trivial decision; cheap to write, cheap to revisit.
- **Tie every package recommendation to numbers**: last release ≤180 days, open issue count <X% of stars, declared Django 5.x classifier, no high CVEs in `pip-audit`.
- **Pick the smallest pattern that fits.** Default to "fat models + simple views" until you have ≥3 places duplicating a write — only then introduce a service layer.
- **Default DB = Postgres**, default queue = Celery + Redis, default deploy = PaaS, default API framework = DRF. Deviate only with an ADR.
- **Reject "use clean architecture" decisions** without two concrete examples of how it pays off in this codebase. Otherwise the abstraction tax dominates.
- **Code-placement rule of thumb**: pure functions in `utils/`, side-effects in `services/`, serialization in `serializers/`, HTTP shape in `views/`, persistence in `models/`, async/scheduled work in `tasks/`. Anything that smells reusable gets a `core/`/`common/` home only after the second use.
- **Migrations as ADRs.** Big schema changes (UUID switch, table partitioning, FK on_delete swap) deserve their own ADR even if the tree doesn't ask.
- **Recheck the tree after major version bumps** (Django LTS, Python EOL) — branches age fast.

## AI-agent gotchas

- **Stale comparison tables.** LLMs quote "Django Ninja vs DRF" articles from 2023; both projects moved. Force a `WebFetch` of the official changelog within last 6 months before recommending.
- **Confusing Django Ninja with FastAPI.** They share idioms but have different ORM stories; agents conflate, then write FastAPI-style migrations on Django Ninja and break.
- **"Best" without context.** Agents will pick a winner even when constraints aren't specified. Force the orchestrator to require team size, ops budget, and traffic profile before answering.
- **Recommending plugins you can't audit.** Agents reach for the first stars-rich package; check archive flag, last commit, security advisories before suggesting.
- **DDD/clean-architecture cargo-cult.** Agents over-stack abstractions on small Django apps. Hard rule: no domain/app/services/repository split unless there are ≥10 entities.
- **Mixing API framework choices** in one repo (DRF on `/api/v1`, Ninja on `/api/v2`) silently doubles auth, throttling, schema docs. Treat as a top-level ADR if introduced.
- **Deployment-tree leaks.** "Use serverless" pick by an agent that doesn't notice Django's long-running celery dependency. Always check the queue/cron requirement before picking serverless.
- **No revisit clause.** Agents skip the "revisit when" section. Force it: every ADR must list ≥1 trigger that invalidates the decision.
- **Code-placement drift.** Agents create `helpers.py`, `mixins.py`, `utilities.py`, `common.py` that all mean the same thing. Pin one name per project and reject the rest at review.
- **Database choice masking.** Agent picks SQLite "for simplicity" without flagging that JSONB-style queries, full-text, partial indexes will need rewriting. Always emit a "what you give up" list.

## References

- Methodology README: `./README.md`
- Django docs: https://docs.djangoproject.com/
- Django 5.2 release notes: https://docs.djangoproject.com/en/5.2/releases/5.2/
- Django REST Framework: https://www.django-rest-framework.org/
- Django Ninja: https://django-ninja.dev/
- Wagtail: https://wagtail.org/
- Strawberry GraphQL: https://strawberry.rocks/
- Architecture Patterns with Python (cosmicpython): https://www.cosmicpython.com/
- Two Scoops of Django: https://www.feldroy.com/books/two-scoops-of-django-5-0
- Django Packages index: https://djangopackages.org/
- Django on Cloud Run: https://cloud.google.com/python/django/run
- Django on k8s: https://cloud.google.com/python/django/kubernetes-engine
- Litestream (SQLite replication): https://litestream.io
- ADR templates (Michael Nygard): https://github.com/joelparkerhenderson/architecture-decision-record
- Snyk Advisor: https://snyk.io/advisor/
- Libraries.io: https://libraries.io/
- pip-audit: https://github.com/pypa/pip-audit
- django-stubs: https://github.com/typeddjango/django-stubs
