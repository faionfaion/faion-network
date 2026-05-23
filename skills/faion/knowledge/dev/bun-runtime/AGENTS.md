# Bun Runtime

## Summary

**One-sentence:** Produces a Bun-based JS/TS service scaffold (Bun runtime + bunfig + drizzle + Hono + Bun.test) pinned to a specific Bun version and gated in CI.

**One-paragraph:** Produces a Bun-based JS/TS service scaffold (Bun runtime + bunfig + drizzle + Hono + Bun.test) pinned to a specific Bun version and gated in CI. The methodology fires on a named trigger, produces a fixed-shape artifact with evidence anchors and a named owner, and is reviewed against outcomes at a published cadence so it stops being folklore.

**Ефективно для:** команд, що оперують цим артефактом регулярно і потребують детермінованого формату плюс перевірюваного результату.

## Applies If (ALL must hold)

- JS/TS project on Node-style runtime where Bun is a viable replacement.
- Single-binary toolchain (bundler + package manager + test runner) is a goal.
- CI runner supports Bun (oven-sh/setup-bun@v2 available).
- Team is willing to pin and freeze the Bun version.

## Skip If (ANY kills it)

- Production target needs npm-only ecosystem (some enterprise registries are not Bun-compatible).
- Project uses Node-specific native modules without Bun shims.
- Team has no capacity to maintain a second toolchain (Bun + Node) during migration.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Output target path | string | constitution / SDD spec |
| Owner (role:person) | string | team roster |
| Trigger event | event/threshold/schedule | constitution |
| Evidence anchor (URL / ticket / commit) | string | upstream context |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/best-practices-2026` | TS5 strict baseline this scaffold inherits. |
| `free/dev/software-developer/documentation` | Documents the file table + AGENTS.md pair this methodology depends on. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules specific to bun-runtime | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artifact + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Recurring antipatterns with reason | ~900 |
| `content/04-procedure.xml` | medium | Step-by-step procedure (when complexity >= medium) | ~600 |
| `content/06-decision-tree.xml` | essential | Decision tree from observable inputs to a rule conclusion | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Scaffold the output skeleton | sonnet | Mechanical, deterministic. |
| Refine domain-specific content | opus | Needs judgement. |
| Validate against output contract | sonnet | Schema check, deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bunfig.toml` | Bun runtime config with frozen-lockfile and coverage enabled. |
| `templates/dockerfile` | Bun production Dockerfile (multi-stage, distroless). |
| `templates/drizzle-schema.ts` | Drizzle ORM schema template wired to Bun. |
| `templates/hono-server.ts` | Hono HTTP server template on Bun.serve. |
| `templates/package.json` | Pinned Bun version + dev/start/test/build scripts. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bun-runtime.py` | Validates the output record against `02-output-contract.xml`. | After the methodology runs, before publishing the artifact. |

## Related

- [[best-practices-2026]] — see methodology AGENTS.md for context.
- [[code-coverage]] — see methodology AGENTS.md for context.
- [[code-review]] — see methodology AGENTS.md for context.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` keys off the observable inputs documented in Prerequisites and routes to either "run the methodology" (preconditions hold) or "skip and route elsewhere" (preconditions fail). Use it before invoking the methodology, not after.
