# Agent Integration — pnpm Package Management

## When to use
- Any time an agent installs / updates / audits Node deps in a repo whose `packageManager` field is `pnpm`.
- Monorepo work: agent must use `pnpm --filter` + workspace protocol, not bare `npm install` in a sub-package.
- CI/CD setup: agent generates GH Actions / Dockerfile that uses `pnpm install --frozen-lockfile`.
- Migrating an `npm`/`yarn` repo to `pnpm` (lockfile import + `.npmrc` setup).

## When NOT to use
- Repos that mandate `npm` or `yarn` (legacy CI, polyrepo with hoisting deps, customer constraint). Forcing `pnpm` breaks builds.
- Single-file scripts using `npx` with no `package.json`.
- Native-heavy projects whose pre-built binaries assume hoisted layout (rare in 2026, but Electron/legacy native modules can still misbehave).
- When the team uses Bun or Deno as the primary runtime — pnpm is fine for deps but adds a dimension to debug.

## Where it fails / limitations
- pnpm's strict, non-hoisted store breaks packages that rely on phantom deps. Agents will "fix" it by setting `shamefully-hoist=true`, defeating the point.
- Workspace protocol (`workspace:*`) is rewritten on `pnpm publish`; if an agent publishes manually, references can leak unresolved.
- Lockfile churn: `auto-install-peers=true` plus `corepack` version mismatch produces noisy diffs CI keeps failing on.
- Windows symlink permissions still bite in 2026 — agents in WSL/dev-containers should pin the same Node + pnpm version as CI.
- `pnpm audit` exits non-zero on transitive CVEs that have no fix; naive "auto-fix" loops fail repeatedly.

## Agentic workflow
Pin the toolchain first: agent reads/writes `packageManager` in root `package.json` and `engines`. Use `corepack` so the version is determined from the file, not globally installed. For installs, prefer `pnpm install --frozen-lockfile` in CI and `pnpm install` only in dev. For dependency changes the agent runs `pnpm add`/`remove` (never edits `package.json` by hand — easy to break peer-dep resolution). For monorepos, `pnpm --filter <pkg>` scopes the change. Always commit `pnpm-lock.yaml`. After updates, run `pnpm audit --prod` and `pnpm outdated` and surface results to a human reviewer.

### Recommended subagents
- `faion-sdd-executor-agent` — gates dep changes behind tests + lockfile diff review.
- `faion-feature-executor` — sequential ops with quality gates per task; ideal for "bump deps, run tests, fix breakage" loops.
- General Sonnet subagent — executes `pnpm` commands, reads lockfile diffs, edits `.npmrc`.
- Security subagent (Opus) — reviews `pnpm audit` output for exploit relevance, not just severity.

### Prompt pattern
```
Task: add <packages> to workspace <name>.
Constraints:
- Use `pnpm --filter <name> add <pkg>` (or `-D` if dev).
- Do NOT edit package.json by hand.
- After install: run `pnpm --filter <name> typecheck && pnpm --filter <name> test`.
- If install fails on peer-dep, set the missing peer (don't disable strict-peer-dependencies).
- Commit package.json + pnpm-lock.yaml together with message
  "chore: deps: add <pkg> to <name>".
```
```
Audit: run `pnpm audit --prod --json`. For each advisory:
- check if package is reachable from a runtime entrypoint
  (`pnpm why <pkg>`).
- if not reachable, mark "noise" and skip.
- if reachable and a fix exists, propose the upgrade.
- if reachable and no fix, propose mitigation or pin to safe version via .pnpmfile.cjs.
Output: structured report, no auto-fixes.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm` | The package manager itself | https://pnpm.io |
| `corepack` | Pin pnpm version per repo | https://nodejs.org/api/corepack.html |
| `npx only-allow pnpm` | Block non-pnpm installs in `preinstall` | https://github.com/pnpm/only-allow |
| `pnpm dlx` | Like `npx` but uses pnpm store | https://pnpm.io/cli/dlx |
| `pnpm why` | Trace why a transitive dep is installed | https://pnpm.io/cli/why |
| `pnpm licenses list` | Inventory licences for compliance | https://pnpm.io/cli/licenses |
| `pnpm patch` | Patch a dep (replaces `patch-package`) | https://pnpm.io/cli/patch |
| `pnpm dedupe` | Reduce duplicates after upgrades | https://pnpm.io/cli/dedupe |
| Changesets | Versioning + publishing in workspaces | https://github.com/changesets/changesets |
| Renovate / Dependabot | Automated dep upgrade PRs | https://renovatebot.com / dependabot.com |
| `npm-check-updates` (`ncu`) | Bulk semver-major upgrades on demand | https://github.com/raineorshine/npm-check-updates |
| `syncpack` | Enforce consistent versions across workspaces | https://github.com/JamieMason/syncpack |
| `nx` / `turbo` | Task graph aware of pnpm workspaces | https://nx.dev / https://turbo.build |
| `verdaccio` | Local registry for testing publishes | https://verdaccio.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions `pnpm/action-setup` | SaaS | Yes | Standard CI install, supports caching |
| Renovate | SaaS + OSS | Yes (config + bot) | Best-in-class for pnpm monorepo upgrades; can group by workspace |
| Dependabot | SaaS | Yes | Native to GitHub; pnpm support is solid in 2026 |
| Snyk | SaaS | Yes (CLI + API) | CVE scanning with reachability analysis |
| Socket.dev | SaaS | Yes (GitHub App + API) | Supply-chain risk score on every PR |
| npm registry / GitHub Packages / Verdaccio | SaaS / OSS | Yes | Pin via `.npmrc` / `@scope:registry=` |
| Turborepo Remote Cache | SaaS | Yes | Speeds CI dramatically with pnpm task graph |
| Nx Cloud | SaaS | Yes | Distributed task execution across workspaces |
| Changesets bot | SaaS | Yes | Enforces changeset on each PR; agent can auto-author the changeset |

