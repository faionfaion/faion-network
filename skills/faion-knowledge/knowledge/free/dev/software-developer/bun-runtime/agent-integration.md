# Agent Integration — Bun Runtime

## When to use
- Greenfield TypeScript backends where startup latency, install time, and test runner speed all matter (CLI tools, edge workers, serverless cold starts).
- Replacing `npm` / `yarn` / `pnpm` + `tsx` / `ts-node` + `vitest` / `jest` with one binary.
- Monorepos with frequent `install` cycles — `bun install` is 10-30x faster than npm in CI.
- Hono / Elysia API servers — both target Bun's `Bun.serve` natively for max throughput.
- Build steps where `bun build` ships faster, smaller bundles than esbuild + tsx wrappers.
- LLM-authored projects — Bun's "TypeScript runs directly" reduces tooling that agents misconfigure.

## When NOT to use
- Long-running production Node.js services already battle-tested — Bun's Node compat is strong (>95%) but not 100%; surprising failures in `node:cluster`, `worker_threads`, native modules with `node-gyp`. Don't migrate stable infra without a parallel test rig.
- Apps depending on niche `npm` packages with native bindings (some Postgres / image libs) — Bun's NAPI is improving but not flawless.
- Edge providers (Vercel, Cloudflare Workers) that don't support Bun runtime — your app runs on V8, not Bun.
- Teams wedded to Jest's ecosystem (snapshot tooling, transformers) — `bun test` is fast and Jest-compatible-ish, but plugin ecosystem is thin.
- Windows-first dev teams — Bun on Windows works (since 2024) but lags macOS/Linux.

## Where it fails / limitations
- **Node compat surprises.** `node:vm`, `node:cluster`, parts of `node:tls` (e.g., custom cipher) work differently. Symptom: prod-style libs throw on Bun.
- **NPM packages with `postinstall` native builds** sometimes fail under Bun's installer. Workarounds: `bun pm trust`, or fall back to npm for that step.
- **`bun.lockb` is binary.** Conflicts in Git can't be resolved manually; use `bun install` again. Some teams prefer `bun install --frozen-lockfile` + JSON lockfile (v1.1+ supports `--save-text-lockfile`).
- **Test runner gaps.** `bun test` lacks Jest's full snapshot mocking parity (less mature `jest.mock`). Mocking ESM modules differs.
- **Hot reload via `--hot`** keeps process alive but persists module state across reloads — not always desired. `--watch` restarts cleanly.
- **Bundler quirks.** `bun build --target bun` produces Bun-only output; deploying that to Node runs but loses Bun-specific imports (`Bun.serve`, `Bun.file`).
- **Logging differences.** Bun streams stdout differently; CI log buffers may flush late. `process.stdout.write` works but flush behavior varies.
- **Memory profile.** Bun's `JavaScriptCore` engine has different GC behavior than V8; high-allocation workloads behave differently.
- **Edge-deploy mismatch.** `bun dev` on Mac, `node` on prod Vercel — `Bun.env`, `Bun.file` calls crash. Force isomorphic patterns or restrict Bun-only APIs to dev tooling.

## Agentic workflow
Drive Bun work in 4 stages: (1) a **runtime-detector** subagent inspects target deploy environment (Vercel / Render / VPS / Docker / edge) and decides whether code can use Bun-native APIs or must stay isomorphic-Node; (2) an **install-and-bootstrap** subagent runs `bun init` / `bun add` and pins Bun version in `package.json` `packageManager` field + Dockerfile; (3) a **server-author** subagent generates Hono/Elysia routes via `Bun.serve`; (4) a **test-author** subagent writes `bun test` specs, exclusively using Jest-compatible API (`describe/it/expect`) to keep portability. Always pin Bun version (`oven-sh/setup-bun@v2` with `bun-version`) in CI; LLMs default to "latest" which breaks builds across teams.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `bun install --frozen-lockfile && bun run typecheck && bun test && bun build`.
- A purpose-built **bun-compat-agent** (worth creating): scans for Node-only APIs (`node:cluster`, `node:vm`, `process.binding`) and reports compatibility risk before migration.
- A **bun-perf-agent** (worth creating): runs `bun --bun run` vs `node` benchmarks (start time, RSS, RPS) and emits a comparison table.
- A **lockfile-agent** (worth creating): converts between `package-lock.json` ↔ `bun.lockb` and validates dep versions match.
- A **dockerfile-agent** that emits a multi-stage Bun Dockerfile pinned to `oven/bun:1.1.x-alpine`.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `.env`, `bunfig.toml`, fixture credentials before commit.

