# Testing in JavaScript

JavaScript/TypeScript testing stack: Vitest vs Jest decision, component testing, MSW for API mocking, and ESM/CJS pitfalls.

## Summary

Covers the Vitest vs Jest decision tree (2025), unit and component testing patterns, React Testing Library integration, MSW v2 for API mocking, fake timers, coverage configuration, and common pitfalls (ESM/CJS confusion, jsdom layout limitations, MSW v1→v2 migration, fake timer leaks).

## Why

The JS testing ecosystem fragmented between Jest (CommonJS-native) and Vitest (ESM-native, Vite-integrated). Choosing the wrong runner or misconfiguring the environment causes non-deterministic test results and hard-to-debug import errors. This methodology provides a decision tree and working config templates for both runners.

## When To Use

- Setting up a new JavaScript/TypeScript test suite (Vitest or Jest)
- Writing unit tests for React components with React Testing Library
- Mocking HTTP calls with MSW (v2 API)
- Debugging ESM/CJS import resolution errors in tests
- Configuring fake timers without leaking state
- Migrating from Jest to Vitest

## When NOT To Use

- E2E browser tests → use `e2e-testing`
- Go tests → use `testing-go`
- Python tests → use `testing-pytest`
- General mocking strategy decisions → use `mocking-strategies`

## Content

| File | What it covers |
|------|---------------|
| `content/01-runner-selection.xml` | Vitest vs Jest decision tree, ESM/CJS handling, config comparison, migration guide |
| `content/02-patterns.xml` | AAA for JS, async patterns (waitFor, findBy), context/hooks testing, fake timers, coverage config |
| `content/03-msw-and-components.xml` | MSW v2 setup (browser + node), React Testing Library queries, component test structure, jsdom limitations |

## Templates

| File | Purpose |
|------|---------|
| `templates/vitest.config.ts` | Vitest config with coverage, jsdom, path aliases |
| `templates/msw-setup.ts` | MSW v2 server setup for Node (tests) and browser (dev) |
