# Agent Integration — Monorepo Setup (Turborepo)

## When to use
- Bootstrapping a JS/TS monorepo from scratch (apps + shared packages); the README's `apps/`, `packages/`, `tools/` shape is the target.
- Migrating multiple npm repos into a single workspace; agent maps each repo to a workspace, lifts shared code, sets up `turbo.json` pipelines.
- Adding remote caching to an existing Turborepo (Vercel Remote Cache or self-hosted).
- Standardising tsconfig / eslint / prettier across packages via a `packages/config` package.

## When NOT to use
- Polyglot monorepos that aren't JS-dominant (e.g., Python + Go + JS) — see Bazel, Pants, or Nx with custom executors.
- Tiny single-app projects (one `apps/web`) — Turborepo overhead is not justified; pnpm workspaces alone suffice.
- Serverless-first projects where each function deploys independently and shared code is minimal — workspace symlinks complicate deployment bundlers.
- Teams without a remote cache strategy — local-only caching gives < 50% of the benefit; without remote, Nx Cloud / Turborepo Remote / self-host is mandatory.

## Where it fails / limitations
- README pins `turbo ^1.12.0` + `pipeline` field. Turborepo 2.x renamed `pipeline` → `tasks`; agents copying as-is will silently fail on `turbo` v2. Update during scaffold.
- `packageManager` field uses pnpm 8; pnpm 9 is current default in 2026. Lockfile compat warnings appear if the agent regenerates.
- `dev` task has `cache: false, persistent: true` correctly, but agent often forgets `persistent: true` for new long-running tasks (`storybook`, `prisma studio`).
- `@monorepo/config` package shape is good but doesn't show how `eslint-preset.js` is consumed (`extends: ['@monorepo/config/eslint-preset']` requires `main`/`exports`).
- Remote cache config: README sets `signature: true` without `secretKey` — production setups need the secret to actually verify.
- `tsup`-based library build in `packages/ui` is fine for libs but agents apply it to *apps*, breaking Next.js builds.
- No mention of Module Federation, only build-time deps; agents asked for "shared runtime modules" generate something that won't tree-shake.

## Agentic workflow
Treat scaffolding as a one-shot task chain: (1) read this reference + project goals, (2) generate the directory tree, (3) install via `pnpm install` and verify `turbo build --dry-run` graph, (4) wire CI with cache tokens, (5) run the full pipeline once and inspect `.turbo/` cache hits. For migrations, work package-by-package; never lift more than one repo per PR. Keep an `apps/_template`/`packages/_template` as the agent's reference for new packages.

### Recommended subagents
- `faion-sdd-executor-agent` — drives migration as sequential tasks (one repo / one package per task).
- General Bash worker — runs `pnpm`, `turbo`, `gh actions` commands and inspects output.

### Prompt pattern
```
Scaffold a Turborepo at ./web-platform with:
- apps/web (Next.js 15), apps/api (Hono on Node)
- packages/ui (React, tsup), packages/config, packages/types, packages/utils
- pnpm@9, turbo v2 (use `tasks`, not `pipeline`)
- shared base tsconfig, eslint preset, prettier config
- GitHub Actions CI with TURBO_TOKEN/TURBO_TEAM secrets
- root scripts: build, dev, lint, test, typecheck, format
After scaffolding, run `pnpm install && turbo build --dry-run` and report graph.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `turbo` | Task orchestrator | `pnpm add -D -w turbo` · https://turbo.build/repo/docs |
| `pnpm` | Workspace package manager | `corepack enable pnpm` · https://pnpm.io |
| `tsup` | Bundle TS libraries (esm+cjs+dts) | `pnpm add -D tsup` |
| `changesets` | Version + publish workspace packages | `pnpm add -D -w @changesets/cli` |
| `syncpack` | Keep dep versions consistent across packages | `pnpm add -D -w syncpack` |
| `manypkg` | Lint workspace structure | `pnpm add -D -w @manypkg/cli` |
| `nx` | Alternative orchestrator (more features) | `pnpm dlx create-nx-workspace` |
| `lerna` | Legacy, on top of Nx | not recommended for new |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vercel Remote Cache | SaaS | Yes — token via env | Default for Turborepo; free tier plenty for solo. |
| Nx Cloud | SaaS | Yes — token | Works with Turborepo via `turbo-remote-cache` or use Nx instead. |
| ducktors/turborepo-remote-cache (self-host) | OSS | Yes | Self-hosted cache server for compliance / cost control. |
| Bytesafe / Verdaccio | OSS / SaaS | Yes | Private npm registries for `@scope/*` packages from monorepo. |
| Chromatic | SaaS | Yes | Visual review per package, integrates with `turbo run storybook`. |
| Renovate | SaaS / OSS | Yes — `monorepoExtras` preset | Keeps shared deps in sync workspace-wide. |
| GitHub Actions cache | SaaS | Yes | Combine with `actions/cache` for `node_modules`, `.turbo/`, `.next/cache`. |

## Templates & scripts
Minimal `turbo.json` for v2 (post-`pipeline → tasks` rename) the agent can paste:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local", "tsconfig.base.json"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "lint": { "dependsOn": ["^build"], "cache": true },
    "typecheck": { "dependsOn": ["^build"], "cache": true },
    "test": { "dependsOn": ["build"], "outputs": ["coverage/**"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

CI cache key for GitHub Actions:

```yaml
- uses: actions/cache@v4
  with:
    path: |
      node_modules/.cache
      .turbo
      apps/*/.next/cache
    key: ${{ runner.os }}-turbo-${{ hashFiles('pnpm-lock.yaml') }}-${{ github.sha }}
    restore-keys: ${{ runner.os }}-turbo-${{ hashFiles('pnpm-lock.yaml') }}-
