# pnpm Package Management

## Summary

**One-sentence:** Produces a reproducible pnpm setup — packageManager pin via corepack, committed pnpm-lock.yaml, no shamefully-hoist, .pnpmfile.cjs for phantom deps, workspace:* protocol, CI --frozen-lockfile gate.

**One-paragraph:** Pin the pnpm version in root package.json `packageManager` field (corepack-managed). Always commit `pnpm-lock.yaml`. Keep `shamefully-hoist=false`; fix phantom-dep issues with the `readPackage` hook in `.pnpmfile.cjs`, never with hoisting. Reference internal packages by `workspace:*`; Changesets rewrites to real versions at publish. CI runs `pnpm install --frozen-lockfile` and caches the pnpm store keyed by `pnpm-lock.yaml` hash.

**Ефективно для:** new repos / monorepos adopting pnpm, migrations from npm/yarn where lockfile drift wastes hours, services suffering from phantom dependencies, CI suites with slow install times.

## Applies If (ALL must hold)

- JS/TS project on Node 18+.
- Team accepts pnpm as the package manager.
- CI can run corepack + pnpm.
- Monorepo with internal packages, OR single repo wanting reproducible installs.

## Skip If (ANY kills it)

- Project mandated to use npm or yarn for compliance reasons.
- Single-tool ecosystem (e.g. Deno) that doesn't need npm-shaped lockfiles.
- Plugin that ships as zero-dep (no install step).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| pnpm version | semver string (e.g. `9.6.0`) | pnpm release notes |
| Node engines | `>=20.x` | infra |
| CI provider | string | infra ADR |
| Workspaces (if any) | YAML pnpm-workspace.yaml | repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[javascript]]` | TS+lint+test stack interacts with the package manager. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: packageManager pin, no shamefully-hoist (with the narrow node-linker escape), workspace:*, frozen-lockfile in CI, committed lockfile, `only-allow pnpm` preinstall guard, lockfile in its own commit | ~900 |
| `content/02-output-contract.xml` | essential | Required files (package.json packageManager, .npmrc, .pnpmfile.cjs) + CI fields | ~500 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: unpinned pnpm, shamefully-hoist=true, npm install in CI, missing lockfile, two lockfiles side by side, `pnpm patch` without `patch-commit` | ~700 |
| `content/04-procedure.xml` | essential | 6-step conversion: audit → pin → .npmrc → block other managers → CI → validate | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "JS/TS project where pnpm is acceptable?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate configs | haiku | Boilerplate. |
| Migration from npm/yarn | sonnet | Lockfile conversion. |
| Phantom-dep diagnosis | opus | Multi-package reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/npmrc` | .npmrc with `engine-strict=true`, `strict-peer-dependencies=false` (or true if team accepts). |
| `templates/pnpm-bootstrap.sh` | Bootstrap script — corepack enable + install + verify. |
| `templates/gh-actions-ci.yml` | GitHub Actions CI with pnpm cache + frozen-lockfile, plus the `--filter '...[origin/main]'` monorepo variant. |
| `templates/dockerfile-pnpm` | Multi-stage Dockerfile using `pnpm fetch` so the dependency layer caches on the lockfile alone. |
| `templates/pnpm-workspace.yaml` | Workspace definition for an apps / packages / tools layout. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pnpm-package-management.py` | Verifies packageManager field, lockfile presence, no shamefully-hoist in any .npmrc. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[javascript]]` — broader TS/JS standards

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters on pnpm acceptability and corepack support, then branches by repo shape: a publishing monorepo lands on the `workspace:*` rule (published via `pnpm publish`, never `npm publish`), and a repo with native add-ons lands on the hoisting rule and its narrow `node-linker=hoisted` escape.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/npmrc`

```text
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false
engine-strict=true
lockfile=true
prefer-frozen-lockfile=true
registry=https://registry.npmjs.org/
# Private scoped registry example:
# @mycompany:registry=https://npm.mycompany.com/
```

### `templates/pnpm-bootstrap.sh`

```bash
# pnpm-bootstrap.sh — initialise a pnpm-pinned project safely.
# Usage: PNPM_VERSION=9.12.0 NODE_VERSION=20 ./pnpm-bootstrap.sh
set -euo pipefail
PNPM_VERSION="${PNPM_VERSION:-9.12.0}"
NODE_VERSION="${NODE_VERSION:-20}"

corepack enable
corepack prepare "pnpm@${PNPM_VERSION}" --activate

[ -f package.json ] || pnpm init

# Pin the toolchain
node -e "
  const fs=require('fs'); const p=JSON.parse(fs.readFileSync('package.json'));
  p.packageManager='pnpm@${PNPM_VERSION}';
  p.engines={node:'>=${NODE_VERSION}.0.0', pnpm:'>=${PNPM_VERSION%.*}.0'};
  p.scripts={...(p.scripts||{}), preinstall:'npx only-allow pnpm'};
  fs.writeFileSync('package.json', JSON.stringify(p,null,2)+'\n');
"

cat > .npmrc <<'EOF'
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false
engine-strict=true
prefer-frozen-lockfile=true
EOF

# Workspace marker (update packages list as needed)
[ -f pnpm-workspace.yaml ] || printf 'packages:\n  - "apps/*"\n  - "packages/*"\n' > pnpm-workspace.yaml

pnpm install
echo "pnpm workspace initialized with pnpm@${PNPM_VERSION}"
```

### `templates/gh-actions-ci.yml`

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Typecheck
        run: pnpm typecheck

      - name: Lint
        run: pnpm lint

      - name: Test
        run: pnpm test

      - name: Build
        run: pnpm build
```
