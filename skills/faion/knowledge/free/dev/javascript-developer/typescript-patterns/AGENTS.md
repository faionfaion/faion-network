# TypeScript Patterns

## Summary

Advanced TypeScript type patterns for production code: utility types, generics, type guards, discriminated unions, and Zod schema validation. Use these patterns to express domain constraints in the type system, catching errors at compile time rather than runtime.

## Why

TypeScript's structural type system enables encoding invariants as types — making impossible states unrepresentable. Patterns like discriminated unions eliminate null checks; generics with constraints prevent misuse at call sites; Zod bridges runtime validation with static types by inferring TS types from schemas.

## When To Use

- Defining repository interfaces with generic CRUD contracts
- Handling API responses where success and error shapes differ
- Validating unknown external input (API bodies, env vars, form data)
- Building reusable generic components or data structures
- Needing exhaustive checks on a union type

## When NOT To Use

- Simple scripts or one-off tools — strict generics add noise without benefit
- Prototyping where types would be reworked immediately anyway
- When a plain interface suffices — avoid generics unless the type parameter is actually reused

## Content

| File | What's inside |
|------|---------------|
| `content/01-utility-types.xml` | Built-in utility types, template literal types, conditional types, indexed access |
| `content/02-generics.xml` | Generic functions with constraints, generic interfaces, generic React components |
| `content/03-type-guards.xml` | Type predicates, discriminated unions, assertion functions |
| `content/04-zod-validation.xml` | Zod schema definition, type inference, safe/unsafe parse patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/repository.ts` | Generic Repository interface with typed CRUD methods |
| `templates/result.ts` | Discriminated union Result type + assertDefined helper |
| `templates/zod-user.ts` | Zod UserSchema with inferred types and validation helpers |