### Prompt pattern
Server scaffold:
```
You are a Bun 1.1.x + Hono engineer. Generate src/index.ts:
- Hono app with routes: GET /health, POST /api/users
- Validate body with zod (UserCreateSchema)
- Use Bun.serve via Hono adapter, port from process.env.PORT
- Logging: console.info {method, path, status, latencyMs}
- Tests in src/index.test.ts using bun:test
Do NOT import 'node:cluster' or 'node:worker_threads'.
Run: bun install && bun test && bun --watch run src/index.ts
```

Compat audit:
```
Scan src/ for Node-only API usage that breaks under Bun:
- node:cluster
- node:vm
- node:async_hooks (custom hooks)
- process.binding(*)
- native packages requiring node-gyp
Output: file:line, API, risk (high/med/low), workaround.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bun` | Runtime, package manager, test runner, bundler | https://bun.sh |
| `bun init` | Scaffold new project | bundled |
| `bun install` | npm-compat installer (10-30x faster) | bundled |
| `bun add` / `bun remove` | Manage deps | bundled |
| `bun run` | Run scripts / TS files directly | bundled |
| `bun test` | Jest-compatible test runner | https://bun.sh/docs/cli/test |
| `bun build` | Bundler with `--target=bun|node|browser` | https://bun.sh/docs/bundler |
| `bun pm trust` | Allow lifecycle scripts (postinstall) | https://bun.sh/docs/cli/pm |
| `bun --hot` | Hot reload (persist state) | bundled |
| `bun --watch` | Watch + restart | bundled |
| `bun upgrade` | Update Bun itself | bundled |
| `bunx` | npx-equivalent | bundled |
| Hono | Web framework, Bun-friendly | https://hono.dev |
| Elysia | Bun-first framework | https://elysiajs.com |
| Drizzle ORM | Bun-compat ORM | https://orm.drizzle.team |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `oven/bun` Docker images | OSS | yes | Pin `oven/bun:1.1.x-alpine` for prod containers. |
| `oven-sh/setup-bun@v2` | GitHub Action | yes | Pins Bun version in CI; reads `package.json` `packageManager`. |
| Render / Railway / Fly.io | SaaS | yes | Native Bun support; deploy via Dockerfile or detected `bun start`. |
| Vercel | SaaS | partial | `bun install` works in build; runtime is Node. |
| Cloudflare Workers | SaaS | no | Workers run on V8 isolates, not Bun. Use `bun build --target=browser` for Workers. |
| AWS Lambda | SaaS | partial | Custom runtime; Bun via Lambda layer or container image. |
| Bun + Docker Buildx | OSS | yes | Multi-arch images (arm64 / amd64) ship native binaries. |
| Coolify | OSS (self-host) | yes | Deploys Bun Dockerfiles seamlessly. |

## Templates & scripts
See `templates.md` and `examples.md` for `bunfig.toml`, Hono server, test setup. Add a Dockerfile + version pin (≤50 lines):

```dockerfile
# syntax=docker/dockerfile:1.7
FROM oven/bun:1.1.34-alpine AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN --mount=type=cache,target=/root/.bun/install/cache \
    bun install --frozen-lockfile --production

FROM oven/bun:1.1.34-alpine AS build
WORKDIR /app
COPY package.json bun.lockb ./
RUN --mount=type=cache,target=/root/.bun/install/cache \
    bun install --frozen-lockfile
COPY . .
RUN bun run typecheck && bun test && \
    bun build src/index.ts --target=bun --outdir dist --minify

FROM oven/bun:1.1.34-alpine AS run
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER bun
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD bun -e "fetch('http://localhost:3000/health').then(r=>r.ok?process.exit(0):process.exit(1))"
ENTRYPOINT ["bun", "run", "dist/index.js"]
```

Keep `package.json` `"packageManager": "bun@1.1.34"` matching the image tag.

