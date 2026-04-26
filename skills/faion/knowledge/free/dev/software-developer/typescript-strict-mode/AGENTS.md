# TypeScript Strict Mode

## Summary

TypeScript strict mode is a compiler flag group (`strict: true` + four recommended extras) that eliminates implicit `any`, enforces null safety, catches unchecked index access, and requires explicit return types. The canonical 2026 baseline adds `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`, and `noFallthroughCasesInSwitch` on top of `strict: true`. IO boundaries are validated with Zod; `unknown` replaces `any` throughout.

## Why

Strict mode is the cheapest static gate against a class of runtime bugs: null dereferences, unchecked array access, implicit any leaking through service layers. LLM-authored code is particularly prone to `any` leaks and non-null assertion abuse; strict mode plus ESLint rules `no-explicit-any` and `no-non-null-assertion` makes these compile-fail instead of runtime-fail.

## When To Use

- All new TypeScript projects — strict mode is the only sane production default.
- JS-to-TS migrations — adopt incrementally per directory.
- Library / SDK development — `.d.ts` strictness is part of the API contract.
- Critical paths (auth, billing, IAM) where null/undefined bugs are unacceptable.
- LLM-authored codebases — strict is the cheapest static gate against hallucinated APIs.

## When NOT To Use

- Throwaway prototypes / spike branches — strict mode doubles iteration cost.
- Bridging legacy JS with thousands of `noImplicitAny` violations — adopt per-file via `// @ts-check` first.
- Heavily dynamic plugin systems where types fight extension hooks — use Zod parse boundaries instead.
- Codebases with poorly typed third-party libs lacking `@types/*` — add typed adapters first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-config.xml` | Canonical `tsconfig.json` with all strict flags explained; `strict: true` + 4 extras. |
| `content/02-patterns.xml` | `noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess`, type narrowing, branded types, `as const`, assertion functions, discriminated unions. |
| `content/03-antipatterns.xml` | `any` cast, non-null assertion overuse, `@ts-ignore` rot, wide return types, `Partial<T>` everywhere, `as` to bypass checks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.json` | Full strict tsconfig with all recommended flags. |
| `templates/strict-ratchet.sh` | CI script: fail if strict error count increases vs stored baseline. |
