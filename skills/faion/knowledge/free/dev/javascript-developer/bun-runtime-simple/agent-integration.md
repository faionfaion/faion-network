# Agent Integration — Bun Runtime (Simple)

## When to use
- New TypeScript project where the agent can pick the runtime — Bun ships installer, bundler, transpiler, and test runner in one binary.
- Edge / lightweight HTTP API where `Bun.serve` plus Hono delivers low cold-start with minimal deps.
- Monorepos that want a single fast installer (`bun install`) replacing pnpm/npm.
- Local dev tooling, scripts, and codegen — `bun run <ts>` skips `tsx`/`ts-node` overhead.
- Test-runner-only adoption: drive `bun test` against existing TS without changing runtime in prod.

## When NOT to use
- AWS Lambda or other FaaS without first-class Bun runtime — packaging is fragile, cold-start gains lost in adapter layers.
- Heavy native-addon dependencies (Sharp variants, Prisma engines tied to Node, native crypto modules) without verified Bun support.
- Long-running production services where SLA depends on Node-specific telemetry/APM agents not yet supported by Bun.
- Teams locked to enterprise Node LTS support contracts.
- Codebases relying on Node-specific globals (`__dirname`, certain `worker_threads` semantics) without auditing Bun parity.

## Where it fails / limitations
- Some `node:` modules are partial — `node:cluster`, `node:vm` features, and some `worker_threads` corners differ; verify before porting.
- npm-package compatibility is high but not 100% — packages with postinstall native compile steps still surprise.
- `Bun.serve` is not Express; middleware ecosystem is smaller. Use Hono for portable middleware semantics.
- Production observability (OpenTelemetry auto-instrumentation, profiler agents) lags Node — agents must avoid recommending tools that silently no-op.
- `bunfig.toml` is poorly documented vs `package.json` scripts — drift between local and CI is a common foot-gun.

## Agentic workflow
Treat Bun as runtime-plus-toolchain: bootstrap subagent runs `bun init`, lays down `bunfig.toml`, picks Hono if HTTP is needed, and writes a `bun test` skeleton. Implementer subagent prefers `Bun.*` APIs (`Bun.file`, `Bun.password`, `Bun.serve`) over Node equivalents only when there is a measurable win; otherwise stays on Web/Node-portable APIs so the code can fall back to Node. Reviewer subagent flags Bun-only APIs in shared libraries that must run on both runtimes.

### Recommended subagents
- `faion-feature-executor` — sequential bootstrap (`bun init` → install → first route → first test → CI).
- `faion-sdd-execution` — quality gate runs `bun test`, `bunx tsc --noEmit`, `bunx eslint .`.
- `faion-improver` — periodic audit: deps with Bun-incompatible postinstall, `node:` calls without portability shims.

### Prompt pattern
```
Bootstrap a Bun + Hono service for <feature>. Output: bunfig.toml, package.json
(engines.bun, scripts), tsconfig.json (target ES2022, module ESNext,
moduleResolution bundler), src/server.ts (Bun.serve OR Hono app), one route
with Zod validation, one bun:test file. No Node-specific globals.
```
```
Review <file>. Flag every Bun-only API (Bun.*, bun:*, $ template tag) and
classify: (a) acceptable in apps, (b) forbidden in shared lib code, (c) has a
Web/Node-portable equivalent. Suggest the portable form.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `bun` | Runtime + installer + bundler + test runner | bun.sh/install |
| `bun test` | Built-in Vitest-compatible test runner | bun.sh/docs/cli/test |
| `bun build` | Bundler / standalone executable (`--compile`) | bun.sh/docs/bundler |
| `bunx` | Equivalent of `npx`, runs from registry | bun.sh/docs/cli/bunx |
| `bun --watch` | File watcher for dev | bun.sh/docs/cli/run |
| `hono` CLI | Project scaffold for Hono framework | hono.dev |
| `bunfig.toml` | Runtime/test/install config | bun.sh/docs/runtime/bunfig |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Cloudflare Workers (compat) | SaaS | Partial | Hono runs on both; share code between Bun + Workers |
| Railway / Fly.io / Render | SaaS | Yes | First-class Bun deploy via Dockerfile or buildpacks |
| Vercel | SaaS | Partial | Bun supported in build step; runtime mostly Node |
| Hono | OSS | Yes | Portable Web-Standard router; agent's preferred Bun API |
| Drizzle ORM | OSS | Yes | Lightweight, Bun-friendly; avoids Prisma engine issues |
| Better-SQLite (`bun:sqlite`) | Built-in | Yes | Built into Bun; no native compile |
| Sentry SDK | SaaS | Partial | JS SDK works; Node-specific auto-instrumentation may degrade |

## Templates & scripts
See `templates.md` for `bunfig.toml` and the Hono+Zod route patterns. Inline portability lint to keep shared libs Node-compatible:

```bash
#!/usr/bin/env bash
# bun-only-scan.sh — flag Bun-specific imports/APIs in shared lib paths
set -euo pipefail
ROOT="${1:-packages/shared}"
grep -RnE '(\bBun\.[A-Za-z_]+|\bfrom\s+["'\'']bun:|\$\`)' "$ROOT" \
  --include='*.ts' --include='*.tsx' || echo "clean: no Bun-only APIs in $ROOT"
```

CI gate (works in either Node or Bun environments):

```bash
bun install --frozen-lockfile && bunx tsc --noEmit && bun test
```

## Best practices
- Pin Bun version in `package.json` (`"engines": { "bun": ">=1.1.0" }`) and CI image; Bun ships fast and minor versions can break TS plugins.
- Prefer Web APIs (`Request`, `Response`, `URL`, `crypto.subtle`) over Node-native — keeps code portable to Workers / Deno later.
- For HTTP, use Hono unless you have a strong reason for raw `Bun.serve` — middleware story is materially better.
- Schema validation belongs at the route boundary (`@hono/zod-validator`); the `c.req.valid('json')` accessor is type-safe and replaces ad-hoc casts.
- Use `bun:sqlite` for embedded data (test fixtures, dev caches) — zero install, sync API.
- Keep `Bun.env` access centralized in a `config.ts` with Zod parsing; never sprinkle `Bun.env.X!` across files.

## AI-agent gotchas
- LLMs reach for `process.env` and `__dirname`; both work in Bun but mixing them with `Bun.env` and `import.meta.url` causes inconsistencies. Pick one style per project.
- `bun test` is Jest-compatible BUT not 100% — agents importing Vitest-specific helpers (`vi.useFakeTimers` advanced usage, MSW v2 specifics) hit silent gaps.
- Agents tend to install Express on Bun; Express 4 works but loses the ecosystem story Bun is good at. Default to Hono.
- Postinstall scripts: agents auto-add tools (Husky, Prisma) without checking Bun postinstall behavior — `bun install --no-postinstall` may be needed in CI.
- Standalone binaries via `bun build --compile` are great for CLIs but ship the runtime — don't recommend for libraries.
- Human-in-loop checkpoint: before swapping a Node-running production service to Bun. Run a parallel canary first; observability and APM gaps must be assessed.

## References
- Bun docs — https://bun.sh/docs
- Bun runtime API — https://bun.sh/docs/api/http
- bunfig.toml reference — https://bun.sh/docs/runtime/bunfig
- Hono — https://hono.dev/
- Drizzle ORM — https://orm.drizzle.team/
- Bun + Node compatibility — https://bun.sh/docs/runtime/nodejs-apis
