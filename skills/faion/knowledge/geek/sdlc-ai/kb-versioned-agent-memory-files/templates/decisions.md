# decisions.md

Append-only log of project-level technical decisions an agent must respect.

Schema per entry:

```
## YYYY-MM-DD — <one-line title>
**Decision.** <one-paragraph statement of the choice>
**Why.** <rationale; cite empirical anchor>
**Alternatives.** <list rejected options + reason>
**Citation.** commit:<sha> · ticket:<id> · pr:<url>
```

---

## 2026-04-26 — Standardise on uv >= 0.4
**Decision.** Repo uses `uv` for Python; `uv.lock` is committed; CI installs from the lockfile only.
**Why.** Mixed `pip-tools` + `uv` envs caused 3 build breaks in two weeks; uv 0.4 lockfile format is required by our `uv sync --frozen` flag.
**Alternatives.** Stay on `pip-tools` (rejected: slower, no inline deps); use `poetry` (rejected: existing repos already on uv).
**Citation.** commit:9f3ac1a · ticket:NERO-412
