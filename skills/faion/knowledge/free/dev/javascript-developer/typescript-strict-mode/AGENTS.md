# TypeScript Strict Mode

## Summary

Full strict-mode TypeScript configuration plus additional checks (noUncheckedIndexedAccess, exactOptionalPropertyTypes, noImplicitReturns) that catch whole classes of bugs at compile time. Includes null safety patterns, type narrowing, branded types, and const assertions.

## Why

TypeScript's default settings permit implicit any, unchecked array access, and nullable function returns — all common sources of runtime errors. Enabling strict mode shifts those errors to compile time. noUncheckedIndexedAccess alone prevents 80%+ of out-of-bounds access bugs; exactOptionalPropertyTypes enforces the semantic difference between "missing" and "explicitly undefined".

## When To Use

- All new TypeScript projects from day one
- JavaScript-to-TypeScript migration (enable flags incrementally)
- Library development where consumers depend on correct types
- Production applications requiring high reliability

## When NOT To Use

- Auto-generated code (e.g., protobuf output) — add // @ts-nocheck per file instead
- Legacy codebases where enabling strict causes thousands of errors before a remediation plan exists — enable flags one at a time

## Content

| File | What's inside |
|------|---------------|
| `content/01-config.xml` | tsconfig.json strict flags with rationale for each |
| `content/02-null-safety.xml` | noImplicitAny, strictNullChecks, noUncheckedIndexedAccess, exactOptionalPropertyTypes patterns |
| `content/03-narrowing.xml` | Type guards, discriminated unions, in operator, instanceof, assertion functions |
| `content/04-advanced.xml` | Branded types, const assertions, template literal types |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.strict.json` | Production-ready tsconfig with all strict flags |
