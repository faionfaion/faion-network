# Bun Runtime

## Summary

Bun is a JavaScript/TypeScript runtime, bundler, test runner, and package manager in a single binary. It runs TypeScript directly without transpilation, provides native HTTP via `Bun.serve`, and replaces the npm + tsx + jest + esbuild stack. Default framework pairing is Hono; database ORM is Drizzle with `bun:sqlite`.

## Why

Startup latency, install time, and test speed are all significantly faster than Node equivalents. Eliminating the ts-node/tsx transpilation layer removes a common misconfiguration surface. The "one binary" model simplifies CI and reduces agent tooling errors. `Bun.serve` and `Bun.file` are measurably faster than Node counterparts for I/O-heavy routes.

## When To Use

- Greenfield TypeScript backends where cold-start latency or CI install speed matters.
- CLI tools and build scripts that need fast execution.
- Hono / Elysia API servers targeting `Bun.serve` natively.
- Replacing npm + tsx + jest stack with a single dependency.
- Monorepos with frequent `install` cycles — Bun install is 10-30x faster.

## When NOT To Use

- Long-running Node services with native bindings (`node-gyp` packages) — Bun NAPI support is improving but not 100%.
- Edge runtimes (Cloudflare Workers, Vercel Edge) that run on V8 isolates, not Bun.
- Teams relying on Jest's full snapshot/mock ecosystem — `bun test` parity is incomplete.
- Windows-first dev teams — Bun on Windows works since 2024 but lags macOS/Linux in stability.

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Project init, `package.json` scripts, `bunfig.toml`, version pinning, tsconfig requirements. |
| `content/02-apis.xml` | `Bun.serve`, `Bun.file`, `Bun.env`, `Bun.password`, `Bun.spawn`, `bun:sqlite`, `bun:test`. |
| `content/03-antipatterns.xml` | Mixed lockfiles, `node:cluster` usage, Bun-native APIs in shared libs, dynamic class strings, missing `--frozen-lockfile`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/package.json` | Project manifest with scripts, `packageManager` pin, Hono + Zod deps. |
| `templates/bunfig.toml` | Bun configuration: frozen lockfile in CI, test coverage, build minify. |
| `templates/hono-server.ts` | Hono server with middleware, Zod validation, JWT-protected routes. |
| `templates/drizzle-schema.ts` | Drizzle ORM schema with `bun:sqlite`. |
| `templates/dockerfile` | Multi-stage Bun Dockerfile pinned to `oven/bun:1.1.x-alpine`. |
