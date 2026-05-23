# pnpm Workspaces with Dependency Catalogs

## Summary

**One-sentence:** Use pnpm 9+ workspaces with the `catalog:` protocol to share external dependency versions across packages; internal packages link via `workspace:*`; CI runs filtered tests with `--filter ...[origin/main]`.

**One-paragraph:** TypeScript / JavaScript monorepos fight "package X wants react@19.0, package Y wants react@19.1" drift indefinitely without a shared-version mechanism. pnpm 9+ catalogs solve this by construction: one entry in `pnpm-workspace.yaml` controls the version of `react`, `typescript`, `vitest`, etc., for every workspace package; every `package.json` references those entries with `"react": "catalog:"`. Internal packages link via `"workspace:*"`. This methodology produces a `pnpm-workspace.yaml` artefact (catalog + workspaces) plus the per-package.json fragment that consumes it.

**Ефективно для:**

- Monorepo з двома+ packages, де React/TS/Vitest версії розповзаються.
- Microfrontend / shared-library workspace, де consistency — audit concern.
- Repo з паралельними AI агентами в worktrees — кожен додає dep незалежно.
- CI що хоче запускати тільки affected packages (`--filter ...[origin/main]`).

## Applies If (ALL must hold)

- Repo has &gt;=2 workspace packages.
- Repo uses (or can switch to) pnpm 9 or newer.
- Two or more packages share at least one external dep (React, TypeScript, Vitest, etc.).
- Team is willing to enforce the catalog rule via lint or pre-commit.

## Skip If (ANY kills it)

- Single-package app — npm or Bun is enough; catalogs add ceremony.
- Bun-native runtime project that needs `bun.lockb` parity with the runtime.
- Yarn 4 PnP shop with working constraints — migration cost rarely wins.
- Hybrid setup that must publish to npm with classic `dependencies` (publish step must replace `catalog:` and `workspace:*` first).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| pnpm-workspace.yaml | YAML | lead |
| Per-package package.json | JSON | per-package owner |
| pnpm 9+ installed | binary | platform |
| CI runner | GitHub Actions / GitLab CI | ci-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Pre-commit hook can lint hard-coded shared deps. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `catalog_design` | sonnet | Which deps are shared, which package-local — needs judgement. |
| `package_json_rewrite` | haiku | Mechanical replacement of versions with `catalog:`. |
| `ci_filter_setup` | haiku | Boilerplate `--filter ...[origin/main]` wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pnpm-workspace.yaml` | Sample pnpm-workspace.yaml with catalog + named catalogs. |
| `templates/package-json-fragment.json` | Per-package package.json fragment referencing `catalog:` and `workspace:*`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pnpm-catalogs.py` | Validate produced pnpm-workspace.yaml + package.json catalog refs. | pre-merge of workspace config |

## Related

- [[pyproject-single-source]]
- [[lint-precommit-floor]]
- [[lint-staged-only-not-whole-tree]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (workspace package count, pnpm version, shared dep count) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to introduce catalogs — the tree terminates either on the active rule or on `skip-this-methodology`.
