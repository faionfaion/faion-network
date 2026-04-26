# TypeScript Strict + isolatedDeclarations + Project References

## Summary

Every `tsconfig.json` in a TypeScript workspace must enable `"strict": true`, `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`, and (for libraries / shared packages) `"isolatedDeclarations": true` plus `"composite": true` with `references` to its dependency packages. This raises compile-time precision so that AI-generated code surfaces type errors instead of runtime bugs, and lets fast emitters (Biome, oxc, swc) produce `.d.ts` without invoking `tsc` for inference.

## Why

LLM-written code statistically prefers permissive shapes (`any`, untyped index access, optional fields it never sets). Strict mode + `noUncheckedIndexedAccess` makes those tells into compile errors the agent must fix before the change is accepted; `exactOptionalPropertyTypes` distinguishes "absent" from "explicitly undefined" so partial-update bugs cannot hide. `isolatedDeclarations` constrains exported APIs to be expressible without inference, which keeps the public surface stable and unlocks 10–50x faster declaration emission via non-tsc tools — sub-second feedback that an agentic edit loop relies on. Project references make package builds incremental and parallel.

## When To Use

- Any monorepo with two or more packages.
- Any published library, regardless of size.
- Any application codebase larger than ~10k lines or with multiple AI agents editing concurrently.
- Greenfield TS projects, default-on.

## When NOT To Use

- Throwaway single-file scripts, scratch Bun/Deno snippets, REPL experiments — strictness overhead outweighs the value at this size.
- Application entrypoints (apps, not libs) — keep `strict` and `noUncheckedIndexedAccess` on, but skip `isolatedDeclarations` since apps emit no `.d.ts`.
- Codebases mid-migration where flipping flags would block trunk for weeks — adopt incrementally with `// @ts-expect-error` budgets.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rule.xml` | The five required compiler flags, with the failure mode each one catches. |
| `content/02-project-refs.xml` | How to wire `composite: true` and `references` for monorepo incremental builds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.base.json` | Shared base with all required strict flags; packages extend this. |
| `templates/tsconfig.lib.json` | Library `tsconfig` with `composite` + `isolatedDeclarations` + `references` example. |
