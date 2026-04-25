# Agent Integration — JavaScript / TypeScript

## When to use
- Bootstrapping a new TS-strict project (Node 22, Bun, or browser+bundler) with the recommended stack.
- Migrating loose JS to strict TypeScript (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`).
- Producing named-exports-only modules and aligned ESLint flat config + Prettier.
- Adding type-safe API clients, request validators (zod / valibot), and shared types between packages.
- Generating Vitest/Jest test scaffolds matching the strict config.

## When NOT to use
- Legacy CommonJS-only codebases pinned to Node ≤ 18 — recommended `"module": "ESNext"` + `"moduleResolution": "bundler"` won't apply.
- Mixed JS+TS with `allowJs: true` and `checkJs: false` — strict mode isn't actionable until conversion finishes.
- Frameworks with strong opinions overriding the methodology (Remix, Nuxt, Angular) — defer to framework docs.
- React Native / Expo — runtime constraints differ; bundler resolution and JSX runtime need RN-specific values.
- Edge runtimes (Cloudflare Workers, Vercel Edge) — `target` and globals differ, "Node 22 LTS" advice misleads.

## Where it fails / limitations
- README focuses on coding standards; lacks build-tool guidance (tsup, tsc-alias, swc, esbuild) — agents pick at random.
- "Use `const` and arrow functions" plus "use `function` for hoisting/`this`" — boundary is fuzzy; agents pick inconsistent styles in the same file.
- Recommends ESLint flat config (v9) but doesn't show a minimal config — agents fall back to legacy `.eslintrc` shape that fails on v9.
- No discussion of monorepo/workspace specifics (pnpm workspaces, project references, path aliases).
- "Internal variables — infer when obvious" is subjective; agents over-annotate or under-annotate, and the rule isn't lintable.
- Nothing about ESM/CJS interop pitfalls — `__dirname`, `require`, default-export shims — which dominate real migration work.

## Agentic workflow
Set the stack contract in the prompt: runtime (Node/Bun), module system (ESM only), package manager (pnpm), test runner (Vitest), linter (ESLint v9 flat). Have one subagent run `tsc --noEmit`, `eslint .`, and `<vitest|jest>` after every batch of edits and surface the first error verbatim. Forbid the agent from changing `tsconfig.json` `strict` flags to silence errors; instead require the underlying type fix.

### Recommended subagents
- `faion-sdd-executor-agent` — for SDD-tracked TS work.
- General-purpose subagent constrained to TypeScript files in one workspace package — narrow blast radius, fast type-check loop.
- A "type-fix only" subagent that runs `tsc --noEmit`, picks the first error, edits to fix, repeats. Disallow logic edits.
- `simplify` skill at session end to catch reuse opportunities and dead code.

### Prompt pattern
```
Stack: Node 22 + pnpm + ESM + TypeScript strict + Vitest + ESLint v9 flat.
Constraints: named exports only (except framework-required defaults); no `any`; no `as` without justification comment;
no disabling rules; arrow funcs for callbacks; explicit return types on exported functions.
After edits: run `pnpm typecheck && pnpm lint && pnpm test`. Stop on first failure and report.
```

```
Type-fix loop: run `tsc --noEmit`. Take the first error, fix it minimally, re-run, repeat.
Do not edit production logic. If a fix requires logic change, stop and explain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tsc` | TypeScript compiler / type-check | https://www.typescriptlang.org/ |
| `eslint` (v9 flat) | Lint | https://eslint.org/ |
| `prettier` | Format | https://prettier.io/ |
| `vitest` | Test runner (Vite-native) | https://vitest.dev/ |
| `jest` | Test runner (legacy default) | https://jestjs.io/ |
| `tsx` | Run TS files directly without build | https://github.com/privatenumber/tsx |
| `tsup` | Bundler for libraries | https://tsup.egoist.dev/ |
| `esbuild` / `swc` | Fast TS transpilation | https://esbuild.github.io/ , https://swc.rs/ |
| `pnpm` | Workspace package manager | https://pnpm.io/ |
| `bun` | All-in-one runtime + bundler + test | https://bun.sh/ |
| `tsconfig-paths` | Runtime path-alias resolution | https://github.com/dividab/tsconfig-paths |
| `typescript-eslint` | TS rules for ESLint | https://typescript-eslint.io/ |
| `@biomejs/biome` | ESLint+Prettier alternative, single tool | https://biomejs.dev/ |
| `knip` | Detect unused exports/files | https://knip.dev/ |
| `madge` | Detect circular deps | https://github.com/pahen/madge |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TypeScript playground | SaaS (free) | Yes | Useful for isolating type errors before pasting into chat. |
| StackBlitz / CodeSandbox | SaaS | Yes | Reproducible repros to share with agent. |
| Renovate / Dependabot | SaaS | Yes | Keep TS / ESLint / framework versions current. |
| Turborepo / Nx | OSS | Yes | Monorepo build cache; pair with the methodology for multi-package projects. |
| Sentry | SaaS | Yes | TS source-map ingestion. |
| Vercel / Netlify | SaaS | Yes | First-class TS/ESM deploy. |
| GitHub Actions | SaaS | Yes | Matrix Node/Bun versions for CI. |

## Templates & scripts
Minimal ESLint v9 flat config that aligns with the methodology — drop into a fresh repo:

```js
// eslint.config.js
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  prettier,
  {
    languageOptions: {
      parserOptions: { project: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/consistent-type-imports": "error",
      "import/no-default-export": "error",
    },
  },
);
```

Strict `tsconfig.json` matching the README:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true
  }
}
```

## Best practices
- Use `as const` for literal-typed config objects; pairs with `typeof X[number]` for derived union types as shown in the README.
- Prefer `import type { ... }` for type-only imports — required by `verbatimModuleSyntax` and improves bundler tree-shaking.
- Validate external inputs at the boundary with zod/valibot; trust types only for internal data.
- Public API surfaces (exported functions, classes, types) get explicit return/parameter types; internals can rely on inference.
- Forbid default exports project-wide (lint rule); they break refactor tooling and make multi-cursor edits unsafe.
- Run `tsc --noEmit` in CI separately from build — type errors should fail fast even when bundler is permissive.
- Use `tsx` for one-off scripts in repo (`scripts/`) instead of compiling to dist.

## AI-agent gotchas
- Agents add `any` or `as` to silence errors; require a comment justification rule (eslint `@typescript-eslint/no-explicit-any` + custom comment-required check).
- Agents conflate ESLint legacy and flat configs — they emit `.eslintrc.json` even when `eslint.config.js` exists. State the version explicitly.
- `exactOptionalPropertyTypes` causes subtle errors agents "fix" by removing the option. Forbid changes to compilerOptions in the prompt.
- Default-export shims (`export default { ... }`) sneak in via framework boilerplate; reviewer pass should flag.
- `noUncheckedIndexedAccess` makes `array[0]` `T | undefined`; agents use non-null assertion (`!`) instead of guarding. Disallow `!` outside test code.
- `await` inside `forEach` is silently broken; agents do this often. Require `for...of` for sequential async or `Promise.all(items.map(...))` for parallel.
- Module resolution differs in Node ESM (`"./mod.js"` extension required) vs bundler — agents drop or add extensions inconsistently. Pin one mode.
- Human-in-loop checkpoint: review every `tsconfig.json` change; one flag flip can hide hundreds of issues.
- Do not let an agent run `pnpm install <random package>` autonomously — every dep is a supply-chain risk.

## References
- https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html
- https://eslint.org/docs/latest/use/configure/configuration-files
- https://typescript-eslint.io/
- https://vitest.dev/guide/
- https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production
- https://bun.sh/docs
- https://pnpm.io/workspaces
- https://github.com/total-typescript/ts-reset
