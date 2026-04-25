# Agent Integration — Modern JavaScript / TypeScript Standards

## When to use
- Project bootstrap: pick runtime (Node 22 LTS / Bun 1.x / Deno 2.x), TS version, ESLint/Prettier baseline.
- House-style decisions for a fresh repo (named exports, arrow-vs-function, explicit return types on public APIs).
- Greenfield decisions about the toolchain matrix (TS 5.x, ESLint 9 flat config, Vitest, React 19 / Next 15, Express 5 / Fastify 5).
- Audit of a stale repo to flag drift from 2025-2026 norms (Node 18 EOL, ESLint 8 legacy config, CommonJS-only modules).

## When NOT to use
- Pure framework-specific deep dives (React patterns, Fastify routing) — load the dedicated methodologies.
- Browser-only ES5 targets / IE compatibility work — guidance is ES2022+.
- Polyglot decisions across non-JS languages.
- Migration cost analysis for monoliths — README sets target state but does not estimate effort.

## Where it fails / limitations
- Stack picks are opinions, not laws. Teams on Yarn classic, Webpack 4, or CommonJS will need adapted lint configs.
- "Prefer named exports" collides with framework defaults (Next.js pages, Astro layouts) — agents must permit framework-mandated exceptions.
- Does not cover monorepo tooling (turborepo, nx, pnpm workspaces) — pair with `automation-tooling` or framework starters.
- ESLint 9 flat-config snippets: agents must check actual project's config style (`.eslintrc.js` legacy vs `eslint.config.js`) before edits.

## Agentic workflow
Use this README as the policy document referenced by every JS/TS-touching subagent. Bootstrap pass writes `package.json`, `tsconfig.json`, ESLint flat config, Prettier, and a Vitest skeleton. House-style pass enforces named exports, explicit return types on exported functions, and the `const`/arrow conventions across modified files. Reviewer pass diffs each PR against the standard and emits a checklist.

### Recommended subagents
- `faion-feature-executor` — applies bootstrap tasks sequentially with quality gates (`tsc --noEmit`, `eslint .`, `vitest run`).
- `faion-sdd-execution` — captures house-style decisions in pattern memory so they survive across features.
- `faion-improver` — periodic audit of dependency freshness, runtime version, and lint-config drift.

### Prompt pattern
```
Use javascript-modern as policy. For repo <path>: produce a delta plan that
brings package.json (engines, scripts, deps), tsconfig.json, eslint.config.js,
and prettier config into compliance. Output a numbered diff plan. Stop.
```
```
Review <PR diff> against javascript-modern. Flag default exports, missing
return types on exports, var/let where const fits, CommonJS in new files,
implicit any. Output: file:line — issue — suggested fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsc --noEmit` | Type gate | `npm i -D typescript` |
| `eslint` (flat config) | Lint gate | eslint.org/docs/latest/use/configure/configuration-files |
| `prettier` | Format | `npm i -D prettier` |
| `vitest` | Unit/component tests | vitest.dev |
| `tsx` / `tsdown` / `tshy` | Dev/build for libs | tsx.is, tsdown.dev |
| `npm-check-updates` (`ncu`) | Dependency freshness audit | `npx ncu` |
| `volta` / `fnm` / `nvm` | Pin Node version | volta.sh, fnm.vercel.app |
| `pnpm` / `bun` | Package manager (preferred over npm/yarn for speed) | pnpm.io / bun.sh |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | Yes | Standard CI matrix: Node 20+22, lint, typecheck, test |
| Renovate / Dependabot | SaaS | Yes | Automated dep PRs; agents can auto-merge minors after CI |
| Snyk / GitHub CodeQL | SaaS | Yes | Supply-chain + SAST per PR |
| Bun / Deno deploy | SaaS | Partial | Edge-style runtimes; agents need runtime-aware code paths |
| Sentry | SaaS | Yes | TS-friendly SDK; sourcemap upload via CLI |

## Templates & scripts
See `templates.md` for the full `tsconfig.json`, `eslint.config.js`, and `package.json` skeletons. Inline runtime/version pinning helper:

```bash
#!/usr/bin/env bash
# pin-toolchain.sh — write engines + packageManager to package.json
set -euo pipefail
NODE="${1:-22}"
PNPM="${2:-9.12.0}"
node -e '
const fs=require("fs");
const p=JSON.parse(fs.readFileSync("package.json","utf8"));
p.engines={...(p.engines||{}),node:">='"$NODE"'.0.0"};
p.packageManager="pnpm@'"$PNPM"'";
p.type=p.type||"module";
fs.writeFileSync("package.json",JSON.stringify(p,null,2)+"\n");
'
```

Quick lint+type gate for pre-commit:

```bash
npx tsc --noEmit && npx eslint . --max-warnings=0 && npx prettier --check .
```

## Best practices
- Pin Node via `engines` and `.nvmrc`/Volta — CI failures from runtime drift are silent and slow to diagnose.
- ESM by default (`"type": "module"`), `import.meta.url` over `__dirname`. Add CJS only for legacy consumers and via build emit.
- Use `"exports"` field with conditional entries for libraries; never rely on `main` alone.
- Prefer `Object.freeze`/`as const` for compile-time-and-runtime immutability of small config tables.
- Treat `process.env` as `unknown` — wrap in a typed loader (Zod/Valibot) at startup.
- Keep `tsconfig.json` warnings near zero; suppress per-line, not per-file or globally.

## AI-agent gotchas
- LLMs default to CommonJS (`require`) when generating quick scripts; in an ESM repo this breaks. Always confirm `"type": "module"` and use `import`.
- Default exports leak in (`export default`), and tooling that auto-imports them assigns arbitrary names. Reviewer must reject in shared modules.
- `package.json` `scripts` get duplicated — agents add `lint:fix` next to existing `lint -- --fix`. Diff-first prevents drift.
- ESLint 9 flat config is incompatible with the legacy `.eslintrc` style; agents copy from old projects without checking. Verify which config system the repo uses.
- `"strict": true` on a JS-heavy migration explodes errors; agents must propose a phased flag flip, not flip all flags at once.
- Human-in-loop checkpoint: when changing the runtime version or package manager — affects every contributor's local env.

## References
- Node release schedule — https://nodejs.org/en/about/previous-releases
- TypeScript 5.x release notes — https://www.typescriptlang.org/docs/handbook/release-notes
- ESLint flat config migration — https://eslint.org/docs/latest/use/configure/migration-guide
- Vitest — https://vitest.dev/
- pnpm — https://pnpm.io/
- Bun — https://bun.sh/
