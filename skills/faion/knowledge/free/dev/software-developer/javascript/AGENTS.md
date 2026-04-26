# JavaScript / TypeScript Standards

## Summary

Universal coding standards for modern JS/TS (2025–2026): TypeScript 5.x with `strict: true`,
named exports over default, `const` + arrow functions for callbacks, `pnpm` as default package
manager, ESLint 9.x flat config + Prettier, Vitest for testing. React follows function components +
hooks; Node.js follows controller → service → repository with centralized error handling.

## Why

TypeScript strict mode catches null-dereference, untyped params, and unreachable branches at compile
time rather than production. Named exports enable accurate IDE refactoring and tree-shaking. The
controller/service/repository split makes business logic unit-testable without HTTP context. A
shared toolchain (pnpm, ESLint, Prettier, Vitest) eliminates per-project setup drift.

## When To Use

- Starting any new TypeScript project (frontend or backend)
- Adding React components, custom hooks, or context providers
- Building Express / Fastify / Bun HTTP services
- Writing unit, component, or API-level tests in Vitest / Jest
- Setting up package management, linting, and formatting for a new repo

## When NOT To Use

- Legacy JavaScript projects where introducing TypeScript requires a full migration — scope first
- Projects locked to Node.js ≤16 — some ES2022 targets and pnpm features won't work
- Deno or edge-runtime projects with incompatible module resolution — verify toolchain support first
- Projects that use Yarn Plug'n'Play workspaces — pnpm config shown is incompatible

## Content

| File | What's inside |
|------|---------------|
| `content/01-typescript-core.xml` | Strict mode options, utility types, generics, type guards, Zod validation |
| `content/02-react-patterns.xml` | Function components, hooks best practices, context pattern, state decision tree |
| `content/03-nodejs-patterns.xml` | Express app structure, controller/service layer, error classes, Pino logging |
| `content/04-testing.xml` | Vitest config, unit + component + API tests with MSW, mocking patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/tsconfig.json` | Full strict `tsconfig.json` with path aliases and monorepo settings |
| `templates/eslint.config.js` | ESLint 9.x flat config with TS strict + React hooks rules |
| `templates/prettierrc.json` | Shared Prettier config (single quotes, trailing commas, LF) |
| `templates/vitest.config.ts` | Vitest config with jsdom + coverage (v8) + setup file |