## Templates & scripts
The README already ships `.npmrc`, workspace setup, GH Actions, and Dockerfile templates. Useful agent companion: a one-shot bootstrap for a new pnpm workspace that locks the toolchain.

```bash
#!/usr/bin/env bash
# pnpm-bootstrap.sh — initialise a pnpm-pinned project safely.
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

# Workspace marker (ok if empty)
[ -f pnpm-workspace.yaml ] || printf 'packages:\n  - "apps/*"\n  - "packages/*"\n' > pnpm-workspace.yaml

pnpm install
```

## Best practices
- Pin pnpm via `packageManager` field + `corepack` — prevents "works on my machine" version drift.
- Always commit `pnpm-lock.yaml`. CI uses `--frozen-lockfile`. PRs that change deps must include the lockfile diff.
- Keep `shamefully-hoist=false`. If a package is broken, fix it via `.pnpmfile.cjs` `readPackage` hook, not by hoisting the whole tree.
- In monorepos, prefer `workspace:*` over fixed versions for internal packages; Changesets handles the rewrite at publish.
- Use `pnpm dedupe` after major upgrades — pnpm doesn't auto-dedupe like npm.
- Cache the pnpm store in CI keyed by `pnpm-lock.yaml` hash.
- Run `pnpm audit --prod` (skip dev) — most CVEs in dev deps don't ship.
- Group dep updates: Renovate `groupName: 'eslint'` to land them in fewer PRs the agent can review at once.

## AI-agent gotchas
- **Mixing managers.** Agent runs `npm install` in a pnpm repo "to be safe", creates `package-lock.json`, breaks workflow. Add `preinstall: "npx only-allow pnpm"` and a `.gitignore` entry for `package-lock.json`/`yarn.lock`.
- **Hand-editing package.json.** Agent edits `dependencies` directly; peer-dep resolution lies. Force `pnpm add`/`remove` only.
- **Phantom deps.** Code uses a transitive dep that pnpm hides. Agent "fixes" by hoisting; correct fix is `pnpm add` the dep explicitly.
- **Lockfile thrash.** `corepack` version drift causes a re-keyed lockfile every PR. Pin pnpm exactly in `packageManager`.
- **Workspace mis-targeting.** `pnpm add x` at root vs in a sub-package installs in the wrong place. Always pass `--filter`.
- **`workspace:*` leaking.** Manually publishing without Changesets can publish unresolved `workspace:*` to npm. Enforce Changesets-driven release.
- **`pnpm audit` loop.** No-fix CVE → agent retries forever. Cap retries; escalate to human.
- **Permissions / symlinks.** Agent sandbox without symlink perms (some Docker setups) silently degrades. Pre-flight with `pnpm doctor`.
- **Human-in-loop checkpoint.** Lockfile-changing PRs (especially major bumps) get a human review; agents have a poor track record on breaking-change reading.

## References
- https://pnpm.io/ (workspaces, CLI, .npmrc)
- https://pnpm.io/cli/audit, https://pnpm.io/cli/why, https://pnpm.io/cli/patch
- https://nodejs.org/api/corepack.html
- https://github.com/pnpm/only-allow
- https://github.com/changesets/changesets
- https://docs.renovatebot.com/, https://docs.github.com/en/code-security/dependabot
- https://socket.dev/, https://snyk.io/
- https://turbo.build/repo/docs/core-concepts/monorepos/configuring-workspaces