```

See `templates.md` for a full per-package template tree.

## Best practices
- Use `workspace:*` for internal deps; never floating ranges. Lockfile resolves to local symlinks.
- Keep package boundaries strict: a UI package never imports from an app. Enforce via `eslint-plugin-import` `no-restricted-paths` or `dependency-cruiser`.
- Output declarations from libraries (`tsc --emitDeclarationOnly` or `tsup --dts`) and consume types from `dist`, not `src`. Avoids massive type-graph rebuilds.
- Hash-aware caching: list every input that affects build under `inputs` in `turbo.json` (e.g., `*.css`, `prisma/schema.prisma`); otherwise cache rot or false hits.
- Pin Node + pnpm via `engines` + `packageManager` so agent runs and CI runs match local. Mismatched pnpm = lockfile churn.
- Use Changesets for versioning even private packages — generates per-package CHANGELOGs that humans/agents can reason about.
- Don't hand-edit per-package tsconfigs; extend a single base. Agents diverge configs subtly per package, then types desync.

## AI-agent gotchas
- Agent often introduces `dependencies` cycles (`@monorepo/ui` → `@monorepo/utils` → `@monorepo/ui`) when refactoring. Run `manypkg check` and `madge --circular` post-edit.
- Adding a new task: agent forgets to declare `outputs` → `turbo` caches nothing, runs every time. Always specify outputs even if `[]` for "side-effect-only" tasks.
- v1 vs v2 split: training data is mostly v1 (`pipeline`). For v2, instruct: "use `tasks` field; `with` configs use `passThroughEnv`".
- Agent copies `--filter=@monorepo/web...` (with three dots) thinking it's a pattern; actually it means "package + dependents", which can over-build. Document the filter syntax (`...` = dependents, `...^` = dependents incl. root, `^...` = dependencies).
- Remote cache misconfiguration: agent puts `TURBO_TOKEN` in repo `vars` instead of `secrets`. Always `secrets`.
- Agent edits `pnpm-lock.yaml` by hand to "fix" a conflict — corrupts the integrity hashes. Always re-run `pnpm install`.
- Human-in-loop checkpoint: any change to `turbo.json` global env / globalDependencies should be reviewed; misconfig invalidates the entire cache farm at once.
- Persistent dev tasks under Turborepo: agent runs `turbo dev` then issues `Ctrl+C` from the LLM via timeout — leaves orphan processes. Use `--ui=stream` and explicit `pkill -f turbo` cleanup.

## References
- https://turbo.build/repo/docs — Turborepo docs (v2)
- https://turbo.build/repo/docs/migrating-from-v1 — v1→v2 migration (`pipeline → tasks`)
- https://pnpm.io/workspaces — pnpm workspaces
- https://monorepo.tools/ — comparison of monorepo tools (Nx, Turborepo, Bazel, Lerna)
- https://github.com/changesets/changesets — versioning
- https://github.com/Thinkmill/manypkg — workspace structure linter
- https://github.com/ducktors/turborepo-remote-cache — self-hosted cache