## Best practices
- **Pin Bun version** in `package.json` `packageManager` and Dockerfile + CI action. Avoid "latest"; reproducibility wins.
- **`bun install --frozen-lockfile` in CI.** Detects lockfile drift, identical to `npm ci`.
- **Use `bun:test` API, not Jest's full surface.** Subset is identical (`describe`, `it`, `expect`); avoid `jest.mock` complexity until parity ships.
- **Isomorphic code by default.** Restrict `Bun.*` APIs to entrypoints / dev tooling so the app can also run under Node if needed.
- **`Bun.file()` for static reads.** Lazy-loaded; faster than `fs.readFileSync`.
- **`Bun.serve` over `node:http`** when on Bun runtime — measurable RPS gains.
- **Co-locate `*.test.ts` next to source.** `bun test` discovers `**/*.test.ts` by default.
- **`tsconfig.json` with `moduleResolution: "bundler"`** — Bun handles modern resolution natively.
- **`bun build --minify`** for prod; `--sourcemap=external` for prod debug.
- **Avoid `--hot` in production.** Bug-prone; use `--watch` for dev restarts; deploy a built bundle.
- **Trust scripts only when needed.** `bun pm trust <pkg>` whitelists lifecycle scripts.
- **CI matrix: `bun-version: [1.1.x, latest]`** to catch upcoming breaks early.

## AI-agent gotchas
- **Mixing npm + Bun lockfiles.** Agent runs `npm install` after `bun install`; `package-lock.json` overrides `bun.lockb`. Pick one PM and lock to it.
- **`bun test` mock semantics.** Agent assumes `jest.mock('./x')` works identically. Module mocking in Bun is via `mock.module()`; semantics differ.
- **Importing `node:cluster`.** Agent ports a Node app verbatim; cluster runtime errors. Refactor to single-process + multiple workers via process manager.
- **`require()` in ESM file.** Bun supports both, but `package.json` `"type": "module"` + CJS shape causes subtle resolution bugs. Stick to ESM.
- **`Bun.serve` and Cloudflare Workers.** Agent writes `Bun.serve` for Workers deploy; Workers expect `export default { fetch }`. Different API.
- **Forgotten `--frozen-lockfile`.** CI runs `bun install` and silently updates lockfile; non-deterministic builds. Always `--frozen-lockfile` in CI.
- **`process.env` typing.** Agent expects strict typing of env vars (`Bun.env.PORT: number`); they're strings. Wrap in `z.coerce.number()`.
- **Hot reload state ghosts.** `--hot` keeps top-level singletons (DB pools); after agent edits the pool config, old pool persists. Restart fully (`--watch`).
- **Native dependency build failure.** `better-sqlite3` postinstall fails under Bun; agent doesn't realize and reports the test failure as code bug. Run `bun install --verbose` to see install errors.
- **Bun-only API in shared lib.** Agent uses `Bun.file()` in a package consumed by both Bun + Node app; Node import crashes. Conditional import or runtime detection.
- **`bun test` flag drift.** Agent runs `bun test --coverage` (supported) then `--coverageThreshold` (different syntax than Jest). Read `bun test --help`.
- **TypeScript path aliases.** Bun reads `tsconfig.json` `paths`, but `compilerOptions.baseUrl` resolution may differ from `tsx`. Verify with `bun --print 'require.resolve("@/utils")'`.
- **Logging and Lambda buffering.** `console.log` not flushed before Lambda handler returns. Use `process.stdout.write` + explicit flush or `bun:logger`.

## References
- Bun docs: https://bun.sh/docs
- `bun test` docs: https://bun.sh/docs/cli/test
- `bun build` docs: https://bun.sh/docs/bundler
- Node.js compatibility table: https://bun.sh/docs/runtime/nodejs-apis
- Hono: https://hono.dev
- Elysia: https://elysiajs.com
- `oven-sh/setup-bun`: https://github.com/oven-sh/setup-bun
- Drizzle + Bun: https://orm.drizzle.team/docs/get-started-sqlite#bun-sqlite
- Sibling methodologies: `free/dev/software-developer/typescript-strict-mode/`, `free/dev/software-developer/nodejs-express-fastify/`, `free/dev/software-developer/pnpm-package-management/`.
