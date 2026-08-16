# Monorepo with Turborepo

## Summary

**One-sentence:** Run a JS/TS monorepo with Turborepo: pnpm workspaces, pinned versions, declared task pipeline, content-hash cache, and remote cache for CI.

**One-paragraph:** Turborepo is a high-performance build system for JavaScript/TypeScript monorepos. Pnpm workspaces own dependency management; turbo.json declares the task pipeline (build → test → lint) with explicit dependsOn edges; content-hash cache makes incremental builds deterministic; remote cache (Vercel Remote Cache or self-hosted) shares hits across CI workers. Output is the workspace + turbo.json + CI integration.

**Ефективно для:**

- Multi-package JS/TS repos (web + api + shared libs).
- Speeding up CI by sharing cached results across PRs.
- Standardising scripts (build/test/lint) across packages.
- Replacing ad-hoc lerna or npm-workspaces setups.

## Applies If (ALL must hold)

- Monorepo has >=3 packages (or apps + at least 1 shared lib).
- Stack is JS/TS with Node >=18.
- Team uses pnpm (or willing to migrate from npm/yarn).
- CI runs the same task pipeline across PRs (caching has payoff).

## Skip If (ANY kills it)

- Single-package repo — Turborepo is overhead without payoff.
- Polyglot monorepo where build owns multiple languages — use Bazel/Nx with language plugins.
- Tiny script repo where caching benefit < setup cost.
- Project already on Nx and migrating would cost more than the benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Package inventory: apps + libs + ownership | table | tech-lead |
| Pnpm version + workspace layout chosen | config | platform |
| Task graph: which task depends on which (build → test ordering) | ADR | tech-lead |
| Remote cache provider (Vercel Remote Cache or self-hosted) + token | config | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[frontend-design]] | Apps may consume the design tokens lib. |
| [[nodejs-service-layer]] | Service apps follow the layered conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 11 testable rules (pnpm workspaces, explicit pipeline, pinned versions, cache outputs, remote cache in CI, no bypass scripts, two-tier layout, shared tsconfig base, per-task inputs, workspace-protocol imports, filtered CI matrix) | 1600 |
| `content/02-output-contract.xml` | essential | JSON Schema for monorepo config spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom/root-cause/fix | 1000 |
| `content/04-procedure.xml` | essential | 7-step procedure: workspace init → hoist shared configs → turbo.json → pin versions → cache inputs+outputs → remote cache CI → filtered CI matrix | 1100 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workspace_layout` | sonnet | Mechanical: pnpm-workspace.yaml + package layout. |
| `pipeline_authoring` | opus | Task graph design (build/test/lint dependencies) needs synthesis. |
| `cache_config` | sonnet | Declare inputs + outputs per task; verify cache hit rate. |
| `import_migration` | sonnet | Rewrite relative cross-package imports to the workspace protocol. |
| `remote_cache_ci` | sonnet | Wire TURBO_TOKEN + TURBO_TEAM env vars in CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pnpm-workspace.yaml` | pnpm workspace declaration |
| `templates/turbo.json` | Turborepo task graph with per-task `inputs` and cached `outputs` |
| `templates/tsconfig-base.json` | Shared tsconfig referenced by package tsconfigs |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-monorepo-turborepo.py` | Validate monorepo config spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[nodejs-service-layer]]
- [[nextjs-app-router]]
- [[frontend-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps repo size, language scope, and caching payoff to a rule from `01-core-rules.xml`, telling the agent whether to apply Turborepo or skip for single-package / polyglot cases. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pnpm-workspace.yaml`

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

### `templates/turbo.json`

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    "**/.env.*local"
  ],
  "globalEnv": [
    "NODE_ENV"
  ],
  "remoteCache": {
    "signature": true
  },
  "tasks": {
    "build": {
      "dependsOn": [
        "^build"
      ],
      "env": [
        "NEXT_PUBLIC_API_URL"
      ],
      "inputs": [
        "src/**",
        "tsconfig.json",
        "package.json"
      ],
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**"
      ]
    },
    "lint": {
      "dependsOn": [
        "^build"
      ],
      "inputs": [
        "src/**",
        ".eslintrc*",
        "package.json"
      ],
      "outputs": []
    },
    "typecheck": {
      "dependsOn": [
        "^build"
      ],
      "inputs": [
        "src/**",
        "tsconfig.json",
        "../../tsconfig.base.json"
      ],
      "outputs": []
    },
    "test": {
      "dependsOn": [
        "build"
      ],
      "inputs": [
        "src/**",
        "tests/**",
        "package.json"
      ],
      "outputs": [
        "coverage/**"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    }
  }
}
```

### `templates/tsconfig-base.json`

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "target": "ES2022",
    "lib": [
      "ES2022"
    ],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
```
