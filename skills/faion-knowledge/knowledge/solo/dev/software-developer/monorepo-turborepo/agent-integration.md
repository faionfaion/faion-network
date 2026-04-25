# Agent Integration — Monorepo Setup (Turborepo)

## When to use
- 2+ JS/TS apps that share UI components, types, or utility packages.
- Solo or small team running web + admin + marketing site that should ship from one repo with shared lint/format/CI.
- Project where CI build time is dominated by re-running unchanged work — Turbo's task cache is a multiplier.
- Microservices in TS/JS where shared types (zod schemas, OpenAPI clients) need single-source-of-truth.

## When NOT to use
- Single app, one team, no shared code — Turbo overhead exceeds benefit.
- Polyglot monorepos (Go + TS + Python) — Turbo only orchestrates JS scripts; consider Bazel, Pants, Nx (better polyglot story), or Moon.
- Teams that need sophisticated dependency graphs (codegen → build → release) — Nx scales further; Bazel is the heavy-duty choice.
- Projects already on Lerna or Yarn Workspaces with no perf pain — migration cost may not pay back.

## Where it fails / limitations
- Cache key bugs: missing `inputs` or wrong `outputs` in `turbo.json` cause stale or no-cache builds; debugging requires `--summarize` and reading hashes.
- Remote cache poisoning: a corrupt artifact uploaded by one machine breaks every other consumer until manually purged.
- `globalDependencies` misconfig — env vars not declared cause silent cache hits across configs (e.g., prod build cached as dev).
- Task pipeline drift: agents add `dev` tasks that get cached because they forgot `"cache": false`.
- Workspace protocol gotchas: `workspace:*` works in pnpm/yarn but not npm <7; agents pick wrong package manager.
- Turbo v1 vs v2 config differences (`pipeline` key removed, replaced by `tasks`); agents copy stale examples.
- Phantom dependencies: hoisted `node_modules` makes packages "work" without explicit deps; breaks when published.

## Agentic workflow
Use a subagent to (1) scaffold the workspace via `npx create-turbo@latest` or `pnpm dlx create-turbo`, (2) extract shared packages (config, ui, types, utils) using a "move + replace imports" agent that updates `package.json` deps and `tsconfig` paths, (3) define `turbo.json` task pipeline + outputs, (4) wire CI with remote cache (Vercel or self-hosted). Always have the agent run `turbo build --dry-run` after config changes — the dry-run output is the truth source for cache hashing.

### Recommended subagents
- `monorepo-extractor` (Sonnet) — moves shared code from an app into a `packages/*` dir, rewrites imports.
- `turbo-config-architect` (Sonnet) — designs `turbo.json` task graph from package layout.
- `package-author` (Haiku) — writes `package.json`, `tsup`/`tsc` build config, `exports` map for a new shared package.
- `ci-wirer` (Sonnet) — writes `.github/workflows/ci.yml` with `pnpm install --frozen-lockfile`, Turbo remote cache env, matrix builds.

### Prompt pattern
```
Task: Extract `lib/auth/` (used in apps/web and apps/admin) into packages/auth.
Steps:
1. Create packages/auth with package.json (name @org/auth), tsconfig (extends @org/config/library), tsup build.
2. Move files; add `export * from './auth'` barrel.
3. Replace all `from '../../../lib/auth'` imports with `from '@org/auth'`.
4. Add @org/auth to apps/web/package.json and apps/admin/package.json deps (workspace:*).
5. Run `pnpm install && turbo build --filter=@org/auth... --dry-run`.
Done = build passes, no remaining relative imports cross app boundaries.
```

