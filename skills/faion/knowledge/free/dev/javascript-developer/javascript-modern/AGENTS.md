# Modern JavaScript/TypeScript Standards

## Summary

Core principles for new JS/TS projects in 2025-2026: TypeScript-first with strict mode, named exports, explicit public API types, pnpm as default package manager, ESLint 9.x flat config, and a code placement decision tree. Supported runtimes: Node.js 22 LTS, Bun 1.x, browser ES2022+.

## Why

JavaScript's ecosystem has consolidated around TypeScript, ESM, and flat ESLint config. Deviating from these defaults (using CJS, legacy .eslintrc, default exports everywhere) creates friction with modern tools, bundlers, and TypeScript inference. Named exports make refactoring and search trivially correct; pnpm enforces strict dep resolution that catches phantom dependency bugs.

## When To Use

- Bootstrapping any new Node.js, Bun, or browser project
- Setting up ESLint in a TypeScript project for the first time
- Deciding whether to use default or named exports
- Choosing a package manager

## When NOT To Use

- Existing projects with established tooling — migrate incrementally, not all at once
- AWS Lambda with vendor-locked Node.js 18 — use Node.js target, skip Bun
- Projects where Yarn 4.x workspaces are already in production

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | TypeScript-first, const/arrow, named exports, explicit types rules |
| `content/02-tooling.xml` | Package manager choice, ESLint 9.x flat config, Prettier, code placement decision tree |

## Templates

| File | Purpose |
|------|---------|
| `templates/eslint.config.js` | ESLint 9.x flat config for TypeScript + React |
| `templates/prettierrc.json` | Prettier baseline config |
