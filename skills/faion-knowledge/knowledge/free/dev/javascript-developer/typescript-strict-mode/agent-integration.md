# Agent Integration — TypeScript Strict Mode

## When to use
- New TS project bootstrap — agent generates `tsconfig.json` with the full strict matrix from this README.
- JS-to-TS migration tasks where the agent must add types incrementally without disabling strict flags.
- Production library work where exported types and `declaration` output need stable signatures.
- Type-error triage: agent reads errors from `tsc --noEmit` and applies the correct narrowing/assertion pattern.
- Pre-merge audit: scan for `any`, `as`, `!`, and missing return types.

## When NOT to use
- Throwaway prototypes / single-file scripts — strict mode + `exactOptionalPropertyTypes` slows iteration without value.
- Codebases with heavy reliance on third-party untyped libraries that can't be stubbed quickly — `skipLibCheck:false` will block.
- React Native / Expo presets that ship their own strict-but-different tsconfig — extend, don't overwrite.
- Pure-JS Node services with no build step.

## Where it fails / limitations
- `exactOptionalPropertyTypes` breaks many existing libraries' option objects; requires audit before flipping on legacy projects.
- `noUncheckedIndexedAccess` adds friction to hot loops over arrays; agents tend to wrap each access with non-null assertions which defeats the flag.
- Branded types use type-only branding — they survive compile but are erased at runtime; agents must remember validation still has to be runtime (Zod/Valibot).
- `verbatimModuleSyntax` requires `import type` discipline; AI-generated code regresses to value imports of types and breaks build under `isolatedModules`.

## Agentic workflow
Use a two-pass pattern: first a "config" pass that lands the canonical `tsconfig.json` and runs `tsc --noEmit` to capture the full error baseline; then a "fix" pass that resolves errors file-by-file, never lowering strictness. Reviewer subagent grep-checks for the specific anti-patterns (`: any`, `as User`, `value!`, missing return types on exported functions). For migrations, gate progress by error-count delta per commit.

### Recommended subagents
- `faion-feature-executor` — sequential file-by-file type fixes, with `tsc --noEmit` as the quality gate after each task.
- `faion-sdd-execution` — pattern/mistake memory: records each new narrowing pattern (type guard, assertion fn) so subsequent agents reuse instead of re-inventing.
- `faion-improver` — audit existing repo for `any`/`as`/`!` density and propose a phased plan.

### Prompt pattern
```
Apply typescript-strict-mode README. Produce a tsconfig.json delta against
<current>: list flag-by-flag (on/off, justification). Then run `tsc --noEmit`
mentally on <file> and output the expected error list with line numbers.
Do not write fixes yet.
```
```
Fix type errors in <file> WITHOUT lowering strictness. Forbidden moves:
adding `any`, `as` casts, non-null `!`, `// @ts-expect-error` without a TODO.
Preferred: type guards, assertion functions, discriminated unions, branded types.
Show the diff and the post-fix `tsc` output.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `typescript` (`tsc --noEmit`) | Source of truth for type errors | `npm i -D typescript` |
| `@typescript-eslint/eslint-plugin` | Lints `no-explicit-any`, `no-non-null-assertion`, `consistent-type-imports` | typescript-eslint.io |
| `tsc-files` | Run `tsc` on staged files only — fast pre-commit gate | `npx tsc-files` |
| `type-coverage` | Percentage of typed identifiers; fails CI under threshold | `npx type-coverage --at-least 99` |
| `tsd` | Author-provided assertion tests for public types | `npx tsd` |
| `arethetypeswrong` (attw) | Validates published d.ts under all module resolutions | `npx attw --pack` |
| `ts-reset` | Strengthens stdlib types (`JSON.parse` returns `unknown`, etc.) | `npm i -D @total-typescript/ts-reset` |
| `zod` / `valibot` | Runtime schemas that double as TS types via `z.infer` | zod.dev / valibot.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| TypeScript Playground | SaaS (free) | Indirect | Useful for sharing minimal repros with humans |
| Sentry | SaaS | Yes | Sourcemap upload + stable runtime types pair well with strict builds |
| GitHub Actions `tsc` matrix | SaaS | Yes | Run `tsc --noEmit` per package across TS 5.x/next |
| ts-pattern (OSS) | OSS | Yes | Exhaustive pattern matching; agents use to keep `Result`/discriminated unions exhaustive |
| Effect (OSS) | OSS | Indirect | Heavyweight; agents should not introduce silently for null safety |

## Templates & scripts
See `templates.md` for the full `tsconfig.json` and reusable `assert*` helpers. Inline strict-debt scanner:

```bash
#!/usr/bin/env bash
# strict-debt.sh — count escape hatches per file
set -euo pipefail
ROOT="${1:-src}"
{
  echo "ANY_TYPE\tAS_CAST\tNON_NULL\tFILE"
  while IFS= read -r f; do
    a=$(grep -cE ':\s*any\b|<any>' "$f" || true)
    c=$(grep -cE '\bas\s+[A-Z][A-Za-z0-9_]*' "$f" || true)
    n=$(grep -cE '![\.\(\[]' "$f" || true)
    if (( a + c + n > 0 )); then printf "%d\t%d\t%d\t%s\n" "$a" "$c" "$n" "$f"; fi
  done < <(find "$ROOT" -name '*.ts' -o -name '*.tsx')
} | column -t
```

## Best practices
- Treat `unknown` as the default for any external input (`fetch` JSON, `JSON.parse`, `process.env.X`); narrow with a guard or schema before use.
- Branded types (`UserId`, `OrderId`) belong at module boundaries — not for every primitive. The cost is the constructor; the value is preventing argument swaps.
- For arrays, prefer pull-based safe accessors (`getFirst`, `at(0)`) over indexed access — composes well with `noUncheckedIndexedAccess`.
- Use `satisfies` to type config objects without losing literal types: `const cfg = {...} satisfies Config;` keeps narrowing.
- `import type` for type-only imports is mandatory under `verbatimModuleSyntax`; configure ESLint `consistent-type-imports` to auto-fix.
- Runtime validation (Zod/Valibot) pairs with strict types — never trust a `as User` from an API response.

## AI-agent gotchas
- LLMs reach for `as` and `!` to silence the compiler; both are bug factories. Reviewer agent must reject every new occurrence absent a justifying comment.
- `noImplicitReturns` plus a `switch` on a discriminated union: if a new variant is added, the missing branch silently returns `undefined`. Use exhaustive `assertNever(x)` helper at the end of switches.
- `exactOptionalPropertyTypes` interacts with React props: `{ size?: 'sm' | 'md' }` no longer accepts `{ size: undefined }`. Agents writing default props must use `Partial` or split into explicit `undefined` unions.
- `strictPropertyInitialization` plus class fields: agents drop `!` on every field; correct fix is constructor assignment or `?` if truly optional.
- Test files often opt out of strictness via separate `tsconfig.test.json` — agents sometimes regress production code by reading the test config. Always reference the right tsconfig.
- Human-in-loop checkpoint: when migrating an existing project, before flipping `exactOptionalPropertyTypes` or `noUncheckedIndexedAccess` (large blast radius).

## References
- TypeScript Handbook — https://www.typescriptlang.org/docs/handbook/intro.html
- tsconfig reference — https://www.typescriptlang.org/tsconfig
- Total TypeScript (Matt Pocock) — https://www.totaltypescript.com/
- typescript-eslint rules — https://typescript-eslint.io/rules/
- Zod — https://zod.dev/
- ts-reset — https://github.com/total-typescript/ts-reset