```
Audit: turbo.json correctness.
Check:
- every `dev` task has `"cache": false, "persistent": true`.
- every build task lists outputs (dist/**, .next/** but NOT .next/cache/**).
- env vars affecting build are listed in `env` or `globalEnv`.
- no task without `dependsOn` consumes another package's output.
Output: patch suggestion + `turbo run build --summarize` reasoning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `turbo` | Task runner + cache | `npm i -D turbo` or `pnpm dlx create-turbo` |
| `pnpm` | Recommended package manager (best workspace support) | https://pnpm.io |
| `changesets` | Versioning + publish workflow | `npm i -D @changesets/cli` |
| `tsup` | Library bundler (esm + cjs + d.ts) | `npm i -D tsup` |
| `syncpack` | Keep dep versions aligned across packages | `npm i -D syncpack` |
| `manypkg check` | Sanity checks on workspace structure | `npm i -D @manypkg/cli` |
| `turbo-ignore` | Skip CI on packages without changes | https://turbo.build/repo/docs/reference/turbo-ignore |
| `lefthook` / `husky` | Run scoped lints on changed files | https://github.com/evilmartians/lefthook |
| `nx` (alternative) | Larger DX feature set | https://nx.dev |
| `moonrepo` (alternative) | Polyglot, Rust-based runner | https://moonrepo.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vercel Remote Cache | SaaS | Yes via env vars | `TURBO_TOKEN`, `TURBO_TEAM` — works for any host |
| Self-hosted cache (`turborepo-remote-cache`) | OSS | Yes | https://github.com/ducktors/turborepo-remote-cache, deploy on Cloudflare Workers / Fly |
| GitHub Actions | SaaS | Yes | First-class with `actions/cache` for `.turbo` |
| GitLab CI / CircleCI | SaaS | Yes | Same env pattern as GitHub |
| Vercel deployments | SaaS | Yes | `vercel link` per app; auto-detects Turbo |
| Cloudflare Pages | SaaS | Partial | Multi-app deploy needs custom build cmd |
| Sentry / Datadog source maps upload | SaaS | Yes | Add to a `release` Turbo task with `dependsOn: ["build"]` |

## Templates & scripts
See `templates.md` for the full `turbo.json` and `pnpm-workspace.yaml`. Useful audit script:

```bash
#!/usr/bin/env bash
# Usage: ./audit-monorepo.sh
# Quick health check for a Turborepo workspace.
set -euo pipefail
echo "=== Workspace packages ==="
pnpm -r exec pwd | sed "s|$PWD/||"
echo "=== Versions sync ==="
npx syncpack list-mismatches || true
echo "=== Workspace structure ==="
npx @manypkg/cli check || true
echo "=== Turbo dry-run ==="
turbo build --dry-run=json | jq '.tasks[] | {task, package, hash, cache}'
echo "=== Build graph ==="
turbo build --graph=graph.svg && echo "wrote graph.svg"
```

## Best practices
- Use one package manager (prefer pnpm) and pin via `packageManager` field + `engines.pnpm`.
- Define `outputs` for every cacheable task — without them, cache stores nothing useful.
- Declare every env var that affects builds in `env`/`globalEnv`; otherwise prod and preview share cache and break.
- Use `dependsOn: ["^build"]` (caret) for tasks that need upstream packages built first.
- Mark `dev` and `start` tasks `"cache": false, "persistent": true`.
- Keep config packages (eslint, tsconfig) versionless and internal (`"version": "0.0.0"`, `"private": true`).
- Use `workspace:*` for internal deps in pnpm; `"workspace:^"` only when publishing.
- Filter aggressively in CI: `turbo build --filter=...[origin/main]` to only rebuild changed.
- Set up remote cache from day one — even a 5-minute cache hit becomes a 5-second one.

## AI-agent gotchas
- Agents copy v1 `pipeline` key into a v2 project (or vice versa); always check Turbo version first.
- Agents add new packages without `pnpm install` afterwards — workspace symlinks not created, builds fail confusingly.
- Cache invalidation surprises: agents add a script that reads `process.env.FOO` without declaring it; cache returns stale builds.
- Agents put outputs at wrong path (`dist/` when build emits `out/`) — Turbo caches an empty dir, future runs miss.
- Agents conflate `apps/*` and `packages/*` — apps are app-shaped (no `exports`), packages are library-shaped.
- Hardcoded relative imports across packages (`../../../packages/ui/src/...`) leak; require `@org/*` imports only.
- Agents enable remote cache without setting `"signature": true` in shared environments — leads to cache poisoning.
- Human-in-loop checkpoint: changing the dep graph (adding new `packages/*` or moving code between packages) is a structural decision; require human review of `turbo build --graph` output before merge.

## References
- https://turbo.build/repo/docs
- https://turbo.build/repo/docs/crafting-your-repository
- https://turbo.build/repo/docs/reference/configuration
- https://github.com/vercel/turborepo/tree/main/examples
- https://monorepo.tools
- https://pnpm.io/workspaces
- https://github.com/changesets/changesets
- https://github.com/Thinkmill/manypkg
- https://github.com/JamieMason/syncpack
