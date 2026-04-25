# Agent Integration — pnpm Package Management

## When to use
- All new Node.js/TS projects unless org policy requires npm/yarn.
- Monorepos with > 3 packages — pnpm workspaces are first-class and faster than alternatives.
- CI pipelines where install time matters; pnpm + cache shaves minutes.
- Projects suffering phantom-dependency bugs (imports that work locally, fail elsewhere).
- Container builds wanting layer-cached deps via `pnpm fetch`.

## When NOT to use
- React Native projects pinned to npm/yarn by Metro/Expo tooling (Expo SDK ≤ 50 had pnpm rough edges).
- Hosting platforms that don't support pnpm out of the box without explicit `packageManager` field (rare in 2026).
- Projects whose deploy uses Vercel/Netlify older configs that expected `package-lock.json`.
- One-file scripts; `npm exec`/`bunx` is lighter.

## Where it fails / limitations
- Native add-ons (sharp, node-canvas) sometimes need `node-linker=hoisted` for tools that scan `node_modules` flat.
- Some Jest/Webpack plugins assume hoisted layout — strict mode breaks them; agents then add `shamefully-hoist=true` defeating the point.
- `pnpm patch` workflow is great but agents forget `pnpm patch-commit` and lose the diff.
- Lockfile churn between pnpm major versions; pin via `packageManager` to avoid noise commits.
- Workspace protocol (`workspace:*`) doesn't work with `npm publish` — must `pnpm publish` which rewrites it.

## Agentic workflow
A package agent reads `package.json` + `pnpm-workspace.yaml` → runs `pnpm install --frozen-lockfile` → executes `pnpm -r build && pnpm -r test` → on failure, narrows with `--filter` to the breaking workspace. For dep upgrades, run `pnpm outdated -r --format json`, feed to LLM for risk classification (major/minor/patch), then `pnpm update -r --interactive` only on approved set. Always commit `pnpm-lock.yaml` separately from app code.

### Recommended subagents
- `faion-sdd-executor-agent` — gates installs/builds with frozen lockfile, fails on drift.
- A custom `dep-upgrade` agent (compose) for monthly batched upgrades using `pnpm outdated --json`.

### Prompt pattern
```
Audit dependencies: run `pnpm outdated -r --format json`.
Classify each: patch=auto, minor=review, major=manual.
Output: 3 separate batches as bash commands using `pnpm update --filter=<pkg> <dep>`.
Stop and wait for me to approve major bumps.
```

```
Add @mycompany/ui to apps/web as workspace dep:
`pnpm --filter @mycompany/web add @mycompany/ui --workspace`
Then run `pnpm --filter @mycompany/web... build`.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pnpm` | Package manager itself | `corepack enable` |
| `pnpm dlx` | One-shot package execution | bundled |
| `npm-check-updates` (`ncu`) | Bulk semver bumps before `pnpm install` | `pnpm dlx npm-check-updates -u` |
| `syncpack` | Enforce consistent versions across workspace | `pnpm add -Dw syncpack` |
| `manypkg` | Monorepo sanity checks | `pnpm add -Dw @manypkg/cli` |
| `changesets` | Workspace-aware versioning + changelog | `pnpm add -Dw @changesets/cli` |
| `taze` | Modern alternative to ncu | `pnpm dlx taze` |
| `knip` | Find unused deps/exports | `pnpm dlx knip` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Verdaccio | OSS | Yes — REST API | Self-hosted private registry. |
| GitHub Packages npm | SaaS | Yes — REST API | Auth via `NODE_AUTH_TOKEN`. |
| npmjs.com | SaaS | Yes — REST API | Public registry; `pnpm publish`. |
| Renovate Bot | SaaS + OSS | Yes — config-driven | Best-in-class for pnpm monorepos; understands workspace protocol. |
| Dependabot | SaaS | Partial | Has pnpm support but weaker on workspace deps. |
| Socket.dev | SaaS | Yes — CLI + GH app | Supply-chain risk per package; integrates with pnpm install. |

## Templates & scripts
See `templates.md` for full `.npmrc`, `pnpm-workspace.yaml`, Dockerfile starters. Block accidental npm/yarn use:

```bash
# package.json scripts
"scripts": {
  "preinstall": "npx -y only-allow pnpm"
}
```

```bash
# Quick CI gate: lockfile must be in sync
pnpm install --frozen-lockfile --ignore-scripts \
  || { echo "pnpm-lock.yaml drift — run 'pnpm install' locally"; exit 1; }
```

## Best practices
- Pin manager: `"packageManager": "pnpm@9.x.y"` in root `package.json` so corepack picks the same version everywhere.
- Always `--frozen-lockfile` in CI; never `--no-frozen-lockfile` to "make it work".
- Use `workspace:*` for internal deps; `pnpm publish` rewrites at publish time, no manual conversion.
- Cache the pnpm store in CI separately from `node_modules` (`~/.local/share/pnpm/store/v3`).
- Run `pnpm dedupe` after major upgrades; agents forget this and lockfile bloats.
- Use `pnpm --filter '...[origin/main]'` to build only changed packages — major CI win for monorepos.

## AI-agent gotchas
- Agents mix `npm install` into READMEs/scripts. Add a lint that greps for `\bnpm\s+(install|add)` outside docs.
- LLMs paste `npx` instead of `pnpm dlx` — works but bypasses pnpm's content-addressable store.
- `auto-install-peers=true` masks missing peer deps; agents over-rely on it then break in strict consumers.
- `shamefully-hoist=true` is the universal "agent wrong-fix"; reject any PR adding it without 2-line justification.
- After `pnpm patch`, the agent must commit BOTH the patch file and `package.json` `pnpm.patchedDependencies` block — easy to forget.
- Human-in-loop checkpoint: any major version bump or new direct dep must be approved; agents underweight supply-chain risk.

## References
- pnpm docs — https://pnpm.io/
- pnpm CLI reference — https://pnpm.io/cli/add
- "Why pnpm" — https://pnpm.io/motivation
- Changesets monorepo guide — https://github.com/changesets/changesets
- Renovate pnpm config — https://docs.renovatebot.com/modules/manager/pnpm/
- Sibling: `monorepo-turborepo/` for build orchestration over pnpm workspaces.
